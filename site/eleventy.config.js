// Athlon Rub v3 storefront preview.
//
// Pages are lists of sections (front matter `sections:`), each rendered from
// src/_includes/sections/{type}.liquid with a `section` object holding
// `settings` and `blocks`. That is the same shape as a Shopify Online Store
// 2.0 JSON template, so porting is a copy of the section files plus moving
// front matter into templates/*.json. See docs/shopify-port.md.

export default function (eleventyConfig) {
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
