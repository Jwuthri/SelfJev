import fs from "node:fs";
import path from "node:path";
import scoreSnapshot from "@/data/scores.json";
export const REPO = "https://github.com/Jwuthri/SelfJev";
export const JOURNAL = "https://jwuthri.github.io/SelfJev";
const root = path.resolve(process.cwd(), "..");
export const source = (file: string) => `${REPO}/blob/master/${file}`;
// reports/**/report.json are Git LFS files that Vercel does not fetch; the build reads
// this snapshot instead (regenerate with `node scripts/build-scores.mjs`).
type ImageGroup = { accuracy: number; n: number; kinds: number };
const scores: Record<string, { accuracy: number; n: number; groups?: Record<"trained" | "unseen", ImageGroup> }> = scoreSnapshot;
export const hasScore = (file: string) => file in scores;
export function score(file: string) {
  const report = scores[file];
  if (!report) throw new Error(`No score snapshot for ${file}; run node scripts/build-scores.mjs`);
  const accuracy = report.accuracy * 100;
  if (!Number.isFinite(accuracy)) throw new Error(`Invalid accuracy: ${file}`);
  return {
    value: accuracy,
    display: accuracy.toFixed(1),
    n: report.n,
    url: source(file),
  };
}
export function headlines() {
  return {
    eval2: score("reports/images_v1/eval2/report.json"),
    llm: score("reports/images_v1/eval_llm/report.json"),
    dev: score("reports/images_v1/test/report.json"),
    original: score("reports/qwen35_4b_tree_scratch_jevall_/eval2/report.json"),
    jev: score("reports/external/eval2/typesafe_jev-latest/report.json"),
  };
}
export function imageResults() {
  const file = "reports/images_v1/images_v1_images/report.json";
  const baselineFile = "reports/images_v1/base_selfjev_4b_images/report.json";
  const groups = scores[file]?.groups;
  const baselineGroups = scores[baselineFile]?.groups;
  if (!groups || !baselineGroups) throw new Error("Missing image groups; regenerate scores.json");
  const group = (key: "trained" | "unseen") => ({
    ...groups[key],
    display: (groups[key].accuracy * 100).toFixed(1),
    baseline: (baselineGroups[key].accuracy * 100).toFixed(1),
  });
  return { overall: score(file), baseline: score(baselineFile), trained: group("trained"), unseen: group("unseen") };
}
export type EvidenceRow = {
  id: string;
  name: string;
  base: string;
  architecture: string;
  eval2: number | null;
  dev: number;
  llm: number | null;
  urls: { eval2: string; dev: string; llm: string };
  current: boolean;
};
export function leaderboard(): EvidenceRow[] {
  // Jev's AI-review result is derived from stored predictions in the canonical
  // dataset, not an external report.json. Reuse the published audited export.
  const jevReviewFile = "weights/selfjev_4b/assets/chart-data.json";
  const chartData = JSON.parse(fs.readFileSync(path.join(root, jevReviewFile), "utf8"));
  const textOnlyReview = score("reports/selfjev_4b_treeserver/eval_llm/report.json");
  const jevReview = chartData.overview.find((entry: { source: string }) =>
    entry.source === "reports/selfjev_4b_treeserver/eval_llm/report.json");
  if (!jevReview || jevReview.n !== textOnlyReview.n ||
      Math.abs(jevReview.ours - textOnlyReview.value) > 0.000001 ||
      !Number.isFinite(jevReview.jev) || jevReview.jev < 0 || jevReview.jev > 100) {
    throw new Error("Jev AI-review export does not match the current evaluation suite");
  }
  const ledger = fs
    .readFileSync(path.join(root, "docs/experiments.md"), "utf8")
    .split("<!-- ledger:start -->")[1]
    .split("<!-- ledger:end -->")[0];
  return ledger
    .trim()
    .split("\n")
    .slice(2)
    .map((line) => {
      const c = line
        .split("|")
        .slice(1, -1)
        .map((s) => s.trim());
      const file = c[11].match(/\(\.\.\/(.*?)\)/)![1].replace(/\.md$/, ".json");
      const dev = score(file).value;
      const e2 =
        c[0] === "external"
          ? `reports/external/eval2/${file.split("/")[3]}/report.json`
          : `reports/${c[0]}/eval2/report.json`;
      const llm = `reports/${c[0]}/eval_llm/report.json`;
      const current = c[0] === "images_v1";
      const isJev = c[0] === "external" && c[1] === "~typesafe/jev-latest";
      return {
        id: c[0] === "external" ? c[1] : c[0],
        name: current
          ? "SelfJev-4B · vision release"
          : c[0] === "selfjev_4b_treeserver"
            ? "SelfJev-4B · text-only release"
          : c[0] === "qwen35_4b_tree_scratch_jevall_"
            ? "SelfJev-4B · text-only original evaluation"
            : c[0] === "external"
              ? c[1].replace("~typesafe/", "").replace("openai/", "")
              : c[0],
        base: c[1],
        architecture: c[2],
        eval2: hasScore(e2) ? score(e2).value : null,
        dev,
        llm: isJev ? jevReview.jev : hasScore(llm) ? score(llm).value : null,
        urls: { dev: source(file), eval2: source(e2), llm: source(isJev ? jevReviewFile : llm) },
        current,
      };
    });
}
export type HardwareLatencyPoint = {
  tokens: number;
  questions: number;
  a10g: number;
  l40s: number;
  h100: number;
};
export type MacLatencyPoint = { tokens: number; questions: number; ms: number };

