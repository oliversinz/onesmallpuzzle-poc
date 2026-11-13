#!/usr/bin/env python3
"""Run one non-interactive Codex CLI task as a real subprocess and log it.

Usage:
  tools/codex_call.py --label a1 --prompt-file test-a/codex-a1-prompt.md \
      --out test-a/codex-a1.json [--schema tools/schema.json] [--image img.png] [--cd test-a]

Codex runs with the user's ChatGPT login (no API key), a read-only sandbox and
approval policy "never". The model actually used is read back from Codex's own
session record (~/.codex/sessions/.../rollout-*.jsonl, turn_context.model).
"""
import argparse
import datetime
import json
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
LOG = ROOT / "logs" / "codex-execution.log"
SESSIONS = pathlib.Path.home() / ".codex" / "sessions"


def secret_values():
    env = ROOT / ".env"
    vals = []
    if env.exists():
        for line in env.read_text().splitlines():
            if "=" in line and not line.strip().startswith("#"):
                v = line.split("=", 1)[1].strip().strip("'\"")
                if len(v) > 12:
                    vals.append(v)
    return vals


def scrub(path):
    """Fail loudly (and redact) if a credential ever appears in a Codex output file."""
    p = pathlib.Path(path)
    if not p.exists():
        return False
    text = p.read_text(errors="replace")
    hit = False
    for v in secret_values():
        if v in text:
            text = text.replace(v, "<REDACTED>")
            hit = True
    if hit:
        p.write_text(text)
    return hit


def session_meta(thread_id):
    if not thread_id:
        return {}
    for f in SESSIONS.rglob(f"*{thread_id}*.jsonl"):
        meta = {"session_file": str(f)}
        for line in f.open():
            d = json.loads(line)
            p = d.get("payload", {})
            if d.get("type") == "session_meta":
                for k in ("cli_version", "originator", "source", "model_provider"):
                    meta[k] = p.get(k)
            if d.get("type") == "turn_context":
                for k in ("model", "effort", "approval_policy", "sandbox_policy"):
                    meta[k] = p.get(k)
        return meta
    return {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    ap.add_argument("--prompt-file", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--schema")
    ap.add_argument("--image", action="append", default=[])
    ap.add_argument("--cd", default=".")
    a = ap.parse_args()

    events_path = ROOT / "logs" / f"codex-{a.label}-events.jsonl"
    cmd = ["codex", "exec"]
    for im in a.image:  # -i takes a list, so keep it before the other options
        cmd += ["-i", str(pathlib.Path(im).resolve())]
    cmd += ["-s", "read-only", "-C", str((ROOT / a.cd).resolve()), "--json",
            "-o", str((ROOT / a.out).resolve())]
    if a.schema:
        cmd += ["--output-schema", str((ROOT / a.schema).resolve())]
    cmd += ["-"]  # prompt from stdin

    prompt = (ROOT / a.prompt_file).read_text()
    started = datetime.datetime.now().astimezone()
    t0 = time.time()
    with open(events_path, "w") as ev, open(ROOT / "logs" / f"codex-{a.label}-stderr.txt", "w") as er:
        proc = subprocess.run(cmd, input=prompt, text=True, stdout=ev, stderr=er, cwd=ROOT)
    secs = round(time.time() - t0, 1)

    thread_id, usage, n_cmds = None, None, 0
    for line in events_path.read_text().splitlines():
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        if d.get("type") == "thread.started":
            thread_id = d.get("thread_id")
        if d.get("type") == "turn.completed":
            usage = d.get("usage")
        if d.get("type") == "item.completed" and d.get("item", {}).get("type") == "command_execution":
            n_cmds += 1

    leaked = scrub(events_path) | scrub(ROOT / a.out)
    rec = {
        "label": a.label,
        "started": started.isoformat(timespec="seconds"),
        "duration_s": secs,
        "exit_code": proc.returncode,
        "command": " ".join(cmd),
        "prompt_file": a.prompt_file,
        "images": a.image,
        "output_file": a.out,
        "events_file": str(events_path.relative_to(ROOT)),
        "thread_id": thread_id,
        "usage": usage,
        "shell_commands_run_by_codex": n_cmds,
        "auth": "ChatGPT login (codex login status)",
        "credential_found_in_output": leaked,
        **session_meta(thread_id),
    }
    with LOG.open("a") as f:
        f.write(json.dumps(rec) + "\n")
    print(json.dumps(rec, indent=2))
    sys.exit(proc.returncode)


if __name__ == "__main__":
    main()
