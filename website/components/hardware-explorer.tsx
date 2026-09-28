"use client";

import Link from "next/link";
import { useState } from "react";
import { ArrowUpRight, Cpu } from "lucide-react";
import type { HardwareLatencyPoint, MacLatencyPoint } from "@/lib/evidence";

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

export function HardwareExplorer({ data, mac }: { data: HardwareLatencyPoint[]; mac: MacLatencyPoint[] }) {
  const [tokens, setTokens] = useState(512);
  const [questions, setQuestions] = useState(1);
  const row = data.find((point) => point.tokens === tokens && point.questions === questions);
  const macRow = mac.find((point) => point.tokens === tokens && point.questions === questions);
  if (!row) return null;
  const maximum = Math.max(row.a10g, row.l40s, row.h100);

  return (
    <div className="hardware-panel">
      <div className="hardware-header">
        <div>
          <span className="eyebrow">SELF-HOSTING / HARDWARE LATENCY</span>
          <h3>Choose the machine.</h3>
          <p>Typical processing time for one request. Lower is faster.</p>
        </div>
        <span className="hardware-model-tag">MEASURED LATENCY</span>
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
          <div className="hardware-name"><strong><Cpu size={16} /> M5 Pro</strong><span>48 GB unified · MPS</span></div>
          <p>Local Apple Silicon</p>
          <strong className="hardware-time">{macRow ? Math.round(macRow.ms).toLocaleString() : "—"}<small>{macRow ? "ms" : ""}</small></strong>
          <a href="https://github.com/Jwuthri/SelfJev/blob/master/reports/latency/mac_m5_pro_selfjev4b.json" aria-label="M5 Pro raw latency measurements" title="Mac benchmark report"><ArrowUpRight size={15} /></a>
        </div>
      </div>
      <div className="hardware-footer">
        <p>Median of 10 warmed runs. Three answer options per question. Network time excluded. A dash means that workload has not been measured.</p>
        <Link href="/docs/hardware/#compare-measured-gpu-response-times">How we measured <ArrowUpRight size={14} /></Link>
      </div>
    </div>
  );
}
