"""
Athlon Rub website: 2026 brand marks.

Builds every logo, emblem and icon the static site uses into
assets/athlon/2026/, from the official 2026 logo pack in
"Brand Elements/2026-rebrand" (Manuel Medina's shield with the diagonal gold
sash and star). Nothing here is drawn from the retired "A" crest system
(system-v2, 00_logo_*, 01-10_*).

Run from anywhere with a Python that has Pillow:

    /usr/bin/python3 "Brand Elements/build_site_marks_2026.py"

What it makes, and where the site uses it:

  logo-gold.png        Logo en Dorado, trimmed. Footer watermark (dark green).
  wordmark.svg         Fuente Dorada y Rub Verde, cropped. Header (white).
  wordmark-gold.svg    Fuente en Dorado, cropped. Spare for dark headers.
  emblem.png           Full-colour shield cut from Logo@3x.png.
  emblem-gold.svg      The shield as one flat #CA9A3A shape (vector, from
                       the single-colour logo's own path).
  favicon.png          Full-colour shield on a square transparent canvas.
  og.png               1200x630 social card: Logo en Dorado on #0E3D28.
  star-mark.svg        The star and sash line from inside the shield, flat
                       gold. Bullet / trust mark.
  star.svg             Plain five-point star, flat gold. Review ratings.
  rule.svg             The two tapered rules that flank RUB, closed up into
                       one marker. Card and persona marker.
  arrow-gold.svg       Tapered rule shaft with a chevron head. Links and
  arrow-green.svg      buttons (replaces the old triple chevron).
"""

import math
import os
import re

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, ".."))
PACK = os.path.join(HERE, "2026-rebrand")
OUT = os.path.join(REPO, "assets", "athlon", "2026")

GREEN = "#0E3D28"
GREEN_DARK = "#2F412F"
GOLD = "#CA9A3A"
COPPER = "#934E1F"

# The pack's artboards are 1087 units square; the @3x PNGs are 3262 px.
PNG_SCALE = 3262 / 1087

# Rows of the 3262 px logo PNGs that hold the shield (it sits above a
# transparent gap before the wordmark). Matches the Black Friday email build.
SHIELD_ROWS = {"Logo@3x.png": (217, 2010), "Logo en Dorado@3x.png": (372, 2170)}


def png(name):
    return Image.open(os.path.join(PACK, "png", name)).convert("RGBA")


def trim(img, pad=0):
    x0, y0, x1, y1 = img.getchannel("A").getbbox()
    return img.crop((max(x0 - pad, 0), max(y0 - pad, 0), x1 + pad, y1 + pad))


def save_png(img, name):
    path = os.path.join(OUT, name)
    img.save(path, "PNG", optimize=True)
    print(f"  {name:20s} {img.size[0]}x{img.size[1]}  {os.path.getsize(path) // 1024} KB")


def save_svg(text, name):
    path = os.path.join(OUT, name)
    with open(path, "w") as f:
        f.write(text)
    print(f"  {name:20s} {os.path.getsize(path) // 1024 or 1} KB")


def shield(name):
    im = png(name)
    y0, y1 = SHIELD_ROWS[name]
    return trim(im.crop((0, y0, im.width, y1)))


def recrop_svg(name, bbox_px, pad=4):
    """Return a pack SVG with its viewBox tightened to the artwork."""
    with open(os.path.join(PACK, "svg", name)) as f:
        svg = f.read()
    x0, y0, x1, y1 = (v / PNG_SCALE for v in bbox_px)
    x0, y0, x1, y1 = x0 - pad, y0 - pad, x1 + pad, y1 + pad
    w, h = x1 - x0, y1 - y0
    svg = svg.replace('viewBox="0 0 1087 1087"',
                      f'viewBox="{x0:.1f} {y0:.1f} {w:.1f} {h:.1f}" '
                      f'width="{w:.0f}" height="{h:.0f}"', 1)
    svg = re.sub(r"<!--.*?-->\s*", "", svg, flags=re.S)
    return svg


def blanco_paths():
    """Vector paths of the single-colour logo (Logo en Blanco.svg)."""
    with open(os.path.join(PACK, "svg", "Logo en Blanco.svg")) as f:
        svg = f.read()
    paths = re.findall(r'<path class="st0" d="([^"]+)"', svg)
    polys = re.findall(r'<polygon class="st0" points="([^"]+)"', svg)
    return paths, polys


