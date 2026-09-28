import fs from "node:fs";
import path from "node:path";
export const REPO = "https://github.com/Jwuthri/SelfJev";
export const JOURNAL = "https://jwuthri.github.io/SelfJev";
const root = path.resolve(process.cwd(), "..");
export const source = (file: string) => `${REPO}/blob/master/${file}`;
export function score(file: string) {
  const report = JSON.parse(fs.readFileSync(path.join(root, file), "utf8"));
  const accuracy = report.metrics.question_accuracy * 100;
  if (!Number.isFinite(accuracy)) throw new Error(`Invalid accuracy: ${file}`);
  return {
    value: accuracy,
    display: accuracy.toFixed(1),
    n: report.meta.n,
    url: source(file),
  };
}
export function headlines() {
  return {
    eval2: score("reports/selfjev_4b_treeserver/eval2/report.json"),
    llm: score("reports/selfjev_4b_treeserver/eval_llm/report.json"),
    dev: score("reports/selfjev_4b_treeserver/test/report.json"),
    original: score("reports/qwen35_4b_tree_scratch_jevall_/eval2/report.json"),
    jev: score("reports/external/eval2/typesafe_jev-latest/report.json"),
  };
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
      const current = c[0] === "selfjev_4b_treeserver";
      return {
        id: c[0] === "external" ? c[1] : c[0],
        name: current
          ? "SelfJev-4B · current engine"
          : c[0] === "qwen35_4b_tree_scratch_jevall_"
            ? "SelfJev-4B · original evaluation"
            : c[0] === "external"
              ? c[1].replace("~typesafe/", "").replace("openai/", "")
              : c[0],
        base: c[1],
        architecture: c[2],
        eval2: fs.existsSync(path.join(root, e2)) ? score(e2).value : null,
        dev,
        llm: fs.existsSync(path.join(root, llm)) ? score(llm).value : null,
        urls: { dev: source(file), eval2: source(e2), llm: source(llm) },
        current,
      };
    });
}
export type SpeedPoint = {
  tokens: number;
  questions: number;
  ours: number;
  jev: number;
  wallOurs: number;
  wallJev: number;
};
export function speedData(): SpeedPoint[] {
  const rows = fs
    .readFileSync(
      path.join(root, "reports/latency/requests_h100.jsonl"),
      "utf8",
    )
    .trim()
    .split("\n")
    .map((s) => JSON.parse(s));
  const median = (values: number[]) => {
    values.sort((a, b) => a - b);
    const m = Math.floor(values.length / 2);
    return values.length % 2 ? values[m] : (values[m - 1] + values[m]) / 2;
  };
  return [1, 16].flatMap((questions) =>
    [8, 512, 2048, 4096].map((tokens) => {
      const samples = (endpoint: string, key: string) =>
        median(
          rows
            .filter(
              (r) =>
                r.status === 200 &&
                r.rep > 0 &&
                r.endpoint === endpoint &&
                r.questions === questions &&
                r.text_tokens === tokens,
            )
            .map((r) => r[key]),
        );
      return {
        tokens,
        questions,
        ours: samples("h100_bf16", "server_ms"),
        jev: samples("jev", "server_ms"),
        wallOurs: samples("h100_bf16", "wall_ms"),
        wallJev: samples("jev", "wall_ms"),
      };
    }),
  );
}

export type HardwareLatencyPoint = {
  tokens: number;
  questions: number;
  a10g: number;
  l40s: number;
  h100: number;
};

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
