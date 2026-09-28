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
  scores[path.relative(repo, file)] = { accuracy, n: report.meta.n };
}
fs.mkdirSync("data", { recursive: true });
fs.writeFileSync("data/scores.json", JSON.stringify(scores, null, 1) + "\n");
console.log(`${Object.keys(scores).length} reports -> data/scores.json`);