# ---------------------------------------------------------------- logos
def build_logos():
    gold = trim(png("Logo en Dorado@3x.png"))
    gold.thumbnail((640, 640), Image.LANCZOS)
    save_png(gold, "logo-gold.png")

    word = png("Fuente Dorada y Rub Verde@3x.png")
    save_svg(recrop_svg("Fuente Dorada y Rub Verde.svg", word.getbbox()), "wordmark.svg")
    word = png("Fuente en Dorado@3x.png")
    save_svg(recrop_svg("Fuente en Dorado.svg", word.getbbox()), "wordmark-gold.svg")


def build_emblems():
    em = shield("Logo@3x.png")
    em.thumbnail((320, 320), Image.LANCZOS)
    save_png(em, "emblem.png")

    # favicon: shield centred on a square canvas
    fav = shield("Logo@3x.png")
    fav.thumbnail((176, 176), Image.LANCZOS)
    sq = Image.new("RGBA", (192, 192), (0, 0, 0, 0))
    sq.alpha_composite(fav, ((192 - fav.width) // 2, (192 - fav.height) // 2))
    save_png(sq, "favicon.png")

    # flat shield: the single-colour logo's own shield path, filled gold
    paths, _ = blanco_paths()
    d = paths[-1]
    save_svg(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="292 123 476 601" '
        'width="476" height="601">'
        f'<path fill="{GOLD}" d="{d}"/></svg>\n',
        "emblem-gold.svg",
    )


def build_og():
    W, H = 1200, 630
    card = Image.new("RGBA", (W, H), GREEN)
    logo = trim(png("Logo en Dorado@3x.png"))
    logo.thumbnail((520, 520), Image.LANCZOS)
    card.alpha_composite(logo, ((W - logo.width) // 2, (H - logo.height) // 2))
    path = os.path.join(OUT, "og.png")
    card.convert("RGB").save(path, "PNG", optimize=True)
    print(f"  {'og.png':20s} {W}x{H}  {os.path.getsize(path) // 1024} KB")


# ---------------------------------------------------------------- icons
def build_star_mark():
    # Subpath 3 of the shield path is the star with the thin sash line through
    # it (it is cut out of the gold band). Filled on its own, and cropped to a
    # short run of the line either side of the star, it becomes the mark.
    paths, _ = blanco_paths()
    subs = re.split(r"(?<=[Zz])(?=M)", paths[-1])
    star_line = subs[2]
    save_svg(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="437 392 197 147" '
        'width="197" height="147">'
        f'<path fill="{GOLD}" d="{star_line}"/></svg>\n',
        "star-mark.svg",
    )


def build_star():
    pts = []
    cx, cy, ro, ri = 50, 52, 48, 19.5
    for i in range(10):
        r = ro if i % 2 == 0 else ri
        a = -math.pi / 2 + i * math.pi / 5
        pts.append(f"{cx + r * math.cos(a):.2f},{cy + r * math.sin(a):.2f}")
    save_svg(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">'
        f'<polygon fill="{GOLD}" points="{" ".join(pts)}"/></svg>\n',
        "star.svg",
    )


def build_rule():
    # The two rules that flank RUB, from the single-colour logo, with the gap
    # where RUB sits closed up to a hairline. Drawn twice as tall as the logo's
    # proportion so the marker holds up at 60-90 px wide.
    _, polys = blanco_paths()
    rules = [p for p in polys if float(p.split()[1]) > 900]
    left, right = sorted(rules, key=lambda p: float(p.split()[0]))
    shift = 697.41 - 373.41 - 16  # pull the right rule in, leaving a 16-unit gap
    save_svg(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="89 925 581 21" '
        'width="581" height="42" preserveAspectRatio="none">'
        f'<polygon fill="{GOLD}" points="{left}"/>'
        f'<polygon fill="{GOLD}" transform="translate(-{shift:.2f} 0)" points="{right}"/>'
        "</svg>\n",
        "rule.svg",
    )


def build_arrow():
    # A tapered rule (point at the tail, full weight at the head, as in the
    # logo's rules) running into a chevron with the wordmark's slanted cuts.
    for name, colour in (("arrow-gold.svg", GOLD), ("arrow-green.svg", GREEN)):
        save_svg(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 32" width="64" height="32">'
            f'<g fill="{colour}">'
            '<polygon points="1,16 50,12.4 50,19.6"/>'
            '<polygon points="33,3 46,3 61,16 46,29 33,29 47,16"/>'
            "</g></svg>\n",
            name,
        )


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print(f"Writing to {os.path.relpath(OUT, REPO)}/")
    build_logos()
    build_emblems()
    build_og()
    build_star_mark()
    build_star()
    build_rule()
    build_arrow()