export function macLatencyData(): MacLatencyPoint[] {
  const report = JSON.parse(fs.readFileSync(path.join(root, "reports/latency/mac_m5_pro_selfjev4b.json"), "utf8"));
  if (report.meta.model.device !== "mps" || report.meta.model.model !== "Qwen/Qwen3.5-4B") {
    throw new Error("Unexpected local Mac benchmark model");
  }
  return report.cells.map((cell: { text_tokens: number; questions: number; median_ms: number; samples_ms: number[] }) => {
    if (cell.samples_ms.length !== 10) throw new Error("Mac benchmark needs 10 timed samples per cell");
    const sorted = [...cell.samples_ms].sort((a, b) => a - b);
    const median = (sorted[4] + sorted[5]) / 2;
    if (Math.abs(median - cell.median_ms) > 0.01) throw new Error("Mac benchmark median does not match its samples");
    return { tokens: cell.text_tokens, questions: cell.questions, ms: median };
  });
}

// The three files use the same archived tree_4b_combo model and request shapes.
// They were measured in separate sweeps; values are server-side medians, not network RTTs.
export function hardwareLatencyData(): HardwareLatencyPoint[] {
  const sources = [
    ["a10g", "reports/latency/requests_combo.jsonl", "combo_vllm"],
    ["l40s", "reports/latency/requests_qwen35.jsonl", "combo_vllm_l40s"],
    ["h100", "reports/latency/requests_h100.jsonl", "h100_bf16"],
  ] as const;
  const loaded = sources.map(([key, file, endpoint]) => ({
    key,
    endpoint,
    rows: fs.readFileSync(path.join(root, file), "utf8").trim().split("\n").map((line) => JSON.parse(line)),
  }));
  return [1, 16].flatMap((questions) =>
    [8, 512, 2048, 4096].map((tokens) => {
      const values = Object.fromEntries(loaded.map(({ key, endpoint, rows }) => {
        const times = rows
          .filter((r: { status: number; rep: number; endpoint: string; questions: number; text_tokens: number }) =>
            r.status === 200 && r.rep > 0 && r.endpoint === endpoint &&
            r.questions === questions && r.text_tokens === tokens)
          .map((r: { server_ms: number }) => r.server_ms)
          .sort((a: number, b: number) => a - b);
        if (times.length !== 10) throw new Error(`Expected 10 latency samples for ${key}, ${tokens} tokens, ${questions} questions`);
        return [key, (times[4] + times[5]) / 2];
      }));
      return { tokens, questions, ...values } as HardwareLatencyPoint;
    }),
  );
}
