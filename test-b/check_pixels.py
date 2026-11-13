#!/usr/bin/env python3
"""Rendered-pixel check for Test B: rebuild the puzzle from puzzle.png alone and re-solve.

- Light state: mean luminance of each room's floor area (lit floors are pale yellow,
  dark floors navy). Room rectangles come from layout.json (geometry only; no lit/door data).
- Doorways: scan the centreline of every wall between two adjacent rooms for a run of
  threshold-coloured pixels; a run >= 50 px is a doorway.
- Exterior: scan the whole outer wall for threshold runs; exactly one (the back door) is expected.
Then solver.py is run on the decoded instance and compared with instance.json.
Run: .venv/bin/python test-b/check_pixels.py
"""
import json
import pathlib
import subprocess
import sys

import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
img = np.asarray(Image.open(HERE / "puzzle.png").convert("RGB")).astype(int)
layout = json.loads((HERE / "layout.json").read_text())
truth = json.loads((HERE / "instance.json").read_text())
th = np.array([int(layout["threshold_rgb"][i:i + 2], 16) for i in (1, 3, 5)])


def runs(pixels):
    hit = np.linalg.norm(pixels - th, axis=1) < 30
    best = cur = 0
    out = []
    for i, h in enumerate(hit):
        cur = cur + 1 if h else 0
        if cur == 1:
            start = i
        if cur and (i == len(hit) - 1 or not hit[i + 1]):
            out.append((start, cur))
    return [r for r in out if r[1] >= 50]


decoded = {"rooms": {}, "doors": [], "start": truth["start"], "exit_room": truth["exit_room"]}
report = {"room_luminance": {}, "doorways_found": [], "exterior_threshold_runs": []}
for key, (x0, y0, x1, y1) in layout["rooms"].items():
    patch = img[y0 + 10:y1 - 10, x0 + 10:x1 - 10]
    lum = float((0.299 * patch[..., 0] + 0.587 * patch[..., 1] + 0.114 * patch[..., 2]).mean())
    report["room_luminance"][key] = round(lum, 1)
    decoded["rooms"][key] = {"name": truth["rooms"][key]["name"], "cell": truth["rooms"][key]["cell"], "lit": lum > 140}
for b in layout["boundaries"]:
    a0, a1 = b["span"]
    if b["orient"] == "v":
        line = img[a0 + 8:a1 - 8, b["at"]]
    else:
        line = img[b["at"], a0 + 8:a1 - 8]
    r = runs(line)
    if r:
        decoded["doors"].append(b["rooms"])
        report["doorways_found"].append({"rooms": b["rooms"], "run_px": [x[1] for x in r]})
xs = sorted({v[0] for v in layout["rooms"].values()} | {v[2] for v in layout["rooms"].values()})
ys = sorted({v[1] for v in layout["rooms"].values()} | {v[3] for v in layout["rooms"].values()})
for name, line in [("north", img[ys[0], xs[0]:xs[-1]]), ("south", img[ys[-1], xs[0]:xs[-1]]),
                   ("west", img[ys[0]:ys[-1], xs[0]]), ("east", img[ys[0]:ys[-1], xs[-1]])]:
    for start, length in runs(line):
        report["exterior_threshold_runs"].append({"wall": name, "length_px": length})

(HERE / "qa").mkdir(exist_ok=True)
dec_path = HERE / "qa" / "decoded-from-pixels.json"
dec_path.write_text(json.dumps(decoded, indent=1))
same_lights = all(decoded["rooms"][k]["lit"] == truth["rooms"][k]["lit"] for k in truth["rooms"])
same_doors = {tuple(sorted(d)) for d in decoded["doors"]} == {tuple(sorted(d)) for d in truth["doors"]}
back_ok = report["exterior_threshold_runs"] == [{"wall": "east", "length_px": report["exterior_threshold_runs"][0]["length_px"]}] \
    if report["exterior_threshold_runs"] else False
solved = subprocess.run([sys.executable, str(HERE / "solver.py"), str(dec_path)], capture_output=True, text=True)
sol = json.loads(solved.stdout[:solved.stdout.rindex("}") + 1])
report.update(lights_match_instance=same_lights, doors_match_instance=same_doors, single_exterior_opening_on_east=back_ok,
              resolved_minimum_from_pixels=sol["bfs_minimum_doorways"], resolved_shortest_walks=sol["bfs_number_of_shortest_walks"])
(HERE / "qa" / "pixel-check.json").write_text(json.dumps(report, indent=1) + "\n")
print(json.dumps(report, indent=1))
ok = same_lights and same_doors and back_ok and sol["bfs_minimum_doorways"] == 13
print("PIXEL CHECK PASS" if ok else "PIXEL CHECK FAILED")
sys.exit(0 if ok else 1)
