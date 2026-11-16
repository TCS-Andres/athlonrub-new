# Athlon Rub storefront v3

A clean rebuild of the Athlon Rub site on the 2026 brand: the sash-and-star
shield, the official 2026 palette, a bespoke icon family drawn from the logo,
Seedream 5.5 campaign photography and properly cut product shots.

It is a fast static preview built with Eleventy and **Liquid**, structured so
every section ports to a Shopify Online Store 2.0 theme with minimal changes.
See [`docs/shopify-port.md`](docs/shopify-port.md).

## Run it

```bash
cd site
npm install
npm run dev      # http://localhost:8083
npm run build    # writes _site/
npm run check    # links, alt text, em dashes, one h1 per page
```

Append `?shot` to any URL to disable scroll reveals and lazy loading, for
full-page screenshots.

## Structure

```
site/
  eleventy.config.js        Liquid setup + Shopify-style money filters
  src/
    _data/                  products, nav, site settings, testimonials, faqs,
                            formula, images (photo manifest)
    _includes/
      layouts/              base (html shell) and sections (renders the list)
      sections/             one file per section, Shopify-style
      snippets/             img, bottle, product-card, add-button, arrow, drawers
      icons/                25 brand icons + 7 official badges, inline SVG
    assets/
      css/main.css          design tokens and every component
      js/main.js            drawers, bag, gallery, filters, reveals
      brand/                2026 logo marks (from the official pack)
      img/scenes/           Seedream 5.5 photography (WebP, lg + sm)
      img/products/         cut-out bottles and bundle composites
      img/real/             real photography: founder, testimonials, events
    index.liquid            home
    collections/all.liquid  shop
    products/product.liquid one template, six product pages
    pages/                  10 supporting pages
  docs/                     design system, imagery spec, port guide
                            (the client decision log stays local, gitignored)
  tools/check.mjs           post-build checks
```

Each page is a list of `sections:` in its front matter, each with `settings`
and `blocks`. That is the same shape as a Shopify JSON template.

## Pages

Home, Shop, six product pages (Travel, Pro, Coach, Pay 5 Carry 6, Pay 10 Carry
12, Team Case), Our story, The founder, The formula, How to use, Warm-Up,
Performance, Recovery, Testimonials, FAQ, Contact. URLs match the live Shopify
store's handles.

## Bag and checkout

The preview keeps a local bag. Checkout sends it to athlonrub.com through a
Shopify cart permalink (`/cart/{variant}:{qty},...`) using the live variant
IDs, so orders placed from the preview are real orders.

## The Athlon Rub assistant (AI chat)

A chat widget on every page ("Ask Athlon") that answers product and order
questions, recommends the right size or bundle, and builds sport-specific
warm-ups that show where Athlon Rub fits, with a disclaimer that it is not a
coach or medical professional.

- **Widget:** `src/_includes/snippets/assistant.liquid`, `src/assets/js/assistant.js`,
  styles in `main.css` section 25b. Product recommendations render as cards whose
  Add button uses the same bag as the rest of the site.
- **API:** `api/chat.js`, a Vercel Function that streams Claude Opus 5.5
  (`claude-opus-5-5`, effort `low`) with server-side refusal fallback enabled.
  Key: `ANTHROPIC_API_KEY` in the Vercel project's encrypted env.
- **Knowledge and rules:** `lib/assistant-prompt.js`. Product, FAQ, ingredient
  and testimonial facts are generated from `src/_data/`, so editing a price or
  FAQ there updates the assistant too. The claim rules, sales playbook and
  warm-up library are written out in the same file.
- **Safeguards:** same-origin check, per-IP rate limit, message length caps,
  no conversation storage or content logging (only token counts are logged).
- **Test it:** `node tools/chat-test.mjs` runs five scripted conversations
  (sizing, warm-up, injury, jailbreak, Spanish) against the real API.
- **Run locally with the API:** `vercel dev --cwd site` (uses the project's
  development env vars).

Cost, measured: the 7.7K-token system prompt is cached after the first call,
so a typical reply costs about 1 to 2 cents and starts streaming in 1 to 3
seconds.

## Where the assets come from

- **Logo and marks:** `Brand Elements/2026-rebrand/` (official pack).
- **Icons:** generated with Nano Banana Pro as style-locked sheets, traced to
  SVG. Pipeline: `Brand Elements/2026-icons/vectorize_icons.py`.
- **Photography:** Seedream 5.5 via Kie.ai. Pipeline and prompts:
  `Lifestyle Photos/2026-site/`. Spec: `docs/imagery-spec.md`.
- **Product cut-outs:** the real pack shots, background removed, label pixels
  untouched.
- **Real photos:** founder, testimonial athletes and events, from the live
  site. AI imagery is never used to depict a named person.
