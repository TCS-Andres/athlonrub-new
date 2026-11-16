# Design system, Athlon Rub v3

All values live as tokens at the top of `src/assets/css/main.css`. Add a token
before using a new value.

## Brand DNA, taken from the 2026 logo

| Logo element | Where it shows up on the site |
|---|---|
| The tapered gold rules that flank **RUB** | Every eyebrow label (`.eyebrow`), stat and shelf rules |
| The diagonal **sash** across the shield (about 20 degrees, rising left to right) | The chamfered corner on buttons, cards and images (`.chamfer`), and the short diagonal accent stroke inside every icon |
| The **star** on the sash | List bullets (`.star-list`), announcement marker |
| The brushed **metallic gold** | `--gold-gradient` on the hero's second line, stats, shelf lines and button hover |
| The shield's **deep green field** | `--green-950` and `.surface-field`, the dark sections |
| The white bottle label | `--paper` light sections |

## Colour

Official (Palette 2026.pdf): green `#0E3D28`, dark green `#2F412F`, gold
`#CA9A3A`, copper `#934E1F`, plus the logo's metallic gradient.

Derived for the web, all documented as tokens:

| Token | Value | Use |
|---|---|---|
| `--green-950` | `#06190F` | Deepest surface: header, hero, footer, drawers |
| `--green-900` | `#0A2A1B` | Cards on dark |
| `--paper` | `#F6F2EA` | Light sections |
| `--paper-2` | `#ECE5D6` | Alternate light sections |
| `--gold-ink` | `#85611A` | Gold text on light surfaces (passes AA; brand gold does not) |
| `--ink` | `#0B140F` | Body text on light |
| `--on-dark` | `#EEE8DA` | Body text on dark |

Contrast: gold on `--green-950` is about 7:1. Brand gold on paper fails AA
for text, so light sections use `--gold-ink` for small gold type.

## Type

- **Archivo** (variable width and weight), the athletic display face. Headlines
  at `font-stretch: 72%`, weight 800, uppercase, tight leading. Eyebrows and
  buttons at `font-stretch: 125%`, widely tracked, echoing the spaced **R U B**.
- **Inter** for body copy.
- Fluid scale: `--fs-display` (hero), `--fs-h1`, `--fs-h2`, `--fs-h3`, `--fs-lead`.

## Icons

25 icons in one family plus the designer's 7 official badges, all inline SVG
with `fill="currentColor"`, so they take gold on dark and green on light.
Usage: `{% render 'icons/warming' %}`.

Benefits: `fast-absorbing`, `warming`, `non-greasy`, `botanical`,
`certified-lab`, `tested-clean`, `shatter-proof`.
Uses: `warm-up`, `performance`, `recovery`, `shake`, `pump`, `rub-in`.
Roster: `combat`, `endurance`, `lifting`, `paddle`, `therapist`, `team`,
`gear-bag`.
Commerce: `shipping`, `guarantee`, `worldwide`, `secure`, `bundles`.
Badges: `badge-made-in-usa`, `badge-non-gmo`, `badge-paraben-free`,
`badge-sulfate-free`, `badge-phthalate-free`, `badge-bpa-free`,
`badge-aluminum-free`.

## Components

Buttons (`.btn`, `--ghost`, `--green`, `--outline`, `--sm`, `--lg`), eyebrow,
icon chip, product shelf (`.p-tile`), product card (`.p-card`), roster card,
moment card, ingredient card, quote card, step card, stats, accordion, cart
drawer with free-shipping meter, sticky mobile buy bar, page hero, CTA band.

## Motion

Short fades on scroll (`[data-reveal]`), product lift on hover, button gold
sweep. Everything honours `prefers-reduced-motion`. The hero never animates,
so it paints immediately.

## Layout

Mobile first. Breakpoints at 640, 900, 1000/1100 px. Container 1320 px,
gutter 16 px on phones. On phones the hero stacks (photo, then copy) so the
bottle is never covered, and the three bottles stay together on one shelf.
