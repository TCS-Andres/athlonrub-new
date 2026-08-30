# Athlon Rub — Brand Element System v2

23 flat, single-colour brand marks built to the official logo sheet
(`New Logo Athlon Rub Cinturon.pdf`). Four colourways, transparent PNG,
2K masters plus 512px web exports.

---

## Why v2 replaces v1

The v1 elements (`Brand Elements/01`–`10_*.png`) were rendered as beveled,
drop-shadowed, metallic graphics. Three problems:

1. **They break a stated brand rule.** The logo sheet's USOS NO PERMITIDOS
   panel forbids `No aplicar efectos`, and shows a glow/bevel treatment
   crossed out. v1 applied exactly that treatment to every element.
2. **They do not match the product.** Every icon on the bottle label is
   flat, solid, single-colour gold. So are the four brand attribute marks
   (PROTECCIÓN, EXCELENCIA, RENDIMIENTO, SUPERACIÓN) on the logo sheet.
   v1 was the only place in the brand where bevels existed.
3. **The shield was the wrong shield.** v1's `03_shield_outline_frame` is a
   generic heater shield. The real crest is a Muay Thai belt-buckle silhouette
   derived from the Lumpini Stadium buckle, which the Master Brain names as
   meaningful brand IP. v2 rebuilds it correctly.

v2 also extends the system from 10 decorative accents to a working website
icon set: crest system, benefit icons, and one icon per audience persona.

---

## Palette

Sampled from PALETA PRINCIPAL on the logo sheet. Note these are the official
values and they differ slightly from what the current home page uses.

| Token | Official | Currently on site | Use |
|---|---|---|---|
| Green | `#0F2B1E` | `#0F2F2F` | Primary surface |
| Gold | `#D4AF37` | `#D9AF37` | Primary accent, default element colour |
| Black | `#0A0A0A` | `#0B1A1A` | Type, deep surfaces |
| Cream | `#EAE9CB` | `#EAE9CB` | Light surface |

Every element in v2 is rendered in exact `#D4AF37`. The recolour step swaps
RGB and preserves alpha, so all four colourways share identical edges.

---

## The set

### Tier 1 — Crest system (01–10)

| # | Element | Use |
|---|---|---|
| 01 | `crest_outline` | Hollow crest frame. Product cards, avatar frames, badge containers |
| 02 | `crest_icon` | Full crest reduced to one flat colour. Favicon, stamp, seal, app tile |
| 03 | `star_excellence` | Star ratings, credential badges, step numbers, list bullets |
| 04 | `apex_monogram` | The A summit mark. Card watermark, section anchor, loader |
| 05 | `chevron_ascend` | SUPERACIÓN. Scroll-to-top, progress, tier markers |
| 06 | `chevron_forward` | CTAs, forward motion, carousel arrows, FAQ toggles |
| 07 | `support_rules` | Mirrored tapered rules that flank a wordmark or a caption |
| 08 | `laurel_open` | Heritage band, awards, testimonial framing |
| 09 | `ribbon_banner` | "Best value" / "Most popular" product labels |
| 10 | `star_rule_divider` | Section dividers between content blocks |

### Tier 2 — Benefit and product icons (11–18)

| # | Element | Use |
|---|---|---|
| 11 | `fast_absorbing` | Absorbs in about a minute |
| 12 | `warming` | Warming sensation |
| 13 | `non_greasy` | Non-greasy, does not transfer to clothing |
| 14 | `botanical_leaf` | Herbal formulation, paraben-free chips |
| 15 | `lab_certified` | FDA-registered, ISO and GMP certified lab |
| 16 | `tested_clean` | Tested clean, free of banned substances |
| 17 | `heritage_motif` | Thai heritage band, story sections |
| 18 | `spray_bottle` | How-to-use steps, format indicator |

### Tier 3 — Persona icons (19–23)

One per persona tile on the home page.

| # | Element | Persona |
|---|---|---|
| 19 | `persona_combat` | Combat Sports |
| 20 | `persona_endurance` | Soccer & Endurance |
| 21 | `persona_lifting` | Hyrox & Lifting |
| 22 | `persona_paddle` | Pickleball & Paddle |
| 23 | `persona_therapist` | Therapists & Bodyworkers |

---

## Folders

```
system-v2/
├─ gold/    2K masters, #D4AF37          ← the source of truth
├─ green/   2K, #0F2B1E                  ← for cream and white surfaces
├─ cream/   2K, #EAE9CB                  ← for green and black surfaces
├─ white/   2K, #FFFFFF                  ← for photography and video
├─ web/     512px gold, optimised        ← drop straight into the site
├─ _raw/    unprocessed API output       ← keep for reprocessing
└─ _qa/     composites on green + cream  ← visual check
```

Use `web/` on the site. Use the 2K colourways for print, packaging, social
templates, and anything that scales.

---

## Usage rules

**Do**
- Use gold on green, black, or photography. Use green on cream or white.
- Keep clear space around any element equal to 25% of its height.
- Size persona and crest marks at 48px or larger; they carry interior detail.
- Recolour only to the four palette values above.

**Do not**
- Add a bevel, gradient, drop shadow, glow, or outer stroke. This is the rule
  v1 broke and the reason the set was rebuilt.
- Stretch an element non-proportionally.
- Place gold on cream at body-text sizes; contrast is too low. Use green.
- Rotate the crest, the monogram, or the star.
- Mix v1 and v2 elements in the same composition.

---

## Contrast

Measured, not estimated.

| Pairing | Ratio | Verdict |
|---|---|---|
| Gold `#D4AF37` on green `#0F2B1E` | 7.21:1 | AAA |
| Gold `#D4AF37` on black `#0A0A0A` | 9.42:1 | AAA |
| Green `#0F2B1E` on cream `#EAE9CB` | 12.29:1 | AAA |
| Cream `#EAE9CB` on green `#0F2B1E` | 12.29:1 | AAA |
| White `#FFFFFF` on green `#0F2B1E` | 15.17:1 | AAA |
| Gold `#D4AF37` on cream `#EAE9CB` | 1.70:1 | Fails. Decorative only, never for text or UI |

Icons carrying meaning need a text label beside them regardless of pairing.

---

## Regenerating

```bash
export KIE_API_KEY=your_key_from_kie_ai

python3 "Brand Elements/generate_flat_system.py"           # all 23
python3 "Brand Elements/generate_flat_system.py" 04 16     # a subset
python3 "Brand Elements/generate_flat_system.py" --reprocess   # no API calls
python3 "Brand Elements/make_colorways.py"                 # colourways + web
```

Model: `nano-banana-pro` via kie.ai. Technique follows
`ELEMENT_GENERATION_GUIDE.md`: generate on solid black, recover alpha by
un-premultiplying, auto-crop.

Two things learned building v2, both now handled in the script:

- **The model drifts to a white background** when the prompt leads with
  "flat vector icon". Roughly a third of the first batch came back on white,
  which silently breaks alpha extraction. Fixed by putting the black-backdrop
  instruction first *and* repeating it as a final line (`BLACK_TAIL`), plus a
  light-background fallback path in `black_to_alpha`.
- **Never name a thing you do not want drawn.** Describing the gap in
  `07_support_rules` as the place "where the wordmark sits" made the model
  draw a garbled wordmark. Describe geometry, not purpose.
