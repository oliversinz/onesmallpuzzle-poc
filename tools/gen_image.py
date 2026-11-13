#!/usr/bin/env python3
"""Generate one image via the official OpenAI Images API and record usage.

Usage:
  .venv/bin/python tools/gen_image.py --label test-a --prompt-file test-a/image-prompt.txt \
      --size 1024x1024 --out test-a/source-image.png

- Reads OPENAI_API_KEY from .env (never printed or logged).
- One request, n=1, no automatic retry (a timed-out request may still be billed).
- Refuses to run once logs/image-api-usage.json holds MAX_CALLS requests
  (the two authorised paid requests) unless --allow-extra is given.
"""
import argparse
import base64
import datetime
import hashlib
import json
import pathlib
import sys
import time

import requests

ROOT = pathlib.Path(__file__).resolve().parent.parent
USAGE_LOG = ROOT / "logs" / "image-api-usage.json"
MODEL = "gpt-image-2.6-flare"
QUALITY = "high"
MAX_CALLS = 2


def api_key():
    for line in (ROOT / ".env").read_text().splitlines():
        if line.strip().startswith("OPENAI_API_KEY="):
            return line.split("=", 1)[1].strip().strip("'\"")
    sys.exit("OPENAI_API_KEY missing from .env")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--prompt-file", required=True)
    ap.add_argument("--size", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--allow-extra", action="store_true")
    a = ap.parse_args()

    log = json.loads(USAGE_LOG.read_text()) if USAGE_LOG.exists() else []
    if len(log) >= MAX_CALLS and not a.allow_extra:
        sys.exit(f"Budget guard: {len(log)} image requests already recorded; explicit approval needed.")

    prompt = (ROOT / a.prompt_file).read_text().strip()
    body = {"model": MODEL, "prompt": prompt, "size": a.size, "quality": QUALITY,
            "n": 1, "output_format": "png"}
    rec = {"label": a.label, "requested_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
           "endpoint": "POST /v1/images/generations", "model": MODEL, "quality": QUALITY,
           "size_requested": a.size, "n": 1, "output_format": "png",
           "prompt_file": a.prompt_file, "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest()}
    t0 = time.time()
    try:
        r = requests.post("https://api.openai.com/v1/images/generations",
                          headers={"Authorization": f"Bearer {api_key()}"}, json=body, timeout=900)
        rec["http_status"] = r.status_code
        data = r.json()
    except Exception as e:  # record the failure; do not retry
        rec.update(error=f"{type(e).__name__}: {e}", duration_s=round(time.time() - t0, 1))
        log.append(rec)
        USAGE_LOG.write_text(json.dumps(log, indent=2) + "\n")
        sys.exit(f"Request failed: {rec['error']}")
    rec["duration_s"] = round(time.time() - t0, 1)
    rec["usage"] = data.get("usage")
    for k in ("created", "size", "quality", "background", "output_format"):
        if k in data:
            rec[f"response_{k}"] = data[k]
    if not r.ok or "data" not in data:
        rec["error"] = data.get("error", data)
        log.append(rec)
        USAGE_LOG.write_text(json.dumps(log, indent=2) + "\n")
        sys.exit(f"API error {r.status_code}: {json.dumps(rec['error'])[:500]}")
    item = data["data"][0]
    if item.get("revised_prompt"):
        rec["revised_prompt"] = item["revised_prompt"]
    png = base64.b64decode(item["b64_json"])
    out = ROOT / a.out
    out.write_bytes(png)
    rec["output_file"] = a.out
    rec["output_sha256"] = hashlib.sha256(png).hexdigest()
    rec["output_bytes"] = len(png)
    log.append(rec)
    USAGE_LOG.write_text(json.dumps(log, indent=2) + "\n")
    print(json.dumps(rec, indent=2))


if __name__ == "__main__":
    main()
