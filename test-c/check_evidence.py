#!/usr/bin/env python3
"""Check the final Test C artwork against Claude's clue inventory, then re-run the logic on
the evidence as decoded from the artwork (not as intended).

1. Structural (compose.svg, the exact source of puzzle.png): which track paths are drawn in the
   softened vs sharp style, where each path starts (through the gateway) and ends (which bay),
   car fills and roof-snow placement, scrape fill.
2. Pixels (puzzle.png): car body and roof colour per bay, an empty bay 3, yellow scrape pixels,
   and which track style (if any) enters the snow just in front of each bay.
3. Decoded evidence -> verify_logic.analyse() -> must give bay 5 only.
Run: .venv/bin/python test-c/check_evidence.py
"""
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter

import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import verify_logic as vl  # noqa: E402

NS = {"s": "http://www.w3.org/2000/svg", "x": "http://www.w3.org/1999/xlink"}
XL = "{http://www.w3.org/1999/xlink}href"
BAY_X = {1: 200, 2: 380, 3: 560, 4: 740, 5: 920}
GATE_Y = (690, 813)          # opening between the two wall ends (from compose.svg)
report = {"structural": {}, "pixels": {}}

# ---------- 1. structural -------------------------------------------------------------------
root = ET.parse(HERE / "compose.svg").getroot()
paths = {p.get("id"): p.get("d") for p in root.iter("{%s}path" % NS["s"]) if p.get("id")}
groups = {g.get("id"): [u.get(XL)[1:] for u in g.iter("{%s}use" % NS["s"])] for g in root.iter("{%s}g" % NS["s"]) if g.get("id")}
style = {}
for gid, look in (("soft-routes", "softened"), ("sharp-route", "sharp")):
    for pid in groups.get(gid, []):
        style[pid] = look
tracks = Counter()
path_info = {}
for pid, look in style.items():
    nums = list(map(float, re.findall(r"-?\d+(?:\.\d+)?", paths[pid])))
    (sx, sy), (ex, ey) = nums[:2], nums[-2:]
    bay = min(BAY_X, key=lambda b: abs(BAY_X[b] - ex))
    through_gate = sx < 0 and GATE_Y[0] < sy < GATE_Y[1]
    path_info[pid] = {"style": look, "start": [sx, sy], "end": [ex, ey], "ends_in_bay": bay,
                      "end_within_car_width": abs(BAY_X[bay] - ex) <= 55, "enters_through_gateway": through_gate}
    if pid.endswith("-left"):
        tracks[(frozenset({"O", f"B{bay}"}), look)] += 1
report["structural"]["track_paths"] = path_info
report["structural"]["tracks_by_bay"] = {next(x for x in k[0] if x != "O"): k[1] for k in tracks}
uses = [u for u in root.findall("s:use", NS)]
cars = {int(u.get("x")): u.get("fill") for u in uses if u.get(XL) == "#car"}
roofs = {int(u.get("x")) for u in uses if u.get(XL) == "#roof-snow"}
scrape_fills = {e.get("fill") for e in root.iter() if e.get("fill") == "#f1ce35"}
report["structural"]["cars"] = {str(x): f for x, f in sorted(cars.items())}
report["structural"]["roof_snow_at"] = sorted(roofs)

# ---------- 2. pixels ------------------------------------------------------------------------
img = np.asarray(Image.open(HERE / "puzzle.png").convert("RGB")).astype(int)


def median(x0, x1, y0, y1):
    return [int(v) for v in np.median(img[y0:y1, x0:x1].reshape(-1, 3), axis=0)]


def classify(rgb):
    r, g, b = rgb
    if r > 200 and g > 170 and b < 120:
        return "yellow"
    if r > 150 and g < 100 and b < 120:
        return "red"
    if min(rgb) > 215:
        return "snow/white"
    return f"other{rgb}"


