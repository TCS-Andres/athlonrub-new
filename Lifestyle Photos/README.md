# Lifestyle Photography

Two sets of 12 square photographs generated with `nano-banana-pro` via kie.ai.

| Set | Folder | What it is |
|---|---|---|
| A | `athletes/` | 12 athlete action shots, no product in frame |
| B | `product/` | 12 shots of the same world with an Athlon Rub bottle in frame |

All 24 are 1:1, 2K, JPG.

## Sport coverage

Set A spans the full all-sports claim rather than leaning on one discipline:
Muay Thai, boxing, soccer, gymnastics, sprinting, distance running, Olympic
weightlifting, Brazilian jiu-jitsu, basketball, volleyball, tennis and road
cycling. Set B revisits the same disciplines with the product present.

Swimming was cut after the first pass: a water sport is the wrong read for a
topical oil. Indoor volleyball took its slot and keeps the court coverage.

Casting is deliberately mixed across gender, age, body type and ethnicity, so
the set reads as a real roster instead of one model in twelve outfits.

## The brief, and how the prompts serve it

The controlling requirement was that the output must not read as AI. Three
files carry that:

- **`_style.py`** — the photographic system. Camera and aperture, a single
  soft overcast window source with an uncorrected shadow side, a muted
  neutral-cool grade with dense blacks, then the long realism block (pores,
  asymmetry, blemishes, sweat that obeys gravity, fabric that creases, a room
  that is worn), capture artefacts (grain, vignetting, chromatic aberration),
  and a negative block that names specific failure modes rather than gesturing
  at "realistic".
- **`_scenes_athletes.py`** — Set A scenes. Each names who, what they are
  doing, where, and what the camera is doing. Nothing more; the style block
  carries the look.
- **`_scenes_product.py`** — Set B. Adds three blocks the product shots need:
  per-SKU **scale** (hard dimensions *plus* a hand anchor, because the model
  reasons about size far better from "spans the palm to past the fingertips"
  than from millimetres), the **label** description, and an **integration**
  block that forces shared lighting, a grounded contact shadow and real wear,
  because the composited-packshot look is the giveaway on product-in-scene.

Reference photographs of each bottle are attached to every Set B request as
`image_input`, so the label is copied rather than invented.

### Three client corrections, and where they live

1. **Clean facilities, not derelict ones.** The first pass read as condemned
   warehouses — peeling paint, cracked concrete, duct-taped bags. The athletes
   train in well-kept rings, halls and courts. The `THE FACILITY IS CURRENT,
   CLEAN AND WELL MAINTAINED` clause in `_style.py` now names the wanted
   details (taut canvas, swept floors, racked plates) *and* the unwanted ones,
   because "clean" alone was too weak to move it. Street and outdoor settings
   still appear — road running, the climb, the neighbourhood court — in good
   repair.
2. **It is an oil, not a spray.** The pump pushes out a dense amber serum that
   gets poured into the palm and rubbed into the muscle. The `OIL` block in
   `_scenes_product.py` forbids spray cones, atomised mist and airborne
   droplets outright, and every Set B scene now shows the *rub* — a palm heel
   driving down a muscle, a thumb drawing along a forearm, skin dragging under
   the pressure.
3. **Oil, but far less of it.** Telling the model "oil" worked too well on the
   first attempt: limbs came back varnished in what looked like syrup. The
   `OIL` block now leads its second half with `USE VERY LITTLE OIL` and names
   the over-application failures directly — no syrupy slick, no laminated
   coating, no liquid running or pooling on a limb, no poured stream in
   mid-air. The read to aim for is *already rubbed in*: a light satin sheen
   along the muscle belly with the surrounding skin still matte.
4. **The bottles were rendering too big.** The error was one-directional every
   time, so the correction is too: each SKU carries a phone anchor and a hand
   anchor alongside its millimetres, and `SCALE_BIAS` tells the model outright
   that this is the failure mode and to err small. Several scenes also pin the
   size against a prop already in frame ("only a little taller than a glove is
   long", "the helmet dwarfs it").

### Two rules learned from the pilot

1. **Fine print.** The first pass rendered the label's five-point bottom panel
   as convincing-looking gibberish. The `FINE PRINT RULE` in `_scenes_product.py`
   now permits only the crest, `ATHLON`, `RUB` and `ALL - SPORTS RUB` to render
   legibly and requires everything smaller to blur the way a real 85mm lens
   would. Unreadable is correct; invented lettering is not.
2. **Grade and light.** "Gently lifted blacks, low contrast" produced washed,
   flat frames, and "window light" alone let the model reach for golden-hour
   sunbeams. Both are now pinned: overcast, no direct sun, dense shadows to a
   true black point.

## Bottle dimensions used

Reference values in the prompts, paired with a body-scale anchor so the model
gets the proportion right against a human.

| SKU | Height (with closure) | Diameter | Anchor |
|---|---|---|---|
| 100 ml / 3.4 fl oz | 135 mm (5.3 in) | 46 mm (1.8 in) | Shorter than a phone; hides in a closed fist |
| 250 ml / 8.5 fl oz | 195 mm (7.7 in) | 52 mm (2.0 in) | ~1⅓ phone lengths; a hand covers half its height |
| 500 ml / 17 fl oz  | 210 mm (8.3 in) | 82 mm (3.2 in) | Full hand to wrap, wine-bottle heft |

When in doubt the prompts render smaller, not larger.

The 100 ml and 250 ml are amber PET with a black pump and a smoke over-cap.
The 500 ml is an amber boston round with a black ribbed screw cap and **no
pump** — worth remembering when briefing new shots. The pump dispenses oil, not
mist; nothing in this system should ever be described as a spray.

## Regenerating

```bash
export KIE_API_KEY=your_key_from_kie_ai

python3 "Lifestyle Photos/generate_lifestyle.py"           # all 24
python3 "Lifestyle Photos/generate_lifestyle.py" A         # set A only
python3 "Lifestyle Photos/generate_lifestyle.py" B         # set B only
python3 "Lifestyle Photos/generate_lifestyle.py" A03 B07   # named shots
python3 "Lifestyle Photos/generate_lifestyle.py" --prompts # dry run, no cost
```

Note: the API advertises a 20,000-character prompt limit but intermittently
rejects submissions at around a third of that, on prompts whose siblings pass at
the same length. Submissions are retried up to three times before the rejection
is believed.

Every run writes the exact prompt for each shot to `_prompts/`. Those text
files are the real asset: a frame that misses gets re-run from an edited
prompt, not rebuilt from scratch. Bottle reference URLs are cached in
`_refs.json`, so reruns do not re-upload.

## Compliance

These are lifestyle images, not claims. Scenes are framed as warm-up,
training and recovery. Nothing depicts Athlon Rub treating an injury or a
medical condition, in line with the FDA cosmetic guardrails in the root
`README.md` — no pain, healing, anti-inflammatory, treatment or cure framing,
in the image or in any caption written against it.
