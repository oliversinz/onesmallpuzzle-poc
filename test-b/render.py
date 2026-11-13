#!/usr/bin/env python3
"""Deterministic renderer for Test B. Reads instance.json (the data solver.py verifies),
writes puzzle.svg, puzzle.png (1080x1080) and layout.json (geometry for the pixel read-back).
Run: .venv/bin/python test-b/render.py
"""
import json
import pathlib
import random

import cairosvg
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
inst = json.loads((HERE / "instance.json").read_text())

XS = [64, 314, 634, 904]          # plan column edges
YS = [282, 482, 692, 902]         # plan row edges
WALL_IN, WALL_EX, GAP = 16, 22, 72
# door centre along its wall, keyed by the unordered room pair
DOOR_AT = {
    ("office", "library"): 404, ("office", "hall"): 196, ("library", "studio"): 352,
    ("library", "bedroom"): 548, ("studio", "bathroom"): 772, ("bedroom", "bathroom"): 612,
    ("hall", "dining"): 196, ("dining", "kitchen"): 812, ("kitchen", "bootroom"): 812,
}
DOOR_AT = {tuple(sorted(k)): v for k, v in DOOR_AT.items()}
SWING = {  # (room the leaf swings into, hinge at the low or high end of the gap)
    ("office", "library"): ("office", "high"), ("office", "hall"): ("office", "low"),
    ("library", "studio"): ("library", "high"), ("library", "bedroom"): ("library", "low"),
    ("studio", "bathroom"): ("studio", "high"), ("bedroom", "bathroom"): ("bedroom", "low"),
    ("hall", "dining"): ("hall", "high"), ("dining", "kitchen"): ("kitchen", "low"),
    ("kitchen", "bootroom"): ("bootroom", "low"),
}
SWING = {tuple(sorted(k)): v for k, v in SWING.items()}
BACK_DOOR_Y = 838
LIT_FLOOR, DARK_FLOOR = ("#fff0b8", "#efbf58"), ("#2c3858", "#212a43")
THRESH = "#c8955a"
WALL = "#15130f"
TEXT = "#f4ead2"

rooms = inst["rooms"]
by_cell = {tuple(v["cell"]): k for k, v in rooms.items()}
doors = {tuple(sorted(d)) for d in inst["doors"]}


def rect_of(key):
    r, c = rooms[key]["cell"]
    return XS[c], YS[r], XS[c + 1], YS[r + 1]


out = []
add = out.append
add('<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080">')
add('<defs>')
add(f'<radialGradient id="lit" cx="50%" cy="50%" r="70%"><stop offset="0" stop-color="{LIT_FLOOR[0]}"/>'
    f'<stop offset="1" stop-color="{LIT_FLOOR[1]}"/></radialGradient>')
add(f'<linearGradient id="dark" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{DARK_FLOOR[0]}"/>'
    f'<stop offset="1" stop-color="{DARK_FLOOR[1]}"/></linearGradient>')
add('<linearGradient id="spill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd76a" stop-opacity="0.38"/>'
    '<stop offset="1" stop-color="#ffd76a" stop-opacity="0"/></linearGradient>')
add('<linearGradient id="spillx" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffd76a" stop-opacity="0.38"/>'
    '<stop offset="1" stop-color="#ffd76a" stop-opacity="0"/></linearGradient>')
add('</defs>')

# --- night garden ---------------------------------------------------------------
add('<rect width="1080" height="1080" fill="#16241d"/>')
rng = random.Random(7)
for _ in range(900):
    x, y = rng.uniform(0, 1080), rng.uniform(0, 1080)
    if XS[0] - 30 < x < XS[3] + 30 and YS[0] - 30 < y < YS[3] + 30:
        continue
    col = rng.choice(["#1d2e25", "#122019", "#22362b"])
    add(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rng.uniform(2, 5):.1f}" ry="{rng.uniform(1, 2.5):.1f}" fill="{col}"/>')
for cx, cy, r in [(1010, 300, 46), (1040, 420, 30), (30, 960, 40), (995, 1035, 34), (20, 520, 26)]:
    add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#10261a"/><circle cx="{cx - r * .25:.0f}" cy="{cy - r * .25:.0f}" '
        f'r="{r * .55:.0f}" fill="#173322"/>')
# stepping stones from the back door
for i, (sx, sy) in enumerate([(944, 846), (976, 880), (1000, 920), (1018, 962)]):
    add(f'<ellipse cx="{sx}" cy="{sy}" rx="17" ry="12" fill="#3a3f3a"/>')

# light spilling from windows of lit rooms onto the lawn (exterior walls only)
windows = [("studio", "top", 770), ("studio", "right", 380), ("bathroom", "right", 586), ("dining", "left", 796),
           ("hall", "left", 586), ("library", "top", 474), ("office", "top", 150), ("kitchen", "bottom", 474),
           ("bedroom", "none", 0)]
