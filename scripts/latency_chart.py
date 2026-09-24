"""Latency vs text length, Jev vs ours (p50 at the client), from reports/latency/requests*.jsonl.

usage: uv run --with matplotlib python scripts/latency_chart.py   -> reports/latency/latency.png
"""
import json
import statistics
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "reports/latency"
rows = [r for f in sorted(OUT.glob("requests*.jsonl")) for r in map(json.loads, open(f)) if r["rep"] > 0 and r["status"] == 200]
SERIES = [("jev", "Jev (via OpenRouter)", "#d62728"), ("ours_vllm", "ours: tree 4B, vLLM, A10G", "#1f77b4"),
          ("ours", "ours: tree 4B, transformers, A10G", "#9ecae1")]
fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), sharey=True)
for ax, n_q in zip(axes, (1, 16)):
    for name, label, color in SERIES:
        pts = sorted({r["text_tokens"] for r in rows if r["endpoint"] == name})
        p50 = [statistics.median(r["wall_ms"] for r in rows if (r["endpoint"], r["text_tokens"], r["questions"]) == (name, n, n_q)) for n in pts]
        ax.plot(pts, p50, "o-", color=color, label=label, lw=2)
    ax.set_xscale("log", base=2)
    ax.set_xticks(pts, [f"{n:,}" for n in pts], rotation=45)
    ax.set_title(f"{n_q} question{'s' if n_q > 1 else ''} × 3 options")
    ax.set_xlabel("text length (tokens)")
    ax.grid(alpha=0.3)
axes[0].set_ylabel("latency p50 at the client (ms)")
axes[0].legend(loc="upper left")
fig.suptitle("End-to-end latency from a Mac in California (ours: 71 ms network to us-east-1 included)")
fig.tight_layout()
fig.savefig(OUT / "latency.png", dpi=150)
print(OUT / "latency.png")
