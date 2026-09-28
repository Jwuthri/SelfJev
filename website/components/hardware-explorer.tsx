"use client";

import Link from "next/link";
import { useState } from "react";
import { ArrowUpRight, Cpu } from "lucide-react";
import type { HardwareLatencyPoint } from "@/lib/evidence";

const inputSizes = [
  { tokens: 8, label: "Very short" },
  { tokens: 512, label: "Short" },
  { tokens: 2048, label: "Medium" },
  { tokens: 4096, label: "Long" },
] as const;
const hardware = [
  { key: "a10g", name: "A10G", memory: "24 GB", className: "a10g", source: "requests_combo.jsonl" },
  { key: "l40s", name: "L40S", memory: "48 GB", className: "l40s", source: "requests_qwen35.jsonl" },
  { key: "h100", name: "H100", memory: "80 GB", className: "h100", source: "requests_h100.jsonl" },
] as const;

export function HardwareExplorer({ data }: { data: HardwareLatencyPoint[] }) {
  const [tokens, setTokens] = useState(512);
  const [questions, setQuestions] = useState(1);
  const row = data.find((point) => point.tokens === tokens && point.questions === questions);
  if (!row) return null;
  const maximum = Math.max(row.a10g, row.l40s, row.h100);

  return (
    <div className="hardware-panel">
      <div className="hardware-header">
        <div>
          <span className="eyebrow">SELF-HOSTED / MEASURED GPU RUNS</span>
          <h3>Choose the machine.</h3>
          <p>Typical processing time for one request. Lower is faster.</p>
        </div>
        <span className="hardware-model-tag">EARLIER QWEN3 TREE MODEL</span>
      </div>
      <div className="hardware-controls">
        <fieldset>
          <legend>Input length · {tokens.toLocaleString()} text tokens</legend>
          <div className="hardware-options">
            {inputSizes.map((item) => (
              <button key={item.tokens} type="button" aria-pressed={tokens === item.tokens} onClick={() => setTokens(item.tokens)}>
                {item.label}
              </button>
            ))}
          </div>
        </fieldset>
        <fieldset>
          <legend>Questions about the same text</legend>
          <div className="hardware-options">
            {[1, 16].map((count) => (
              <button key={count} type="button" aria-pressed={questions === count} onClick={() => setQuestions(count)}>
                {count} {count === 1 ? "question" : "questions"}
              </button>
            ))}
          </div>
        </fieldset>
      </div>
      <div className="hardware-results" aria-live="polite">
        {hardware.map((gpu) => {
          const ms = row[gpu.key];
          return (
            <div className={`hardware-result ${gpu.className}`} key={gpu.key}>
              <div className="hardware-name"><strong>{gpu.name}</strong><span>{gpu.memory} GPU memory</span></div>
              <div className="hardware-track" aria-hidden="true"><span style={{ width: `${(ms / maximum) * 100}%` }} /></div>
              <strong className="hardware-time">{Math.round(ms)}<small>ms</small></strong>
              <a href={`https://github.com/Jwuthri/SelfJev/blob/master/reports/latency/${gpu.source}`} aria-label={`${gpu.name} raw latency measurements`} title="Raw measurements"><ArrowUpRight size={15} /></a>
            </div>
          );
        })}
        <div className="hardware-result mac">
          <div className="hardware-name"><strong><Cpu size={16} /> Apple Silicon</strong><span>Local Mac</span></div>
          <p>Not measured. Current server requires NVIDIA CUDA.</p>
          <Link href="/docs/hardware/" aria-label="Apple Silicon hardware support details" title="Hardware support details"><ArrowUpRight size={15} /></Link>
        </div>
      </div>
      <div className="hardware-footer">
        <p><strong>Scope:</strong> These are separate 2026 sweeps of an earlier Qwen3-4B model on vLLM, with three answer options per question. Each number is the median of 10 timed requests after warm-up, measured inside the server. The current SelfJev-4B / TreeServer has not been timed on any of these GPUs.</p>
        <Link href="/docs/hardware/">Sizing guide <ArrowUpRight size={14} /></Link>
      </div>
    </div>
  );
}
