"""
Derive the Athlon Rub v2 colorways and web exports from the gold masters.

Every mark in system-v2 is flat single-colour by construction, so a colourway
is an RGB swap with the alpha channel left untouched. That keeps the
anti-aliased edges identical across all four colourways: recolouring a
gradient or beveled mark this way would not work, which is one more reason
the system is flat.

    python3 "Brand Elements/make_colorways.py"
"""
import glob
import os

import numpy as np
from PIL import Image

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "system-v2")
SRC = os.path.join(BASE, "gold")

# Official palette, sampled from PALETA PRINCIPAL on the logo sheet.
COLORWAYS = {
    "green": (0x0F, 0x2B, 0x1E),   # on cream / white surfaces
    "cream": (0xEA, 0xE9, 0xCB),   # on green / black surfaces
    "white": (0xFF, 0xFF, 0xFF),   # on photography and video
}
WEB_MAX = 512   # longest edge for the site-ready copies


def recolor(src, dst, rgb):
    a = np.array(Image.open(src).convert("RGBA"))
    a[..., 0], a[..., 1], a[..., 2] = rgb
    Image.fromarray(a).save(dst, "PNG", optimize=True)


def web_export(src, dst):
    im = Image.open(src).convert("RGBA")
    if max(im.size) > WEB_MAX:
        s = WEB_MAX / max(im.size)
        im = im.resize((max(1, round(im.size[0] * s)),
                        max(1, round(im.size[1] * s))), Image.LANCZOS)
    im.save(dst, "PNG", optimize=True)


def main():
    masters = sorted(glob.glob(os.path.join(SRC, "*.png")))
    if not masters:
        raise SystemExit(f"no masters in {SRC}")

    for name, rgb in COLORWAYS.items():
        out = os.path.join(BASE, name)
        os.makedirs(out, exist_ok=True)
        for m in masters:
            recolor(m, os.path.join(out, os.path.basename(m)), rgb)
        print(f"{name:6s} {len(masters)} files -> {out}")

    web = os.path.join(BASE, "web")
    os.makedirs(web, exist_ok=True)
    total = 0
    for m in masters:
        dst = os.path.join(web, os.path.basename(m))
        web_export(m, dst)
        total += os.path.getsize(dst)
    print(f"web    {len(masters)} files -> {web}  ({total // 1024} KB total)")


if __name__ == "__main__":
    main()
