# Athlon Rub

Brand asset repo for [Athlon Rub](https://athlonrub.com), a next-generation
Thai-oil topical liniment for athletes. FDA-registered cosmetic, manufactured
in an FDA, ISO and GMP certified lab in the USA.

## What's in here

```
Athlon Rub/
├─ index.html                 # Website home page (static rebuild)
├─ pages/, collections/       # Supporting pages and the shop page
├─ css/athlon-brand.css       # Brand layer: 2026 palette tokens + re-skin rules
├─ assets/athlon/2026/        # Every logo, emblem and icon the site uses
│
├─ Home Page/
│  └─ _extract_logo.py        # Pulled the retired pre-2026 logo out of the
│                               old brand PDF (kept for reference)
│
├─ Brand Elements/
│  ├─ 2026-rebrand/           # CURRENT: the official 2026 logo pack
│  │                            (svg/, png/, badges/, Palette 2026.pdf,
│  │                            Logo Versions 2026.pdf)
│  ├─ build_site_marks_2026.py # Builds assets/athlon/2026/ from that pack
│  ├─ 00_logo_full.png        # Retired pre-2026 lockup ("A" crest)
│  ├─ 00_logo_shield.png      # Retired pre-2026 crest
│  ├─ system-v2/              # Retired element system built on the "A"
│  │                            crest: 23 flat marks. Do not use.
│  ├─ generate_flat_system.py # v2 generation pipeline (retired)
│  ├─ make_colorways.py       # v2 colourway + web export step (retired)
│  ├─ 01–10_*.png             # v1 accents (retired)
│  ├─ generate_elements.py    # v1 generation pipeline
│  └─ regenerate_three.py     # v1 retry script
│
├─ ELEMENT_GENERATION_GUIDE.md  # Reusable methodology (alpha extraction,
│                                 prompt formula, content-filter pitfalls)
│
├─ Lifestyle Photos/
│  ├─ athletes/               # Set A: 12 athlete action shots, no product
│  ├─ product/                # Set B: 12 of the same world, product in frame
│  ├─ _style.py               # Shared photographic system (camera, light,
│  │                            grade, skin realism, capture, negatives)
│  ├─ _scenes_athletes.py     # Set A scene manifest
│  ├─ _scenes_product.py      # Set B scenes + per-SKU scale, label, integration
│  ├─ generate_lifestyle.py   # Generation pipeline
│  └─ README.md               # Brief, dimensions and regeneration notes
│
├─ Product Photos/
│  └─ New product photos/     # Current pack shots, 100 / 250 / 500 ml
│
├─ New Logo Athlon Rub Cinturon.pdf  # Brand logo system / guidelines
│
└─ .gitignore                # Excludes the Master Brain docs (sensitive)
```

## The website

Static site at the repo root (`index.html`, `pages/*/index.html`,
`collections/all/index.html`), served as-is by GitHub Pages with no build
step. `css/athlon-brand.css` is the brand layer loaded last; its `:root`
block holds the 2026 palette tokens.

All copy stays inside Athlon Rub's FDA-cosmetic claim guardrails: no
*pain / heal / anti-inflammatory / treat / cure* language. Benefits framed
as what individual ingredients are known to do.

## Brand elements

The current identity is the **2026 rebrand** in
`Brand Elements/2026-rebrand/`: Manuel Medina's shield with a diagonal gold
sash and star, ATHLON in brushed gold, RUB between two tapered gold rules.
Everything the website shows is built from that pack by
`Brand Elements/build_site_marks_2026.py` into `assets/athlon/2026/`:

| File | What it is | Where the site uses it |
|---|---|---|
| `wordmark.svg` | Fuente Dorada y Rub Verde (vector) | Header, mobile drawer (white) |
| `logo-gold.png` | Logo en Dorado | Footer watermark (dark green) |
| `emblem.png` | Full-colour shield, cut from Logo@3x.png | Footer AdChoices link |
| `favicon.png` | Full-colour shield, square | Favicon, touch icon |
| `og.png` | Logo en Dorado on `#0E3D28`, 1200x630 | Social share card |
| `star-mark.svg` | The star and sash line from inside the shield | Trust bar, ingredient rings, checklists, ingredient chips |
| `rule.svg` | The two tapered rules that flank RUB | Persona cards, benefit and contact cards |
| `arrow-gold.svg`, `arrow-green.svg` | Tapered rule into a chevron | Text links, carousel arrows, newsletter button |
| `star.svg` | Plain five-point star | Review ratings |
| `emblem-gold.svg`, `wordmark-gold.svg` | Flat gold shield; gold wordmark | Spares for dark surfaces |

Icons with no 2026 equivalent (benefit pictograms, persona silhouettes, the
spray and absorb step icons) were retired rather than redrawn: the routine
steps are numbered and the cards carry the logo's rule. Of the certification
badges in `2026-rebrand/badges/`, only Made in USA and BPA Free are confirmed
claims.

Rebuild after changing the pack:

```bash
/usr/bin/python3 "Brand Elements/build_site_marks_2026.py"
```

### Retired: system-v2 and the "A" crest

`Brand Elements/system-v2/` and `00_logo_*` belong to the pre-2026 "A" apex
crest identity. They are kept for reference only; nothing on the website uses
them.

### On v1 (`01`–`10_*.png`)

The v1 elements are kept for reference but should not be used in new work.
They were rendered with bevels, drop shadows and a metallic finish, which the
logo sheet's USOS NO PERMITIDOS panel forbids (`No aplicar efectos`), and
which matches nothing else in the brand: every icon on the bottle label and
every attribute mark on the logo sheet is flat and single-colour. v1's shield
was also a generic heater shield rather than the Lumpini belt-buckle crest
that the Master Brain identifies as brand IP.

## Regenerating elements

The 2026 website marks need no API: see the rebuild command under Brand
elements. For the retired v2 pipeline and the lifestyle photography, set your
kie.ai API key:

```bash
export KIE_API_KEY=your_key_from_kie_ai
```

Then:

```bash
# Retired v2 system, kept for reference: generate all 23 v2 elements
# (writes to Brand Elements/system-v2/gold/)
python3 "Brand Elements/generate_flat_system.py"

# Regenerate only specific elements by id
python3 "Brand Elements/generate_flat_system.py" 04 16

# Rebuild PNGs from cached raw output, no API calls and no cost
python3 "Brand Elements/generate_flat_system.py" --reprocess

# Derive the green / cream / white colourways and the 512px web exports
python3 "Brand Elements/make_colorways.py"

# Re-extract the retired pre-2026 logo from the old brand PDF
python3 "Home Page/_extract_logo.py"

# Lifestyle photography: all 24, one set, or named shots
python3 "Lifestyle Photos/generate_lifestyle.py"
python3 "Lifestyle Photos/generate_lifestyle.py" A
python3 "Lifestyle Photos/generate_lifestyle.py" A03 B07
```

The (retired) v2 generation pipeline is: API submission → polling → download →
black-to-alpha conversion → flatten to exact `#D4AF37` → auto-crop → QA
composite onto green and cream. `make_colorways.py` then swaps RGB while
preserving alpha, so every colourway keeps identical anti-aliased edges.

Model is `nano-banana-pro` via kie.ai. The prompt technique, including the
two failure modes specific to this set, is documented in
[`ELEMENT_GENERATION_GUIDE.md`](ELEMENT_GENERATION_GUIDE.md) and
[`system-v2/README.md`](Brand%20Elements/system-v2/README.md).

## Brand palette

The 2026 palette, from `Brand Elements/2026-rebrand/Palette 2026.pdf`. These
are the `:root` tokens in `css/athlon-brand.css`.

| Token | Hex | Use |
|---|---|---|
| `--athlon-green` | `#0E3D28` | Primary surface: hero bands, trust bar, routine block |
| `--athlon-green-dark` | `#2F412F` | Second dark surface: footer, heritage band |
| `--athlon-gold` | `#CA9A3A` | Primary accent: buttons, rules, stars, every flat mark |
| `--athlon-copper` | `#934E1F` | Deep accent; mixed into `--athlon-gold-dim` for hover and small gold type |
| `--athlon-gold-metal` | `#f8da88` `#af9253` `#ca9a3a` `#f3c663` `#976b33` `#936731` | The logo's brushed-gold gradient |

Neutrals sit outside the palette sheet: ink `#0A0A0A` and the ivory light
surface `#F5F0E6` (the same ivory the 2026 Black Friday email uses).

## Compliance notes

Athlon Rub is registered with the FDA as a cosmetic product, **not** as an
over-the-counter drug. The website may not claim pain relief, anti-inflammatory
effect, healing, treatment, prevention, or cure of any condition. Approved
claim families: warming sensation, fast-absorbing, supports the body's natural
recovery process, prepares the body for activity, time-tested heritage. When
adding new copy, default to ingredient-led framing (*"Wintergreen, an ingredient
in Athlon Rub, is widely recognized for its warming properties"*) rather than
product-claim framing.

---

© Athlon Rub. External use only.
