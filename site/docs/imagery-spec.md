# Imagery spec, Athlon Rub site v3

Owner of record for every photograph on the v3 site. Generated with
**Seedream 5.5** (`seedream/5-5-image-to-image` with the real bottle photos as
references whenever a bottle is in frame, `seedream/5-5-text-to-image`
otherwise) through the Kie.ai task API. Key lives in the repo-root `.env`
(gitignored). Pipeline and prompts live in `Lifestyle Photos/2026-site/`.

## Look: "Corner-side cinematic"

A premium campaign, not stock. Think fight-night photography crossed with a
fragrance or spirits campaign.

- **Camera:** full-frame cinema camera (ARRI Alexa 35 class), 35/50/85 mm
  primes, wide open, shallow depth of field, natural lens falloff, fine
  organic film grain. Never "digital clean".
- **Light:** one motivated warm key (tungsten practical, low sodium overhead,
  or a soft window), a separating rim, dense shadows that fall to a true black.
  No golden-hour sunbeams, no HDR.
- **Grade:** shadows sit in deep forest green (brand `#0E3D28` family, never
  teal), highlights warm amber and gold (brand `#CA9A3A` family), skin true to
  life. Low saturation outside the green and amber.
- **The bottle is the hero.** When it is in frame it is sharp, backlit or
  rim-lit so the amber body glows like liquid gold, label legible at the
  crest, `ATHLON`, `RUB` and `ALL - SPORTS RUB` only. Everything smaller on
  the label blurs the way a real lens would. Never invent label text.
- **Real places, kept well.** Taut canvas, swept floors, racked plates,
  clean towels. No derelict warehouses, no peeling paint.
- **Real people.** Mixed casting across gender, age, ethnicity and build.
  Pores, sweat that obeys gravity, wraps that are actually worn.

## Product truths (from earlier client corrections, non-negotiable)

1. **It is an oil, not a spray.** The pump pushes a dense amber oil into the
   palm, then it is rubbed in. No mist, no spray cone, no airborne droplets.
2. **Very little oil.** Already rubbed in: a light satin sheen on the muscle
   belly, surrounding skin matte. No syrupy slick, no pooling, no pour.
3. **Bottles render small.** Err small, never large.

| SKU | Height | Diameter | Scale anchor | Closure |
|---|---|---|---|---|
| Travel 100 mL / 3.4 fl oz | 135 mm | 46 mm | shorter than a phone, hides in a fist | black pump + smoke over-cap |
| Pro 250 mL / 8.5 fl oz | 195 mm | 52 mm | about 1.3 phone lengths | black pump + clear over-cap |
| Coach 500 mL / 17 fl oz | 210 mm | 82 mm | full hand to wrap, wine-bottle heft | black ribbed screw cap, **no pump** |

## Compliance

Scenes are warm-up, training, performance and recovery. Nothing shows an
injury, a medical setting, a brace, ice packs or treatment. Therapist scenes
are sports massage on a clean table, not a clinic. No AI image is ever
presented as a specific real customer, athlete, staff member or facility.
Testimonials use real photos only.

## Shot list

All saved under `site/src/assets/img/scenes/` as WebP, two widths:
`{name}-lg.webp` and `{name}-sm.webp`. Landscape lg = 2400 w, sm = 1200 w.
Portrait and square lg = 1600 w, sm = 800 w.

