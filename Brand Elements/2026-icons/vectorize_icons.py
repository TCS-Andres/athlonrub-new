"""
Athlon Rub 2026 icon family: raster sheets -> clean single-colour SVG.

The sheets in _raw/ were generated with Nano Banana Pro (kie.ai), black ink
on white, in grids. Sheet 1 set the style; sheets 2-5 were generated with
sheet 1 attached as the style reference so the family stays consistent.

For each grid cell this script:
  1. thresholds to pure ink,
  2. drops any caption the model added under the icon (a separate short
     band of ink rows below the icon),
  3. crops to the icon, pads to a square with a shared margin,
  4. traces with potrace into one flat path,
  5. writes  svg/{name}.svg  (fill #000) and the site include
     site/src/_includes/icons/{name}.liquid  (fill currentColor).

Also traces the designer's official single-colour badges
(2026-rebrand/badges) into currentColor SVGs, so they can sit in gold on the
dark sections.

Run:  /usr/bin/python3 "Brand Elements/2026-icons/vectorize_icons.py"
Needs Pillow, numpy and the potrace CLI (brew install potrace).
"""

import os
import re
import subprocess
import tempfile

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
RAW = os.path.join(HERE, "_raw")
OUT_SVG = os.path.join(HERE, "svg")
OUT_SITE = os.path.join(REPO, "site", "src", "_includes", "icons")
BADGES = os.path.join(REPO, "Brand Elements", "2026-rebrand", "badges")

CANVAS = 600     # traced canvas, px
FILL = 0.84      # icon's larger side as a share of the canvas

# sheet file -> (cols, rows, names in reading order; None = skip that cell)
SHEETS = {
    "sheet1_benefits.png": (3, 2, ["fast-absorbing", "warming", "non-greasy",
                                   "botanical", "certified-lab", "tested-clean"]),
    "sheet2_uses.png": (3, 2, ["warm-up", "performance", "recovery",
                               "shake", "pump", "rub-in"]),
    "sheet3_roster.png": (3, 2, [None, "endurance", "lifting",
                                 "paddle", None, "gear-bag"]),
    "sheet4_commerce.png": (3, 2, ["shipping", "guarantee", "worldwide",
                                   "secure", "shatter-proof", "bundles"]),
    "sheet5_redo.png": (3, 1, ["combat", "therapist", "team"]),
}


def ink_mask(img):
    g = np.asarray(img.convert("L"), dtype=np.uint8)
    return g < 128


def row_bands(mask, min_gap):
    """Contiguous runs of rows containing ink, merging gaps < min_gap."""
    rows = np.where(mask.any(axis=1))[0]
    if rows.size == 0:
        return []
    bands, start, prev = [], rows[0], rows[0]
    for r in rows[1:]:
        if r - prev > min_gap:
            bands.append((start, prev))
            start = r
        prev = r
    bands.append((start, prev))
    return bands


def isolate_icon(cell):
    """Return the icon's bounding box inside a cell mask, minus any caption."""
    h = cell.shape[0]
    bands = row_bands(cell, min_gap=max(12, h // 40))
    if not bands:
        return None
    # Captions are short bands under the icon. Keep the tallest band, plus
    # any band touching it closely (parts of the icon split by a thin gap).
    tallest = max(bands, key=lambda b: b[1] - b[0])
    keep = [b for b in bands if (b[1] - b[0]) > 0.22 * (tallest[1] - tallest[0])]
    y0, y1 = min(b[0] for b in keep), max(b[1] for b in keep)
    sub = cell[y0:y1 + 1]
    cols = np.where(sub.any(axis=0))[0]
    return y0, y1 + 1, cols[0], cols[-1] + 1


def normalise(mask):
    """Crop, pad to square, scale so the icon fills FILL of CANVAS."""
    ys, xs = np.where(mask)
    m = mask[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    h, w = m.shape
    side = int(max(h, w) / FILL)
    sq = np.zeros((side, side), dtype=bool)
    oy, ox = (side - h) // 2, (side - w) // 2
    sq[oy:oy + h, ox:ox + w] = m
    im = Image.fromarray((~sq * 255).astype(np.uint8)).resize((CANVAS, CANVAS), Image.LANCZOS)
    return im.point(lambda v: 0 if v < 128 else 255).convert("1")


def trace(bitmap, alphamax="1.0"):
    with tempfile.TemporaryDirectory() as td:
        pbm, svg = os.path.join(td, "i.pbm"), os.path.join(td, "i.svg")
        bitmap.save(pbm)
        subprocess.run(["potrace", pbm, "-s", "--flat", "-t", "8", "-a", alphamax,
                        "-O", "0.3", "-o", svg], check=True)
        raw = open(svg).read()
    paths = re.findall(r'<path d="([^"]+)"', raw, re.S)
    tf = re.search(r'<g transform="([^"]+)"', raw).group(1)
    w = re.search(r'width="([\d.]+)pt"', raw).group(1)
    h = re.search(r'height="([\d.]+)pt"', raw).group(1)
    d = " ".join(" ".join(p.split()) for p in paths)
    return f"0 0 {float(w):g} {float(h):g}", tf, d


def write(name, viewbox, tf, d, kind="icon"):
    os.makedirs(OUT_SVG, exist_ok=True)
    os.makedirs(OUT_SITE, exist_ok=True)
    body = f'<g transform="{tf}"><path d="{d}"/></g>'
    with open(os.path.join(OUT_SVG, f"{name}.svg"), "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" fill="#000">{body}</svg>\n')
    with open(os.path.join(OUT_SITE, f"{name}.liquid"), "w") as f:
        f.write(f'<svg class="{kind} {kind}--{name}" viewBox="{viewbox}" fill="currentColor" '
                f'aria-hidden="true" focusable="false">{body}</svg>')


def main():
    made = []
    for sheet, (cols, rows, names) in SHEETS.items():
        mask = ink_mask(Image.open(os.path.join(RAW, sheet)))
        H, W = mask.shape
        ch, cw = H // rows, W // cols
        for i, name in enumerate(names):
            if not name:
                continue
            r, c = divmod(i, cols)
            cell = mask[r * ch:(r + 1) * ch, c * cw:(c + 1) * cw].copy()
            # clear a thin border so neighbours' strays never leak in
            cell[:6, :] = cell[-6:, :] = False
            cell[:, :6] = cell[:, -6:] = False
            box = isolate_icon(cell)
            if not box:
                print("EMPTY", sheet, name)
                continue
            y0, y1, x0, x1 = box
            icon = np.zeros_like(cell)
            icon[y0:y1, x0:x1] = cell[y0:y1, x0:x1]
            vb, tf, d = trace(normalise(icon))
            write(name, vb, tf, d)
            made.append(name)

    for f in sorted(os.listdir(BADGES)):
        if not f.endswith(".png"):
            continue
        name = "badge-" + f.replace(" Icon.png", "").lower().replace(" ", "-")
        im = Image.open(os.path.join(BADGES, f)).convert("RGBA")
        a = np.asarray(im, dtype=np.float32)
        lum = a[..., :3].mean(axis=2)
        ink = (a[..., 3] > 128) & (lum < 160)
        vb, tf, d = trace(normalise(ink), alphamax="1.1")
        write(name, vb, tf, d, kind="badge")
        made.append(name)

    print(f"{len(made)} marks:", ", ".join(made))


if __name__ == "__main__":
    main()
