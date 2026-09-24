"""LinkedIn chart: question accuracy on the identical 3,471 test questions, read straight from the report files.

usage: uv run --with matplotlib python scripts/make_post_chart.py   -> docs/linkedin_accuracy.png (1200x1200)
If reports/lora_4b_r2/test exists (round 2), it is added as its own highlighted bar.
"""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SURFACE, INK, INK2, MUTED, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#c3c2b7"
ACCENT, OTHER = "#2a78d6", "#b4b2aa"  # reference palette: series-1 blue for ours; recessive gray for the rest

BARS = [  # (label, sublabel, report, highlighted); rows whose report is missing are skipped
    ("Qwen3-Reranker-4B", "open model, no training", "baseline_4b/test", False),
    ("Qwen3-Reranker-4B + LoRA", "trained in 42 min on 1 GPU", "lora_4b/test", True),
    ("Qwen3-Reranker-4B + LoRA, shared-prefix tree", "same training; text read once for all questions", "tree_4b/test", True),
    ("Qwen3-Reranker-4B + LoRA, round 2", "+ targeted hard cases", "lora_4b_r2/test", True),
    ("Shared-prefix tree, round 2", "+ targeted hard cases", "tree_4b_r2/test", True),
    ("Jev", "TypeSafe, via OpenRouter", "external/full/typesafe_jev-latest", False),
    ("GPT-6 Astra", "frontier LLM, reasoning low", "external/full/openai_gpt-6-astra", False),
]


def accuracy(rel):
    p = ROOT / "reports" / rel / "report.json"
    if not p.exists():
        return None
    r = json.loads(p.read_text())
    assert r["meta"]["n"] == 3471 or len(r["predictions"]) == 3471, f"{rel} is not the 3,471-question test set"
    return 100 * r["metrics"]["question_accuracy"]


rows = [(lab, sub, accuracy(rel), hi) for lab, sub, rel, hi in BARS]
rows = [r for r in rows if r[2] is not None]

plt.rcParams["font.family"] = ["Helvetica Neue", "Arial", "DejaVu Sans"]
fig = plt.figure(figsize=(6, 6), dpi=200, facecolor=SURFACE)
ax = fig.add_axes([0.07, 0.13, 0.86, 0.66], facecolor=SURFACE)
n, bar_h = len(rows), 0.46
for i, (lab, sub, val, hi) in enumerate(rows):
    y = n - 1 - i
    color = ACCENT if hi else OTHER
    r = 0.9  # rounded data end (x units), square at the baseline
    ax.add_patch(FancyBboxPatch((0, y - bar_h / 2), val, bar_h, boxstyle=f"round,pad=0,rounding_size={r}",
                                mutation_aspect=bar_h / 6, linewidth=0, facecolor=color))
    ax.add_patch(Rectangle((0, y - bar_h / 2), min(val, 3), bar_h, linewidth=0, facecolor=color))
    ax.text(val + 1.2, y, f"{val:.1f}%", va="center", ha="left", fontsize=13, fontweight="bold" if hi else "normal", color=INK)
    ax.text(0, y + bar_h / 2 + 0.08, lab, va="bottom", ha="left", fontsize=10, fontweight="bold" if hi else "normal", color=INK)
    ax.text(1.5, y - 0.02, sub, va="center", ha="left", fontsize=7.5, color="white" if hi else INK2)
ax.set_xlim(0, 100)
ax.set_ylim(-0.6, n - 0.25)
ax.axvline(0, color=AXIS, linewidth=1)
for s in ax.spines.values():
    s.set_visible(False)
ax.set_yticks([])
ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xticklabels(["0", "25", "50", "75", "100%"], fontsize=7.5, color=MUTED)
ax.tick_params(axis="x", length=0, pad=4)
ax.grid(axis="x", color="#e1e0d9", linewidth=0.8)
ax.set_axisbelow(True)

fig.text(0.07, 0.915, "Rebuilding Jev's idea in one day", fontsize=18, fontweight="bold", color=INK, ha="left")
fig.text(0.07, 0.868, "Accuracy on the same 3,471 classification questions", fontsize=10.5, color=INK, ha="left")
fig.text(0.07, 0.838, "Typed decisions (yes/no, pick one, pick many) straight from a model, no text generation.",
         fontsize=8.5, color=INK2, ha="left")
fig.text(0.07, 0.045, "Benchmark: 11 public datasets + an LLM-written test set of hard cases. Single run, own benchmark.\n"
         "LoRA = small adapter (0.3% of the weights) on a frozen open model.", fontsize=7, color=MUTED, ha="left", linespacing=1.5)
out = ROOT / "docs/linkedin_accuracy.png"
out.parent.mkdir(exist_ok=True)
fig.savefig(out, facecolor=SURFACE)
print(out, [(lab, round(val, 1)) for lab, _, val, _ in rows])
