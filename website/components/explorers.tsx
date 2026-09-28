"use client";
import { useState } from "react";
import { ArrowUpRight, Search } from "lucide-react";
import type { EvidenceRow, SpeedPoint } from "@/lib/evidence";

const modelLabels: Record<string, [string, string]> = {
  selfjev_4b_treeserver: ["SelfJev", "Our current model · self-hosted"],
  "~typesafe/jev-latest": ["Jev", "TypeSafe’s hosted decision model"],
  qwen35_4b_tree: ["Earlier SelfJev", "Before training for AI response review"],
  lora_4b: ["Fine-tuned text reranker", "Our early approach · adapted from a search model"],
};
const testLabels = { eval2: "Text decisions", llm: "AI response review", dev: "Broader text tasks" };
const descriptions = {
  eval2: "How often did the model choose the expected answer? The same 1,991 questions test yes/no decisions, choosing one answer, and selecting all that apply.",
  llm: "Can it assess an AI response? 946 questions cover answer quality, factual support, policy compliance, and attempts to bypass instructions.",
  dev: "How broadly does it handle text? 3,471 questions span topics, intent, sentiment, and more. We reused these during development, so this is a progress measure, not an independent final test.",
};
export function Benchmarks({ rows, compact = false, archive = false }: {
  rows: EvidenceRow[];
  compact?: boolean;
  archive?: boolean;
}) {
  const [metric, setMetric] = useState<"eval2" | "llm" | "dev">("eval2");
  const [query, setQuery] = useState("");
  const filtered = rows
    .filter((r) => [r.name, r.id, r.base, r.architecture, ...(modelLabels[r.id] || [])].join(" ").toLowerCase().includes(query.toLowerCase()))
    .filter((r) => r[metric] !== null)
    .sort((a, b) => (b[metric] ?? 0) - (a[metric] ?? 0));
  return (
    <div className="benchmark-panel">
      {!compact && <div className="panel-toolbar">
        <div className="segmented" aria-label="Type of task">
          {(["eval2", "llm", "dev"] as const).map((x) => (
            <button key={x} aria-pressed={metric === x} onClick={() => setMetric(x)}>{testLabels[x]}</button>
          ))}
        </div>
        {archive && <label className="search">
          <Search size={15} />
          <input placeholder="Find a model or experiment…" value={query} onChange={(e) => setQuery(e.target.value)} aria-label="Filter research runs" />
        </label>}
      </div>}
      <p className="chart-description">{descriptions[metric]}</p>
      <div className="benchmark-head"><span>{archive ? "MODEL / EXPERIMENT" : "MODEL"}</span><span>ANSWERS MATCHED</span></div>
      <div aria-live="polite">
        {filtered.map((r, i) => (
          <a className={`benchmark-row ${r.current ? "current" : ""}`} href={r.urls[metric]} key={r.id}>
            <span className="rank">{String(i + 1).padStart(2, "0")}</span>
            <div className="model-name">
              <strong>{modelLabels[r.id]?.[0] || r.name}</strong>
              <span>{archive ? `${r.id} · ${r.base}` : modelLabels[r.id]?.[1] || r.base}</span>
            </div>
            <div className="bar-track"><span style={{ width: `${r[metric]}%` }} /></div>
            <strong className="score">{r[metric]?.toFixed(1)}<small>%</small></strong>
            <ArrowUpRight size={14} />
          </a>
        ))}
        {filtered.length === 0 && <p className="empty-state">No scored runs match “{query}”. Try another model name.</p>}
      </div>
      <p className="chart-note">
        {metric === "llm" && !archive ? "This view compares two versions of SelfJev; it does not rank competing services. " : ""}
        Scores are the share of answers matching the expected result; for “select all,” every choice must match. Only models with a recorded result are shown. Click a row for its report.
      </p>
    </div>
  );
}
export function SpeedExplorer({ data }: { data: SpeedPoint[] }) {
  const [q, setQ] = useState(1);
  const [wall, setWall] = useState(false);
  return (
    <div className="speed-panel">
      <div className="panel-toolbar">
        <div className="segmented" aria-label="Question count">
          {[1, 16].map((n) => <button key={n} aria-pressed={q === n} onClick={() => setQ(n)}>{n} question{n > 1 ? "s" : ""}</button>)}
        </div>
        <div className="segmented" aria-label="Timing scope">
          <button aria-pressed={!wall} onClick={() => setWall(false)}>Processing</button>
          <button aria-pressed={wall} onClick={() => setWall(true)}>With network</button>
        </div>
      </div>
      <div className="speed-legend">
        <span><i />Earlier prototype · H100</span>
        <span><i />Jev · hosted</span>
        <span>Typical time / milliseconds</span>
      </div>
      <div className="speed-chart">
        {data.filter((r) => r.questions === q).map((r) => (
          <div className="speed-group" key={r.tokens}>
            <span>{({8: "Very short", 512: "Short", 2048: "Medium", 4096: "Long"} as Record<number, string>)[r.tokens]} <small>input</small></span>
            <div>
              {[["ours", wall ? r.wallOurs : r.ours], ["jev", wall ? r.wallJev : r.jev]].map(([key, v]) => (
                <div className={`speed-bar ${key}`} key={key}>
                  <span style={{ width: `${(Number(v) / 300) * 100}%` }} />
                  <strong>{Math.round(Number(v))} <small>ms</small></strong>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
      <p className="chart-note"><b>These measurements are from an earlier prototype. The current SelfJev model has not yet been timed.</b></p>
      <details className="evidence-details speed-methodology">
        <summary>Measurement details</summary>
        <p>Median of 10 timed rounds per setting, after warm-up. Input lengths: 8, 512, 2,048, and 4,096 tokens. The prototype used Qwen3-4B with vLLM on an H100 in bf16. Jev was accessed through OpenRouter. Processing excludes network travel; “with network” includes it, with different distances to each server.</p>
        <a href="https://github.com/Jwuthri/SelfJev/blob/master/reports/latency/requests_h100.jsonl">Raw measurements ↗</a>
      </details>
    </div>
  );
}
