#!/usr/bin/env python3
"""Render a 1080x1080 composition SVG to PNG (and a 360 px QA preview).

Usage: .venv/bin/python tools/render_svg.py test-a/compose.svg test-a/puzzle.png
Relative <image href="..."> paths resolve against the SVG's own folder.
"""
import pathlib
import sys

import cairosvg
from PIL import Image

src, dst = map(pathlib.Path, sys.argv[1:3])
cairosvg.svg2png(url=str(src.resolve()), write_to=str(dst), output_width=1080, output_height=1080, unsafe=True)
im = Image.open(dst).convert("RGB")
assert im.size == (1080, 1080), im.size
im.save(dst, optimize=True)
qa = dst.parent / "qa"
qa.mkdir(exist_ok=True)
im.resize((360, 360), Image.LANCZOS).save(qa / f"{dst.stem}-360.png")
print(f"{dst}: {im.size}, preview {qa / (dst.stem + '-360.png')}")