| Name | Ratio | Bottle | Use on site | Brief |
|---|---|---|---|---|
| hero-desktop | 16:9 | Pro | Home hero | Dim, clean Muay Thai gym at night. Pro bottle sharp in the lower right third on the ring apron, backlit, glowing amber. Behind it, soft focus, a fighter seated in the corner while a cornerman's hands work oil into his shoulder. Left half dark and quiet for headline type. |
| hero-mobile | 9:16 | Pro | Home hero, phones | Same scene composed vertically. Bottle sharp in the lower third, fighter soft above, top third dark for headline type. |
| product-stage | 16:9 | Pro | "Working liniment" feature, product page | Still life. Pro bottle on a dark green-black stone plinth, backlit so the amber glows, gold rim light, two or three small beads of amber oil on the stone, arnica flowers and a cut Thai Plai root soft in the background. Negative space left. |
| product-trio | 3:2 | All three | Shop hero, lineup | Still life. Travel, Pro and Coach together on the same plinth at true relative scale (Coach widest, Pro tallest pump, Travel smallest). Same light as product-stage. |
| roster-combat | 3:4 | Travel or Pro | Roster card | Muay Thai fighter wrapping hands on a bench, bottle beside the wraps. |
| roster-endurance | 3:4 | Travel | Roster card | Runner or soccer player at the edge of a track at dusk, working oil into a calf, bottle on the track kerb. |
| roster-lifting | 3:4 | Pro | Roster card | HYROX or barbell athlete, chalked hands, working a shoulder, bottle on a bumper plate. Clean strength gym. |
| roster-paddle | 3:4 | Travel | Roster card | Pickleball player courtside working a forearm, paddle and bottle on the bench. Indoor or covered court. |
| roster-therapist | 3:4 | Coach | Roster card | Sports massage therapist's hands working a quad on a clean treatment table, Coach bottle on the table edge. |
| use-warmup | 3:4 | Pro | Uses band, Warm-Up page | Before the session: athlete pumping a small amount of oil into an open palm, gym soft behind. |
| use-performance | 3:4 | Pro | Uses band, Performance page | Between rounds: fighter on the corner stool, cornerman re-applying to the shoulder, bottle on the apron. |
| use-recovery | 3:4 | Coach or Pro | Uses band, Recovery page | After the session: athlete on a locker-room bench, towel over neck, working a calf, bottle beside. Calm, cooler key. |
| ingredient-arnica | 1:1 | none | Formula cards | Arnica montana flowers on dark stone, one bead of amber oil, side light. |
| ingredient-plai | 1:1 | none | Formula cards | Thai Plai (Zingiber cassumunar) rhizome, one cut to show the yellow interior, dark stone, amber bead. |
| ingredient-turmeric | 1:1 | none | Formula cards | Fresh turmeric roots, one split showing orange flesh, dark stone. |
| ingredient-wintergreen | 1:1 | none | Formula cards | Wintergreen leaves and red berries, dark stone, amber bead. |
| oil-macro | 16:9 | none | Formula hero, science band | Extreme macro of a single drop of amber oil on skin, light passing through it, pores visible, satin sheen around it. |
| step-shake | 3:2 | Pro | How-to step 1 | Two hands shaking the Pro bottle, slight motion blur at the edges, bottle label readable. |
| step-pump | 3:2 | Pro | How-to step 2 | One press of the pump into an open palm, a coin-sized pool of dense amber oil. |
| step-rub | 3:2 | none | How-to step 3 | Palm heel driving up a calf, skin dragging under pressure, light satin sheen. |
| heritage-camp | 16:9 | none | Story page, heritage band | Traditional open-air Muay Thai camp in Thailand, early morning haze, wooden ring, heavy bags, clean. No people or distant small figures only. |
| cta-locker | 21:9 | Pro | Closing CTA band | Low-light locker room, athlete taping hands on a bench, Pro bottle sharp on the bench in the foreground. |
| pdp-travel-bag | 3:4 | Travel | Travel product page | Open gym duffel with gloves and wraps, Travel bottle tucked in the side pocket. |

## Product cutouts

Clean transparent PNGs of the three real product photos replace the old,
rough cutouts. Saved to `site/src/assets/img/products/`:

- `bottle-travel.png`, `bottle-pro.png`, `bottle-coach.png`: transparent,
  trimmed to the bottle, no halo, semi-transparent over-caps kept
  semi-transparent, label pixels untouched, all three on a shared scale
  (1 px = same mm) so they can sit side by side at true relative size.
- `bundle-6.png`, `bundle-12.png`, `bundle-case.png`: composites built from
  the cutouts (not generated), with soft contact shadows.
- Each also as `.webp`.

## Manifest

`site/src/_data/images.json` maps each name to `{ alt, w, h }` (lg size), so
templates pull alt text and dimensions from one place.
