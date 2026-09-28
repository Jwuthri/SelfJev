import fs from "node:fs";
import path from "node:path";
import assert from "node:assert/strict";
const output = path.resolve("out");
const repo = path.resolve("..");
const base = process.env.NEXT_PUBLIC_BASE_PATH || "";
const walk = (dir) =>
  fs
    .readdirSync(dir, { withFileTypes: true })
    .flatMap((e) =>
      e.isDirectory() ? walk(path.join(dir, e.name)) : [path.join(dir, e.name)],
    );
const pages = walk(output).filter((f) => f.endsWith(".html"));
const broken = [];
let links = 0;
for (const file of pages) {
  const html = fs.readFileSync(file, "utf8");
  assert.match(html, /<title>[^<]+<\/title>/, `Missing title in ${file}`);
  for (const [, href] of html.matchAll(/<a\b[^>]*href="([^"]+)"/g)) {
    links++;
    if (href.startsWith("https://github.com/Jwuthri/SelfJev/blob/master/")) {
      const local = decodeURIComponent(
        href.split("/blob/master/")[1].split("#")[0],
      );
      if (!fs.existsSync(path.join(repo, local)))
        broken.push(`${file}: source ${local}`);
    }
    if (!href.startsWith("/") && !href.startsWith("#")) continue;
    const [raw, hash] = href.split("#");
    const route = decodeURIComponent(
      (base && raw.startsWith(base + "/") ? raw.slice(base.length) : raw) ||
        "/",
    );
    const target = raw
      ? path.join(output, route, route.endsWith("/") ? "index.html" : "")
      : file;
    const resolved =
      fs.existsSync(target) && fs.statSync(target).isFile()
        ? target
        : path.join(target, "index.html");
    if (!fs.existsSync(resolved)) {
      broken.push(`${file}: ${href}`);
      continue;
    }
    if (
      hash &&
      !fs
        .readFileSync(resolved, "utf8")
        .includes(`id="${decodeURIComponent(hash)}"`)
    )
      broken.push(`${file}: missing anchor ${href}`);
  }
}
assert.equal(broken.length, 0, broken.join("\n"));
for (const route of [
  "index.html",
  "research/index.html",
  "docs/index.html",
  ...[
    "hardware",
    "api",
    "architecture",
    "finetuning",
    "docker",
    "aws",
    "runpod",
    "gcp",
    "operations",
  ].map((x) => `docs/${x}/index.html`),
])
  assert.ok(fs.existsSync(path.join(output, route)), `Missing ${route}`);
const home = fs.readFileSync(path.join(output, "index.html"), "utf8");
for (const set of ["eval2", "eval_llm"]) {
  const r = JSON.parse(
    fs.readFileSync(
      path.join(repo, `reports/selfjev_4b_treeserver/${set}/report.json`),
      "utf8",
    ),
  );
  assert.ok(
    home.includes((100 * r.metrics.question_accuracy).toFixed(1)),
    `Missing current ${set} score`,
  );
}
console.log(
  `Export checked: ${pages.length} HTML pages, ${links} links; all internal targets, anchors, and linked repo sources exist. Current report scores are present.`,
);
