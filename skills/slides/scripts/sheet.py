"""Tile build/sheet-*.png (one per Beamer page) into a single contact sheet.

    python3 tools/sheet.py build/sheet.png build/sheet-*.png
"""
import sys
from PIL import Image

out, files = sys.argv[1], sorted(sys.argv[2:])
ims = [Image.open(f) for f in files]
w, h = ims[0].size
cols, gap = 5, 6
rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (cols * (w + gap) + gap, rows * (h + gap) + gap), "white")
for i, im in enumerate(ims):
    sheet.paste(im, (gap + (i % cols) * (w + gap), gap + (i // cols) * (h + gap)))
sheet.save(out)
print(out, sheet.size, len(ims), "pages")
