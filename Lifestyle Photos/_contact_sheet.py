"""
Build a contact sheet per set so 12 frames can be reviewed at once.

    python3 "Lifestyle Photos/_contact_sheet.py"
"""
import os
from PIL import Image, ImageDraw

BASE = os.path.dirname(os.path.abspath(__file__))
CELL, COLS, PAD, STRIP = 640, 4, 12, 34

for folder, out in (("athletes", "_sheet_athletes.jpg"),
                    ("product", "_sheet_product.jpg")):
    d = os.path.join(BASE, folder)
    files = sorted(f for f in os.listdir(d) if f.endswith(".jpg"))
    if not files:
        continue
    rows = -(-len(files) // COLS)
    W = COLS * CELL + (COLS + 1) * PAD
    H = rows * (CELL + STRIP) + (rows + 1) * PAD
    sheet = Image.new("RGB", (W, H), (18, 18, 18))
    draw = ImageDraw.Draw(sheet)
    for i, f in enumerate(files):
        r, c = divmod(i, COLS)
        x = PAD + c * (CELL + PAD)
        y = PAD + r * (CELL + STRIP + PAD)
        im = Image.open(os.path.join(d, f)).convert("RGB").resize((CELL, CELL), Image.LANCZOS)
        sheet.paste(im, (x, y))
        draw.text((x + 4, y + CELL + 9), f.rsplit(".", 1)[0], fill=(190, 190, 190))
    sheet.save(os.path.join(BASE, out), quality=88)
    print(f"{out}  {len(files)} frames  {sheet.size[0]}x{sheet.size[1]}")
