# Athlon Rub

Brand asset repo for [Athlon Rub](https://athlonrub.com) — a next-generation
Thai-oil topical liniment for athletes. FDA-registered cosmetic, manufactured
in an FDA, ISO and GMP certified lab in the USA.

## What's in here

```
Athlon Rub/
├─ Home Page/
│  ├─ index.html              # The home page, single-file (HTML + embedded CSS)
│  └─ _extract_logo.py        # Pulls the primary logo out of the brand PDF
│                               and alpha-extracts it for web use
│
├─ Brand Elements/
│  ├─ 00_logo_full.png        # Primary brand lockup (shield + ATHLON RUB)
│  ├─ 00_logo_shield.png      # Shield crest only (no wordmark)
│  ├─ system-v2/              # CURRENT element system: 23 flat marks,
│  │                            4 colourways, 2K + web. See its README.
│  ├─ generate_flat_system.py # v2 generation pipeline
│  ├─ make_colorways.py       # v2 colourway + web export step
│  ├─ 01–10_*.png             # v1 accents (superseded, see note below)
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

## The home page

Single-file static landing page at `Home Page/index.html`. Open directly in
a browser — no build step. Loads Google Fonts (Oswald + Inter) and references
the PNGs in `Brand Elements/`. Section flow mirrors `tidl.com`:

```
nav → hero → credibility strip → clean-credentials chips → where to find us
→ persona grid → how-to-use → product grid → bundles → find-your-fit CTA
→ why it hits different → heritage band → reviews → stat band
→ featured product → FAQ → instagram feed → newsletter → footer
```

All copy stays inside Athlon Rub's FDA-cosmetic claim guardrails — no
*pain / heal / anti-inflammatory / treat / cure* language. Benefits framed
as what individual ingredients are known to do.

## Brand elements

The current system is **`Brand Elements/system-v2/`**: 23 flat single-colour
marks in four colourways, documented in
[`system-v2/README.md`](Brand%20Elements/system-v2/README.md).

- **Tier 1, crest system (01–10).** Crest frame and icon, star, apex monogram,
  ascend and forward chevrons, support rules, laurel, ribbon, star divider.
- **Tier 2, benefit icons (11–18).** Fast-absorbing, warming, non-greasy,
  botanical, lab-certified, tested-clean, heritage motif, spray bottle.
- **Tier 3, persona icons (19–23).** One per persona tile: combat, endurance,
  lifting, paddle, therapist.

### On v1 (`01`–`10_*.png`)

The v1 elements are kept for reference but should not be used in new work.
They were rendered with bevels, drop shadows and a metallic finish, which the
logo sheet's USOS NO PERMITIDOS panel forbids (`No aplicar efectos`), and
which matches nothing else in the brand: every icon on the bottle label and
every attribute mark on the logo sheet is flat and single-colour. v1's shield
was also a generic heater shield rather than the Lumpini belt-buckle crest
that the Master Brain identifies as brand IP.

`Home Page/index.html` still references v1. Swapping it to v2 is a separate
task.

## Regenerating elements

Set your kie.ai API key:

```bash
export KIE_API_KEY=your_key_from_kie_ai
```

Then:

```bash
# Generate all 23 v2 elements (writes to Brand Elements/system-v2/gold/)
python3 "Brand Elements/generate_flat_system.py"

# Regenerate only specific elements by id
python3 "Brand Elements/generate_flat_system.py" 04 16

# Rebuild PNGs from cached raw output, no API calls and no cost
python3 "Brand Elements/generate_flat_system.py" --reprocess

# Derive the green / cream / white colourways and the 512px web exports
python3 "Brand Elements/make_colorways.py"

# Re-extract the logo from the brand PDF
python3 "Home Page/_extract_logo.py"

# Lifestyle photography: all 24, one set, or named shots
python3 "Lifestyle Photos/generate_lifestyle.py"
python3 "Lifestyle Photos/generate_lifestyle.py" A
python3 "Lifestyle Photos/generate_lifestyle.py" A03 B07
```

The generation pipeline is: API submission → polling → download →
black-to-alpha conversion → flatten to exact `#D4AF37` → auto-crop → QA
composite onto green and cream. `make_colorways.py` then swaps RGB while
preserving alpha, so every colourway keeps identical anti-aliased edges.

Model is `nano-banana-pro` via kie.ai. The prompt technique, including the
two failure modes specific to this set, is documented in
[`ELEMENT_GENERATION_GUIDE.md`](ELEMENT_GENERATION_GUIDE.md) and
[`system-v2/README.md`](Brand%20Elements/system-v2/README.md).

## Brand palette

Official values, sampled from PALETA PRINCIPAL on the logo sheet.

| Token | Official hex | Use |
|---|---|---|
| Green | `#0F2B1E` | Primary surface: nav, hero, heritage band |
| Gold  | `#D4AF37` | Primary accent: buttons, dividers, stars, all elements |
| Black | `#0A0A0A` | Body text, deep surfaces |
| Cream | `#EAE9CB` | Light backgrounds |

The home page currently ships slightly different values, carried over from
before the logo sheet was available: `--green: #0F2F2F`, `--gold: #D9AF37`,
`--ink: #0B1A1A`. The v2 elements are rendered in the official `#D4AF37`, so
aligning the CSS tokens to the table above is worth doing in one pass.

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
