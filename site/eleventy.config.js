// Athlon Rub v3 storefront preview.
//
// Pages are lists of sections (front matter `sections:`), each rendered from
// src/_includes/sections/{type}.liquid with a `section` object holding
// `settings` and `blocks`. That is the same shape as a Shopify Online Store
// 2.0 JSON template, so porting is a copy of the section files plus moving
// front matter into templates/*.json. See docs/shopify-port.md.

import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";

// Cache-busting: one short hash of the stylesheet, scripts and photo manifest,
// recomputed before every build and appended as ?v= to asset URLs. Any change
// to those files gives every asset a new URL, so browsers never pair new
// markup with a stale cached stylesheet or photo.
const VERSIONED = [
  "src/assets/css/main.css", "src/assets/js/main.js", "src/assets/js/assistant.js", "src/_data/images.json",
  "src/assets/video/hero-ambient.mp4", "src/assets/video/hero-ambient.webm", "src/assets/video/hero-ambient-poster.jpg",
];
let assetVersion = "dev";
const computeVersion = () => {
  const h = createHash("sha1");
  for (const f of VERSIONED) h.update(readFileSync(new URL(`./${f}`, import.meta.url)));
  assetVersion = h.digest("hex").slice(0, 10);
};

export default function (eleventyConfig) {
  computeVersion();
  eleventyConfig.on("eleventy.before", computeVersion);
  eleventyConfig.addFilter("v", (url) => `${url}${String(url).includes("?") ? "&" : "?"}v=${assetVersion}`);

  eleventyConfig.addPassthroughCopy({ "src/assets": "assets" });
  eleventyConfig.addPassthroughCopy({ "src/assets/brand/favicon.png": "favicon.png" });

  eleventyConfig.setLiquidOptions({
    dynamicPartials: true,
    strictFilters: true,
    jsTruthy: false,
  });

  // Shopify-compatible money filters: prices are stored in cents.
  const money = (cents) => {
    const n = Number(cents || 0) / 100;
    return "$" + n.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  };
  eleventyConfig.addFilter("money", money);
  eleventyConfig.addFilter("money_without_trailing_zeros", (cents) => money(cents).replace(/\.00$/, ""));

  // Small helpers Shopify provides natively.
  eleventyConfig.addFilter("handleize", (s) =>
    String(s || "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "")
  );
  eleventyConfig.addFilter("where_exp_handle", (arr, handle) => (arr || []).find((p) => p.handle === handle));
  eleventyConfig.addFilter("by_handles", (arr, handles) =>
    (handles || []).map((h) => (arr || []).find((p) => p.handle === h)).filter(Boolean)
  );
  eleventyConfig.addFilter("reject_handle", (arr, handle) => (arr || []).filter((p) => p.handle !== handle));
  // Minimal product data the chat widget needs to render product cards.
  eleventyConfig.addFilter("chat_products", (arr) =>
    JSON.stringify(
      (arr || []).map((p) => ({
        handle: p.handle, title: p.title, size: p.size, price: p.price,
        compare_at_price: p.compare_at_price, variant_id: p.variant_id, cutout: p.cutout,
        image: `/assets/img/products/${p.cutout}.webp?v=${assetVersion}`,
      }))
    ).replace(/</g, "\\u003c")
  );
  eleventyConfig.addFilter("json_attr", (v) => JSON.stringify(v).replace(/"/g, "&quot;"));

  return {
    dir: { input: "src", includes: "_includes", data: "_data", output: "_site" },
    templateFormats: ["liquid", "md", "html"],
    htmlTemplateEngine: "liquid",
    markdownTemplateEngine: "liquid",
  };
}
