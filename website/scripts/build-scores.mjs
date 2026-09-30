// Snapshot of the numbers the site reads from reports/**/report.json.
// Those reports are Git LFS files, which Vercel does not pull, so the build reads
// data/scores.json (a few KB, committed) instead. Re-run after writing a new report:
//   node scripts/build-scores.mjs
import fs from "node:fs";
import path from "node:path";
const repo = path.resolve("..");
const walk = (dir) =>
  fs.readdirSync(dir, { withFileTypes: true }).flatMap((e) =>
    e.isDirectory() ? walk(path.join(dir, e.name)) : [path.join(dir, e.name)]);
const scores = {};
for (const file of walk(path.join(repo, "reports")).sort()) {
  if (path.basename(file) !== "report.json") continue;
  const text = fs.readFileSync(file, "utf8");
  if (text.startsWith("version https://git-lfs")) {
    throw new Error(`${file} is an LFS pointer; run git lfs pull first`);
  }
  const report = JSON.parse(text);
  const accuracy = report.metrics?.question_accuracy;
  if (!Number.isFinite(accuracy) || !report.meta?.n) continue;
  const relative = path.relative(repo, file);
  const entry = { accuracy, n: report.meta.n };
  if (["reports/images_v1/images_v1_images/report.json", "reports/images_v1/base_selfjev_4b_images/report.json"].includes(relative)) {
    // Categories in the vision training mix; all scored photos are held out.
    const trained = ["img_pets", "img_fashion", "img_beans", "img_rice", "img_eurosat", "img_trash"];
    const unseen = ["img_hurricane", "img_indoor", "img_painting", "img_snacks"];
    if (report.predictions.length !== report.meta.n || report.predictions.some((p) => ![...trained, ...unseen].includes(p.family))) {
      throw new Error(`Unexpected image evaluation coverage: ${relative}`);
    }
    entry.groups = Object.fromEntries(Object.entries({ trained, unseen }).map(([key, families]) => {
      const rows = report.predictions.filter((p) => families.includes(p.family));
      if (!rows.length || rows.some((p) => typeof p.correct !== "boolean")) throw new Error(`Invalid image group: ${relative}/${key}`);
      return [key, { accuracy: rows.filter((p) => p.correct).length / rows.length, n: rows.length, kinds: families.length }];
    }));
  }
  scores[relative] = entry;
}
fs.mkdirSync("data", { recursive: true });
fs.writeFileSync("data/scores.json", JSON.stringify(scores, null, 1) + "\n");
console.log(`${Object.keys(scores).length} reports -> data/scores.json`);