def near(rgb_hex, tol):
    c = np.array([int(rgb_hex[i:i + 2], 16) for i in (1, 3, 5)])
    return np.linalg.norm(img - c, axis=2) < tol


sharp_px = near("#62576f", 22) | near("#7a7089", 22)
soft_px = near("#bdb7ce", 10)
decoded_cars, decoded_tracks = {}, Counter()
for bay, cx in BAY_X.items():
    body = classify(median(cx - 30, cx + 30, 628, 636))
    roof = classify(median(cx - 18, cx + 18, 562, 580))
    band = (slice(658, 672), slice(cx - 70, cx + 70))
    n_sharp, n_soft = int(sharp_px[band].sum()), int(soft_px[band].sum())
    entering = "sharp" if n_sharp > 40 else ("softened" if n_soft > 40 else None)
    report["pixels"][f"bay{bay}"] = {"body": body, "roof": roof, "sharp_px_in_front": n_sharp,
                                     "softened_px_in_front": n_soft, "tracks_entering": entering}
    if body in ("yellow", "red"):
        decoded_cars[f"B{bay}"] = (body, roof == "snow/white")
    if entering:
        decoded_tracks[(frozenset({"O", f"B{bay}"}), entering)] += 1
lamp_box = json.loads((HERE / "qa-boxes.json").read_text())["C4"]
x0, y0, x1, y1 = map(int, lamp_box)
report["pixels"]["yellow_scrape_px_in_C4_box"] = int(near("#f1ce35", 40)[y0:y1, x0:x1].sum())

# ---------- 3. decoded evidence -> logic -----------------------------------------------------
vl.CARS, vl.TRACKS = decoded_cars, decoded_tracks
culprits, n_hist = vl.analyse()
culprits_noroof, _ = vl.analyse(use_roof=False)
report["decoded_cars"] = {k: list(v) for k, v in decoded_cars.items()}
report["decoded_tracks"] = {next(x for x in k[0] if x != "O"): k[1] for k in decoded_tracks}
report["logic_on_decoded_evidence"] = {"possible_culprits": culprits, "ignoring_roof": culprits_noroof,
                                       "consistent_histories": n_hist}
expected_cars = {"B1": ("yellow", True), "B2": ("red", True), "B4": ("yellow", False), "B5": ("yellow", True)}
checks = {
    "structural_tracks_match_inventory": tracks == Counter({(frozenset({"O", "B2"}), "softened"): 1,
                                                           (frozenset({"O", "B4"}), "sharp"): 1,
                                                           (frozenset({"O", "B5"}), "softened"): 1}),
    "all_paths_through_gateway_and_into_car": all(v["enters_through_gateway"] and v["end_within_car_width"] for v in path_info.values()),
    "structural_cars_match": cars == {200: "#f1ce35", 380: "#bd3e53", 740: "#f1ce35", 920: "#f1ce35"} and roofs == {200, 380, 920},
    "scrape_same_yellow_as_cars": "#f1ce35" in scrape_fills,
    "pixel_cars_match": decoded_cars == expected_cars and report["pixels"]["bay3"]["body"] == "snow/white",
    "pixel_tracks_match": decoded_tracks == vl.TRACKS and report["pixels"]["bay1"]["tracks_entering"] is None
                          and report["pixels"]["bay3"]["tracks_entering"] is None,
    "pixel_scrape_visible": report["pixels"]["yellow_scrape_px_in_C4_box"] > 150,
    "logic_on_decoded_gives_bay5": culprits == ["B5"] and culprits_noroof == ["B5"],
}
report["checks"] = checks
(HERE / "qa").mkdir(exist_ok=True)
(HERE / "qa" / "evidence-check.json").write_text(json.dumps(report, indent=1) + "\n")
print(json.dumps(report, indent=1))
ok = all(checks.values())
print("EVIDENCE CHECK PASS" if ok else "EVIDENCE CHECK FAILED")
sys.exit(0 if ok else 1)