for key, side, pos in windows:
    if side == "none" or not rooms[key]["lit"]:
        continue
    if side == "right":
        add(f'<polygon points="{XS[3]},{pos - 40} {XS[3]},{pos + 40} {XS[3] + 90},{pos + 70} {XS[3] + 90},{pos - 70}" fill="url(#spillx)"/>')
    elif side == "left":
        add(f'<polygon points="{XS[0]},{pos - 40} {XS[0]},{pos + 40} {XS[0] - 60},{pos + 64} {XS[0] - 60},{pos - 64}" '
            f'fill="url(#spillx)" transform="rotate(180 {XS[0] - 30} {pos})"/>')

# --- floors ----------------------------------------------------------------------
for key in rooms:
    x0, y0, x1, y1 = rect_of(key)
    lit = rooms[key]["lit"]
    add(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="url(#{"lit" if lit else "dark"})"/>')
    tone = "#000000" if lit else "#ffffff"
    for yy in range(y0 + 26, y1, 26):  # floorboards
        add(f'<line x1="{x0}" y1="{yy}" x2="{x1}" y2="{yy}" stroke="{tone}" stroke-opacity="{0.06 if lit else 0.04}" stroke-width="1.5"/>')

# --- furniture (low contrast, kept away from doorways) ---------------------------------
def furn(key):
    return ("#d9a443", "#c88f2e") if rooms[key]["lit"] else ("#36446a", "#3d4c74")


def box(key, x, y, w, h, rx=4, shade=0):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{furn(key)[shade]}"/>')


box("office", 92, 304, 30, 150, 3)                      # console table
add(f'<rect x="140" y="322" width="100" height="78" rx="6" fill="none" stroke="{furn("office")[1]}" stroke-width="4"/>')
for i in range(9):                                         # library shelves
    box("library", 330 + i * 32, 298, 26, 22, 2, i % 2)
box("library", 345, 410, 54, 50, 14)                       # armchair
box("studio", 852, 300, 34, 150, 3)                        # plan chest
add(f'<polygon points="666,452 696,340 726,452" fill="none" stroke="{furn("studio")[1]}" stroke-width="5"/>')
box("bedroom", 332, 560, 120, 112, 8)                      # bed
box("bedroom", 340, 568, 46, 30, 6, 1)
box("bedroom", 396, 568, 46, 30, 6, 1)
box("bathroom", 822, 506, 64, 130, 26)                     # bath
box("bathroom", 690, 646, 50, 30, 10, 1)                   # basin
add(f'<circle cx="190" cy="818" r="40" fill="{furn("dining")[0]}"/>')   # table + chairs
for ang_x, ang_y in [(0, -54), (0, 54), (-56, 0), (56, 0)]:
    add(f'<rect x="{190 + ang_x - 11}" y="{818 + ang_y - 11}" width="22" height="22" rx="4" fill="{furn("dining")[1]}"/>')
box("kitchen", 336, 862, 276, 28, 3)                       # counter along back wall
box("kitchen", 520, 708, 92, 60, 4, 1)                     # range
box("bootroom", 716, 864, 160, 26, 3)                      # bench
for i in range(4):
    box("bootroom", 728 + i * 36, 836, 22, 18, 5, 1)       # boots

# --- walls -----------------------------------------------------------------------
def hwall(y, x0, x1, gaps, t):
    segs, cur = [], x0
    for g in sorted(gaps):
        segs.append((cur, g - GAP / 2))
        cur = g + GAP / 2
    segs.append((cur, x1))
    for a, b in segs:
        add(f'<rect x="{a:.0f}" y="{y - t / 2:.0f}" width="{b - a:.0f}" height="{t}" fill="{WALL}"/>')


def vwall(x, y0, y1, gaps, t):
    segs, cur = [], y0
    for g in sorted(gaps):
        segs.append((cur, g - GAP / 2))
        cur = g + GAP / 2
    segs.append((cur, y1))
    for a, b in segs:
        add(f'<rect x="{x - t / 2:.0f}" y="{a:.0f}" width="{t}" height="{b - a:.0f}" fill="{WALL}"/>')


layout = {"rooms": {}, "boundaries": [], "back_door": None, "threshold_rgb": THRESH, "wall_rgb": WALL}
for key in rooms:
    layout["rooms"][key] = rect_of(key)

door_draw = []
for r in range(3):
    for c in range(3):
        a = by_cell[(r, c)]
        if c + 1 < 3:  # vertical wall to the right
            b = by_cell[(r, c + 1)]
            pair = tuple(sorted((a, b)))
            gaps = [DOOR_AT[pair]] if pair in doors else []
            vwall(XS[c + 1], YS[r], YS[r + 1], gaps, WALL_IN)
            layout["boundaries"].append({"rooms": [a, b], "orient": "v", "at": XS[c + 1], "span": [YS[r], YS[r + 1]]})
            if gaps:
                door_draw.append(("v", XS[c + 1], gaps[0], a, b))
        if r + 1 < 3:  # horizontal wall below
            b = by_cell[(r + 1, c)]
            pair = tuple(sorted((a, b)))
            gaps = [DOOR_AT[pair]] if pair in doors else []
            hwall(YS[r + 1], XS[c], XS[c + 1], gaps, WALL_IN)
            layout["boundaries"].append({"rooms": [a, b], "orient": "h", "at": YS[r + 1], "span": [XS[c], XS[c + 1]]})
            if gaps:
                door_draw.append(("h", YS[r + 1], gaps[0], a, b))
for pair in doors:
    assert pair in DOOR_AT, pair

# exterior walls (back door gap on the boot room's east wall)
hwall(YS[0], XS[0] - WALL_EX / 2, XS[3] + WALL_EX / 2, [], WALL_EX)
hwall(YS[3], XS[0] - WALL_EX / 2, XS[3] + WALL_EX / 2, [], WALL_EX)
vwall(XS[0], YS[0], YS[3], [], WALL_EX)
vwall(XS[3], YS[0], YS[3], [BACK_DOOR_Y], WALL_EX)
layout["back_door"] = {"x": XS[3], "y": BACK_DOOR_Y}

# windows: pale glass lines set into exterior walls
for key, side, pos in windows:
    if side == "none":
        continue
    glass = "#cfe3f0" if rooms[key]["lit"] else "#59647e"
    if side in ("top", "bottom"):
        y = YS[0] if side == "top" else YS[3]
        add(f'<rect x="{pos - 34}" y="{y - 3}" width="68" height="6" fill="{glass}"/>')
    else:
        x = XS[0] if side == "left" else XS[3]
        add(f'<rect x="{x - 3}" y="{pos - 34}" width="6" height="68" fill="{glass}"/>')

# doorways: wooden threshold + door leaf + swing arc
def leaf_col(key):
    return "#7a4e17" if rooms[key]["lit"] else "#d7dceb"


L = GAP - 6
for orient, at, pos, a, b in door_draw:
    into, hinge = SWING[tuple(sorted((a, b)))]
    sgn = 1 if into == b else -1          # b is right of / below a
    d = 1 if hinge == "low" else -1
    col = leaf_col(into)
    if orient == "v":
        add(f'<rect x="{at - WALL_IN / 2}" y="{pos - GAP / 2}" width="{WALL_IN}" height="{GAP}" fill="{THRESH}"/>')
        hx, hy = at, pos - d * GAP / 2
        ex, ey = hx + sgn * L, hy
        fx, fy = hx, hy + d * L
        sweep = 1 if sgn * d > 0 else 0
    else:
        add(f'<rect x="{pos - GAP / 2}" y="{at - WALL_IN / 2}" width="{GAP}" height="{WALL_IN}" fill="{THRESH}"/>')
        hx, hy = pos - d * GAP / 2, at
        ex, ey = hx, hy + sgn * L
        fx, fy = hx + d * L, hy
        sweep = 1 if sgn * d < 0 else 0
    add(f'<line x1="{hx}" y1="{hy}" x2="{ex}" y2="{ey}" stroke="{col}" stroke-width="4"/>')
    add(f'<path d="M {ex} {ey} A {L} {L} 0 0 {sweep} {fx} {fy}" fill="none" stroke="{col}" stroke-width="1.6" '
        f'stroke-dasharray="5 5" stroke-opacity="0.8"/>')

# back door: threshold, outward arrow and label
add(f'<rect x="{XS[3] - WALL_EX / 2}" y="{BACK_DOOR_Y - GAP / 2}" width="{WALL_EX}" height="{GAP}" fill="{THRESH}"/>')
add(f'<path d="M {XS[3] + 18} {BACK_DOOR_Y} L {XS[3] + 70} {BACK_DOOR_Y}" stroke="#9fe0a8" stroke-width="7" stroke-linecap="round"/>')
add(f'<path d="M {XS[3] + 58} {BACK_DOOR_Y - 15} L {XS[3] + 80} {BACK_DOOR_Y} L {XS[3] + 58} {BACK_DOOR_Y + 15}" '
    f'fill="none" stroke="#9fe0a8" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>')
add(f'<text x="{XS[3] + 92}" y="{BACK_DOOR_Y - 58}" font-family="Ubuntu" font-weight="bold" font-size="23" fill="#9fe0a8" text-anchor="middle">Back</text>')
add(f'<text x="{XS[3] + 92}" y="{BACK_DOOR_Y - 32}" font-family="Ubuntu" font-weight="bold" font-size="23" fill="#9fe0a8" text-anchor="middle">door</text>')

# --- room labels and bulbs -----------------------------------------------------------
def bulb(cx, cy, lit, s=1.0):
    if lit:
        for i in range(8):
            import math
            a = i * math.pi / 4
            add(f'<line x1="{cx + math.cos(a) * 21 * s:.1f}" y1="{cy + math.sin(a) * 21 * s:.1f}" '
                f'x2="{cx + math.cos(a) * 29 * s:.1f}" y2="{cy + math.sin(a) * 29 * s:.1f}" stroke="#a8670a" stroke-width="{3 * s:.1f}" stroke-linecap="round"/>')
        add(f'<circle cx="{cx}" cy="{cy}" r="{15 * s:.1f}" fill="#fffbe8" stroke="#a8670a" stroke-width="{3 * s:.1f}"/>')
    else:
        add(f'<circle cx="{cx}" cy="{cy}" r="{15 * s:.1f}" fill="#1b2236" stroke="#8e9bbd" stroke-width="{3 * s:.1f}"/>')


LABEL_POS = {"office": (189, 0), "library": (474, 0), "studio": (769, 0), "hall": (189, 0), "bedroom": (540, 0),
             "bathroom": (740, 0), "dining": (189, 0), "kitchen": (430, 0), "bootroom": (769, 0)}
BULB_POS = {"office": (190, 361), "library": (474, 372), "studio": (790, 372), "hall": (190, 592),
            "bedroom": (512, 618), "bathroom": (740, 575), "dining": (256, 770), "kitchen": (430, 790),
            "bootroom": (769, 780)}
for key, v in rooms.items():
    x0, y0, x1, y1 = rect_of(key)
    lx = LABEL_POS[key][0]
    col = "#5a3a0c" if v["lit"] else "#b9c3de"
    add(f'<text x="{lx}" y="{y0 + 44}" font-family="Ubuntu" font-weight="bold" font-size="25" letter-spacing="1.5" '
        f'fill="{col}" text-anchor="middle">{v["name"].upper()}</text>')
    bulb(*BULB_POS[key], v["lit"])

# "you" token in the hall
add('<circle cx="108" cy="606" r="19" fill="#e4572e" stroke="#fff6e6" stroke-width="4"/>')
add('<text x="108" y="658" font-family="Ubuntu" font-weight="bold" font-size="24" fill="#7a2c10" text-anchor="middle">YOU</text>')

# --- text ----------------------------------------------------------------------------------
add(f'<text x="62" y="104" font-family="P052" font-weight="bold" font-size="74" fill="{TEXT}">Lights out</text>')
# legend
add('<rect x="636" y="62" width="44" height="44" rx="4" fill="url(#lit)"/>')
bulb(658, 84, True, 0.62)
add(f'<text x="692" y="93" font-family="Ubuntu" font-size="24" fill="{TEXT}">on</text>')
add('<rect x="760" y="62" width="44" height="44" rx="4" fill="url(#dark)"/>')
bulb(782, 84, False, 0.62)
add(f'<text x="816" y="93" font-family="Ubuntu" font-size="24" fill="{TEXT}">off</text>')
rules = [
    "Step into a room and its light flips: on turns off, off turns on.",
    "Stepping out changes nothing. Reuse rooms and doorways freely.",
    "Start in the Hall. Leave by the back door with every light off.",
]
for i, line in enumerate(rules):
    add(f'<text x="64" y="{162 + i * 38}" font-family="Ubuntu" font-size="30" fill="#e6dcc2">{line}</text>')
add('<text x="64" y="968" font-family="Ubuntu" font-weight="bold" font-size="38" fill="#ffd66b">'
    'How few doorways can you get away with?</text>')
add('<text x="64" y="1012" font-family="Ubuntu" font-size="27" fill="#e6dcc2">'
    'Count every pass through an inside doorway. The back door doesn’t count.</text>')
add('</svg>')

svg = "\n".join(out)
(HERE / "puzzle.svg").write_text(svg)
(HERE / "layout.json").write_text(json.dumps(layout, indent=1))
cairosvg.svg2png(bytestring=svg.encode(), write_to=str(HERE / "puzzle.png"), output_width=1080, output_height=1080)
im = Image.open(HERE / "puzzle.png").convert("RGB")
im.save(HERE / "puzzle.png", optimize=True)
(HERE / "qa").mkdir(exist_ok=True)
im.resize((360, 360), Image.LANCZOS).save(HERE / "qa" / "puzzle-360.png")
print("wrote", HERE / "puzzle.png", im.size)
