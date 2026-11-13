#!/usr/bin/env python3
"""Side-by-side thumbnails of the three finished PNGs (variety check), plus 360 px previews.
Run: .venv/bin/python tools/contact_sheet.py  -> logs/contact-sheet.png
"""
import pathlib

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
tiles = [ROOT / t / "puzzle.png" for t in ("test-a", "test-b", "test-c")]
tiles = [p for p in tiles if p.exists()]
sheet = Image.new("RGB", (len(tiles) * 370 + 10, 380), "white")
for i, p in enumerate(tiles):
    sheet.paste(Image.open(p).convert("RGB").resize((360, 360), Image.LANCZOS), (10 + i * 370, 10))
sheet.save(ROOT / "logs" / "contact-sheet.png")
print("logs/contact-sheet.png", [p.parent.name for p in tiles])
