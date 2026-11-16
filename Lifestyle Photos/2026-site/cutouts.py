"""
Product cutouts for the v3 site, from the real 2026-label pack shots.

Method
------
1. Mask: recraft/remove-background (kie.ai) on each real photo. Recraft only
   computes alpha; the RGB it returns is byte-identical to the source photo,
   so label pixels are never redrawn. (Seedream 5.5's transparent mode was
   tried too and rejected: it regenerates the bottle and swapped the 500 mL's
   black screw cap for an over-cap.)
2. Snap the near-opaque interior (Recraft leaves it at alpha 254) to 255.
3. De-fringe: semi-transparent edge pixels still carry the white studio
   sweep blended in, which shows as a light halo on dark sections. Each edge
   pixel is un-blended against the measured backdrop: F = (C - (1-a)B) / a.
4. Over-caps (100 and 250 mL): Recraft treats the clear/smoked cap as solid,
   so it renders milky on dark backgrounds. Inside the cap rows only, alpha
   is rebuilt by colour-to-alpha against the white backdrop, with a small
   floor so the cap still reads as a physical object. The black pump inside
   stays opaque because it is dark.
5. Shared scale: every bottle is resampled to 4.83 px/mm (the 250 mL's native
   density), so the three files sit side by side at true relative size when
   rendered at the same px-to-CSS ratio. The 500 mL is upscaled 1.15x (the
   only upscale), the 100 mL downscaled. Native-resolution "-hd" versions are
   kept for single-product use.
6. Bundles are composited locally from those cutouts with soft contact
   shadows. Nothing in them is generated.

    python3 cutouts.py
"""
import json
import os

import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CUT = os.path.join(HERE, "_raw", "cutouts")
OUT = os.path.join(ROOT, "site", "src", "assets", "img", "products")
os.makedirs(OUT, exist_ok=True)

SKUS = {
    # sku: (name, real height mm, cap region as fraction of bottle height or None)
    "100": ("travel", 135, 0.355),
    "250": ("pro", 195, 0.120),
    "500": ("coach", 210, None),
}
PX_PER_MM = 4.83


def clean(sku):
    name, mm, cap = SKUS[sku]
    src = np.array(Image.open(os.path.join(HERE, "_prompts", f"_ref_{sku}.png")).convert("RGB")).astype(np.float64) / 255
    a = np.array(Image.open(os.path.join(CUT, f"recraft_{sku}.png")).convert("RGBA"))[:, :, 3].astype(np.float64) / 255

    bg = np.median(src[a < 0.01].reshape(-1, 3), axis=0)
    a[a >= 250 / 255] = 1.0
    a[a < 0.03] = 0.0

    rgb = src.copy()
    edge = (a > 0) & (a < 1)
    ae = a[edge][:, None]
    rgb[edge] = np.clip((src[edge] - (1 - ae) * bg) / ae, 0, 1)

    ys, xs = np.where(a > 0.03)
    y0, y1 = ys.min(), ys.max()
    if cap:
        yc = y0 + int((y1 - y0) * cap)
        region = np.zeros_like(a, dtype=bool)
        region[:yc + 1] = a[:yc + 1] > 0
        c = np.clip(src[region] / bg, 0, 1)
        ac = 1 - c.min(axis=1)
        ac = np.maximum(ac, 0.12)
        # keep Recraft's outer silhouette edge softness
        a_new = np.minimum(ac, a[region])
        f = np.clip((c - (1 - a_new)[:, None]) / np.maximum(a_new, 1e-3)[:, None], 0, 1)
        a[region] = a_new
        rgb[region] = f * bg

    out = np.dstack([rgb, a])
    im = Image.fromarray((out * 255 + 0.5).astype(np.uint8))
    ys, xs = np.where(a > 0.03)
    pad = 6
    box = (max(xs.min() - pad, 0), max(ys.min() - pad, 0),
           min(xs.max() + pad + 1, im.width), min(ys.max() + pad + 1, im.height))
    hd = im.crop(box)
    native_px_per_mm = (ys.max() - ys.min()) / mm
    scale = PX_PER_MM / native_px_per_mm
    shared = hd.resize((round(hd.width * scale), round(hd.height * scale)), Image.LANCZOS)
    return name, hd, shared, mm, scale


def save(im, stem):
    im.save(os.path.join(OUT, stem + ".png"), optimize=True)
    im.save(os.path.join(OUT, stem + ".webp"), "WEBP", quality=90, method=6)


