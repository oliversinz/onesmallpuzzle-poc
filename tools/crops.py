#!/usr/bin/env python3
"""Save enlarged crops of named regions of a PNG for clue-by-clue visual QA.
Usage: .venv/bin/python tools/crops.py test-c/puzzle.png boxes.json out_dir
boxes.json: {"name": [x0, y0, x1, y1], ...}
"""
import json
import pathlib
import sys

from PIL import Image

src, boxes, out = sys.argv[1], json.loads(pathlib.Path(sys.argv[2]).read_text()), pathlib.Path(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
im = Image.open(src).convert("RGB")
for name, (x0, y0, x1, y1) in boxes.items():
    c = im.crop((x0, y0, x1, y1))
    s = max(1, min(3, 600 // max(c.size)))
    c.resize((c.size[0] * s, c.size[1] * s), Image.LANCZOS).save(out / f"crop-{name}.png")
    print(out / f"crop-{name}.png")
