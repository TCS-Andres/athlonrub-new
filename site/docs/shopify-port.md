# Porting v3 to a Shopify theme

The preview was built so the port is mostly copying. Start from a clean Online
Store 2.0 base (Dawn, or an empty theme) and bring these across.

## 1. Assets

- `src/assets/css/main.css` → `assets/main.css`, loaded in `layout/theme.liquid`.
- `src/assets/js/main.js` → `assets/main.js`. Replace the `Bag` object with
  Shopify's AJAX cart: `POST /cart/add.js`, `POST /cart/change.js`,
  `GET /cart.js`. The drawer markup and free-shipping meter stay as they are.
- Brand marks, badges and the real photos → `assets/`.
- Scene photography and product cut-outs → upload to Files (or product media)
  and reference with `image_url`.

## 2. Sections

Each file in `src/_includes/sections/` becomes `sections/{name}.liquid`.

- `section.settings.*` and `section.blocks` already match Shopify's names. Add
  a `{% schema %}` block to each section listing its settings and block types.
- Replace `{% render 'snippets/img', name: ... %}` with
  `{{ section.settings.image | image_url: width: 2400 | image_tag: widths: '800,1200,1600,2400', sizes: ... }}`.
- Replace `{% render 'snippets/bottle' %}` with the product's featured image
  (upload the transparent cut-outs as each product's first media item).
- `{% include %}` of a section becomes `{% render %}` for snippets, since
  sections are rendered by Shopify itself.
- `products | by_handles: s.handles` becomes a `product_list` setting
  (`section.settings.products`).
- `testimonials`, `faqs` and `formula` data become blocks, or metaobjects if
  the client wants to edit them centrally.

## 3. Templates

Each page's front matter `sections:` list becomes a JSON template:

| Preview file | Shopify template |
|---|---|
| `src/index.liquid` | `templates/index.json` |
| `src/collections/all.liquid` | `templates/collection.json` |
| `src/products/product.liquid` | `templates/product.json` (`product-main` becomes the main product section with a product form) |
| `src/pages/*.liquid` | `templates/page.{handle}.json`, assigned to each page in the admin |

## 4. Product data

`src/_data/products.json` mirrors the live catalogue (handles, variant IDs,
prices). In Shopify, keep: `tagline`, `summary`, `best_for`, `closure` and the
`scenes` list as product metafields (`custom.tagline`, `custom.best_for`, ...).
The size picker links sibling sizes; use a `custom.size_siblings` product list
metafield or a collection.

## 5. The AI assistant

Keep the API on Vercel; Shopify themes cannot run server code.

- Copy `snippets/assistant.liquid` into the theme and render it in
  `layout/theme.liquid`. Set `data-endpoint` to the full Vercel URL, for
  example `https://athlonrub-v3.vercel.app/api/chat`.
- Replace the `chat_products` filter output with a small Liquid loop over the
  products the assistant can recommend (handle, title, size, price, variant id,
  featured image URL), and point the card image at that URL.
- In the Vercel project, set `ALLOWED_ORIGINS` to the store domains
  (`https://athlonrub.com,https://www.athlonrub.com`, already the default) and
  add CORS headers to `api/chat.js` for those origins.
- The card's Add button then calls `/cart/add.js` with the variant id, like the
  rest of the ported bag.

## 6. Things the preview fakes

- **Bag:** local storage, checkout by cart permalink. Port to AJAX cart.
- **Newsletter:** collects nothing. Port to `{% form 'customer' %}`.
- **Subscription:** links to the live product page. Port to selling plans in
  the product form.
- **Account icon:** links to the live account page. Use `routes.account_url`.