def shadow_layer(size, items, strength=0.55):
    """items: list of (cx, base_y, width). Soft elliptical contact shadows."""
    w, h = size
    sh = np.zeros((h, w), dtype=np.float64)
    yy, xx = np.mgrid[0:h, 0:w]
    for cx, by, bw in items:
        rx, ry = bw * 0.58, bw * 0.085
        d = ((xx - cx) / rx) ** 2 + ((yy - by) / ry) ** 2
        sh = np.maximum(sh, np.clip(1 - d, 0, 1) ** 1.2)
        rx2, ry2 = bw * 0.42, bw * 0.03
        d2 = ((xx - cx) / rx2) ** 2 + ((yy - by) / ry2) ** 2
        sh = np.maximum(sh, np.clip(1 - d2, 0, 1) * 1.0)
    alpha = Image.fromarray((np.clip(sh, 0, 1) * 255 * strength).astype(np.uint8))
    alpha = alpha.filter(ImageFilter.GaussianBlur(max(3, items[0][2] * 0.035)))
    layer = Image.new("RGBA", size, (6, 14, 10, 0))
    layer.putalpha(alpha)
    return layer


def darken(im, f):
    arr = np.array(im).astype(np.float64)
    arr[:, :, :3] *= f
    return Image.fromarray(arr.clip(0, 255).astype(np.uint8))


def bundle(bottle, rows, stem, spacing=1.30):
    """rows: back to front, each (count, scale, darken, y_lift_fraction, x_offset_fraction).
    Floor shadows for every row are laid down first, then bottles back to front,
    so no shadow ever lands on a bottle that stands behind it."""
    bw, bh = bottle.size
    body_w = bw * 0.94
    widest = max((n - 1 + abs(xoff)) * body_w * s * spacing + bw * s for n, s, _, _, xoff in rows)
    W = int(widest + bw * 0.8)
    H = int(bh * 1.6)
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    base_front = int(H - bh * 0.08)
    placed = []
    for n, s, dk, lift, xoff in rows:
        b = darken(bottle.resize((round(bw * s), round(bh * s)), Image.LANCZOS), dk)
        gap = body_w * s * spacing
        cx0 = W / 2 - gap * (n - 1) / 2 + xoff * gap / 2
        base = base_front - int(bh * lift)
        placed.append((b, dk, [(cx0 + i * gap, base - 2, b.width * 0.94) for i in range(n)]))
    for b, dk, items in placed:
        canvas.alpha_composite(shadow_layer((W, H), items, strength=0.5 * dk))
    for b, dk, items in placed:
        for cx, by, _ in items:
            canvas.alpha_composite(b, (int(cx - b.width / 2), int(by - b.height + 4)))
    arr = np.array(canvas)
    ys, xs = np.where(arr[:, :, 3] > 4)
    pad = int(bh * 0.04)
    canvas = canvas.crop((max(xs.min() - pad, 0), max(ys.min() - pad, 0),
                          min(xs.max() + pad, W), min(ys.max() + pad, H)))
    save(canvas, stem)
    return canvas.size


def main():
    meta = {}
    shared = {}
    for sku in SKUS:
        name, hd, sh, mm, scale = clean(sku)
        save(sh, f"bottle-{name}")
        save(hd, f"bottle-{name}-hd")
        shared[name] = sh
        meta[f"bottle-{name}"] = {"w": sh.width, "h": sh.height, "mm": mm, "px_per_mm": PX_PER_MM}
        meta[f"bottle-{name}-hd"] = {"w": hd.width, "h": hd.height, "mm": mm}
        print(f"{name}: shared {sh.size} (x{scale:.3f}), hd {hd.size}")

    meta["bundle-6"] = dict(zip(("w", "h"), bundle(shared["pro"], [
        (3, 0.88, 0.62, 0.09, 1.0),
        (3, 1.00, 1.00, 0.00, 0.0)], "bundle-6", spacing=1.32)))
    meta["bundle-12"] = dict(zip(("w", "h"), bundle(shared["pro"], [
        (6, 0.88, 0.62, 0.09, 1.0),
        (6, 1.00, 1.00, 0.00, 0.0)], "bundle-12", spacing=1.32)))
    meta["bundle-case"] = dict(zip(("w", "h"), bundle(shared["travel"], [
        (6, 0.80, 0.50, 0.19, 0.0),
        (6, 0.90, 0.70, 0.095, 1.0),
        (6, 1.00, 1.00, 0.00, 0.0)], "bundle-case", spacing=1.30)))
    json.dump(meta, open(os.path.join(CUT, "_meta.json"), "w"), indent=2)
    print(json.dumps(meta, indent=1))


if __name__ == "__main__":
    main()
