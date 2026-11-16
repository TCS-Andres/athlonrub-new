// Post-build checks for the static preview. Run: npm run build && npm run check
// - every internal href/src resolves to a built file
// - every <img> has an alt attribute
// - no em dashes in rendered copy (brand rule)
// - no image placeholders left (missing manifest entries)
// - one <h1> per page
import { readFileSync, existsSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const OUT = fileURLToPath(new URL("../_site/", import.meta.url));
const pages = [];
(function walk(d) {
  for (const f of readdirSync(d)) {
    const p = join(d, f);
    if (statSync(p).isDirectory()) walk(p);
    else if (f.endsWith(".html")) pages.push(p);
  }
})(OUT);

const problems = [];
const resolve = (u) => {
  const clean = u.split("#")[0].split("?")[0];
  if (!clean) return true;
  const p = join(OUT, clean);
  return existsSync(p) && (statSync(p).isFile() || existsSync(join(p, "index.html")));
};

for (const file of pages) {
  const rel = file.replace(OUT, "/");
  const html = readFileSync(file, "utf8");
  const text = html.replace(/<script[\s\S]*?<\/script>/g, "").replace(/<style[\s\S]*?<\/style>/g, "");
  for (const [, u] of text.matchAll(/(?:href|src)="(\/[^"]*)"/g)) if (!resolve(u)) problems.push(`${rel}: broken ${u}`);
  for (const [, u] of text.matchAll(/srcset="([^"]*)"/g))
    for (const part of u.split(",")) { const s = part.trim().split(" ")[0]; if (s.startsWith("/") && !resolve(s)) problems.push(`${rel}: broken srcset ${s}`); }
  for (const [tag] of text.matchAll(/<img\b[^>]*>/g)) if (!/\balt="/.test(tag)) problems.push(`${rel}: img without alt ${tag.slice(0, 80)}`);
  const visible = text.replace(/<[^>]+>/g, " ");
  if (/—/.test(visible)) problems.push(`${rel}: em dash in copy`);
  if (/media--placeholder/.test(text)) problems.push(`${rel}: image placeholder (missing manifest entry)`);
  const h1 = (text.match(/<h1\b/g) || []).length;
  if (h1 !== 1) problems.push(`${rel}: ${h1} <h1> elements`);
}

console.log(`Checked ${pages.length} pages.`);
if (problems.length) { console.log(problems.join("\n")); process.exit(1); }
console.log("No problems found.");
