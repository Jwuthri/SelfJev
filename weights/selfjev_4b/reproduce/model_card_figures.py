"""Architecture and latency figures for the model cards; saved measurements only."""

import csv
import json
import math
from statistics import median

from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib.ticker import ScalarFormatter

BG, PANEL, FG, MUTED, GRID = "#111211", "#1c201b", "#eeeee7", "#a9afa1", "#343c32"
ORANGE, GREEN, BLUE = "#ff7547", "#bad68e", "#9eb9d3"


def architecture(frame, save):
    fig = frame("One document. Many decisions.", "The shared-prefix tree used in SelfJev training and the TreeServer engine", 8.4)
    ax = fig.add_axes([0.035, 0.18, 0.93, 0.56])
    ax.set(xlim=(0, 14), ylim=(0, 5.5))
    ax.axis("off")

    def box(x, y, w, h, label, color=FG):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.12", facecolor=PANEL, edgecolor=GRID))
        ax.text(x + w / 2, y + h / 2, label, color=color, size=11, ha="center", va="center", linespacing=1.5)

    def arrow(a, b, color):
        ax.add_patch(FancyArrowPatch(a, b, arrowstyle="->", mutation_scale=13, color=color, lw=1.7))

    for x, label in [(0.15, "01 / READ ONCE"), (4.0, "02 / ASK QUESTIONS"), (7.5, "03 / SCORE OPTIONS"), (11.0, "04 / RETURN")]:
        ax.text(x, 5.25, label, color=MUTED, size=9, weight="bold")
    box(0.2, 2.0, 2.6, 1.2, "System prompt\n+ your document", ORANGE)
    ax.text(1.5, 1.6, "Shared prefix", color=ORANGE, size=10, ha="center")
    for qy, label, options in [(4.0, "Which team?", ["Billing", "Support"]), (1.75, "Which priority?", ["Normal", "Urgent"])]:
        arrow((2.95, 2.6), (3.8, qy), ORANGE)
        box(4, qy - 0.43, 2.5, 0.86, label + "\n" + " / ".join(options))
        for cy, option in zip([qy + 0.53, qy - 0.53], options):
            arrow((6.66, qy), (7.35, cy), GREEN)
            box(7.5, cy - 0.26, 1.8, 0.52, option, GREEN)
            arrow((9.46, cy), (10.8, qy), GREEN)
        box(11, qy - 0.43, 2.5, 0.86, "Option probabilities\n+ selected answer")
    ax.text(4, 0.25, "Each question reuses\nthe document computation", color=MUTED, size=10, linespacing=1.5)
    ax.text(7.5, 0.25, "Each option reuses\nits question prefix", color=MUTED, size=10, linespacing=1.5)
    fig.text(0.05, 0.115, "ATTENTION", color=ORANGE, size=10, weight="bold")
    fig.text(0.05, 0.075, "Branches see their ancestors, not their siblings.", color=FG, size=11)
    fig.text(0.55, 0.115, "DELTANET", color=GREEN, size=10, weight="bold")
    fig.text(0.55, 0.075, "Branches inherit their parent's recurrent state.", color=FG, size=11)
    fig.text(
        0.05, 0.028, "Schematic choice questions; no measured output shown. vLLM uses its own prefix-cache execution.", color=MUTED, size=9
    )
    save(fig, "prefix-tree")


def latency(assets, record, frame, save, axes_style):
    rows = []
    sources = [
        ("A10G", "reports/latency/requests_combo.jsonl", "combo_vllm"),
        ("L40S", "reports/latency/requests_qwen35.jsonl", "combo_vllm_l40s"),
        ("H100", "reports/latency/requests_h100.jsonl", "h100_bf16"),
    ]
    for gpu, path, endpoint in sources:
        samples = [json.loads(line) for line in record(path).read_text().splitlines()]
        for questions in (1, 16):
            for tokens in (8, 512, 2048, 4096):
                selected = [
                    r
                    for r in samples
                    if r["endpoint"] == endpoint and r["text_tokens"] == tokens and r["questions"] == questions and r["rep"] > 0
                ]
                assert len(selected) == 10 and all(r["status"] == 200 for r in selected), (gpu, tokens, questions)
                values = [r["server_ms"] for r in selected]
                assert all(math.isfinite(t) and t > 0 for t in values)
                rows.append(
                    {
                        "hardware": gpu,
                        "model": "tree_4b_combo (archived Qwen3-4B)",
                        "engine": "vLLM bf16",
                        "text_tokens": tokens,
                        "questions": questions,
                        "candidates_per_question": 3,
                        "timed_calls": 10,
                        "metric": "server_ms",
                        "median_ms": median(values),
                        "wall_median_ms": median(r["wall_ms"] for r in selected),
                        "samples_ms": values,
                        "source": path,
                        "endpoint": endpoint,
                    }
                )

    path = "reports/latency/mac_m5_pro_selfjev4b.json"
    mac = json.loads(record(path).read_text())
    assert mac["meta"]["model"]["adapter_sha256"] == "dfbf2834d883987893ec305a6093a345fd79c77f903f60f2f914cbe3b6058d1b"
    assert mac["meta"]["model"]["device"] == "mps" and mac["meta"]["reps"] == 10
    mac_rows = []
    for cell in mac["cells"]:
        values = cell["samples_ms"]
        assert len(values) == 10 and abs(median(values) - cell["median_ms"]) < 0.01
        assert cell["candidates_per_question"] == 3 and all(math.isfinite(t) and t > 0 for t in values)
        mac_rows.append(
            {
                "hardware": "Apple M5 Pro / 48 GB",
                "model": "SelfJev-4B (current adapter)",
                "engine": "TreeServer / MPS bf16",
                "text_tokens": cell["text_tokens"],
                "questions": cell["questions"],
                "candidates_per_question": 3,
                "timed_calls": 10,
                "metric": "local_call_ms",
                "median_ms": median(values),
                "wall_median_ms": None,
                "samples_ms": values,
                "source": path,
                "endpoint": "TreeServer.score_requests",
            }
        )
    assert {(r["text_tokens"], r["questions"]) for r in mac_rows} == {(8, 1), (8, 16), (512, 1), (512, 16)}

    fig = frame("Measured on NVIDIA GPUs", "Earlier Qwen3 prototype · tree_4b_combo · vLLM bf16 · not current SelfJev-4B timings", 7.6)
    for j, questions in enumerate((1, 16)):
        ax = fig.add_axes([0.085 + 0.47 * j, 0.26, 0.38, 0.43])
        axes_style(ax)
        for (gpu, _, _), color, marker in zip(sources, (BLUE, GREEN, ORANGE), ("s", "^", "o")):
            cells = [r for r in rows if r["hardware"] == gpu and r["questions"] == questions]
            ax.plot([r["text_tokens"] for r in cells], [r["median_ms"] for r in cells], color=color, marker=marker, lw=2, label=gpu)
        ax.set_yscale("log")
        ax.set(
            ylim=(15, 1600),
            xlim=(-100, 4300),
            xticks=[8, 512, 2048, 4096],
            xticklabels=["8", "512", "2,048", "4,096"],
            yticks=[20, 50, 100, 250, 500, 1000],
            xlabel="Text tokens",
        )
        ax.yaxis.set_major_formatter(ScalarFormatter())
        ax.minorticks_off()
        ax.grid(axis="y", color=GRID, lw=0.7)
        ax.set_title(f"{questions} question{'s' if questions > 1 else ''} · 3 options each", color=FG, fontsize=13, pad=14)
        if j == 0:
            ax.set_ylabel("Median server time (ms, log scale)")
            ax.legend(loc="upper left", frameon=False, labelcolor=FG, fontsize=10)
    fig.text(0.045, 0.12, "10 warmed requests per point, one request at a time. Network excluded. Lower is faster.", color=FG, size=11)
    fig.text(
        0.045,
        0.065,
        "The three GPU sweeps were recorded separately with the same archived model and request shapes.\n"
        "These results cannot establish latency for the current Qwen3.5 checkpoint or a hardware-only comparison with MPS.",
        color=MUTED,
        size=10,
    )
    save(fig, "latency-gpu")

    fig = frame(
        "Current SelfJev on Apple Silicon", "Apple M5 Pro · 20-core GPU · 48 GB unified memory · TreeServer / PyTorch MPS bf16", 6.9
    )
    ax = fig.add_axes([0.24, 0.25, 0.66, 0.45])
    axes_style(ax)
    mac_rows.sort(key=lambda r: (r["text_tokens"], r["questions"]))
    for i, r in enumerate(mac_rows):
        ax.barh(3 - i, r["median_ms"], 0.52, color=ORANGE if r["questions"] == 1 else GREEN)
        ax.text(r["median_ms"] + 120, 3 - i, f"{r['median_ms']:,.0f} ms", color=FG, va="center", weight="bold")
    ax.set(
        xlim=(0, 10200),
        xticks=[0, 2000, 4000, 6000, 8000, 10000],
        yticks=[3, 2, 1, 0],
        yticklabels=[f"{r['text_tokens']} text tokens\n{r['questions']} question{'s' if r['questions'] > 1 else ''}" for r in mac_rows],
        xlabel="Median local call time (ms)",
    )
    fig.text(
        0.045,
        0.105,
        "10 timed calls after 2 warmups · 3 options per question · synthetic repeated text · MPS synchronized",
        color=FG,
        size=10,
    )
    fig.text(
        0.045,
        0.052,
        "Includes tokenization and model work; excludes HTTP/network. Uses the slower PyTorch recurrence fallback.\n"
        "A lower-level engine experiment, not a validated Mac server or a comparison against the archived NVIDIA model.",
        color=MUTED,
        size=10,
    )
    save(fig, "latency-mac")

    payload = {
        "gpu": rows,
        "mac": mac_rows,
        "mac_meta": mac["meta"],
        "scope": "Different models and engines. No current-model NVIDIA measurement. No new inference.",
    }
    (assets / "latency-data.json").write_text(json.dumps(payload, indent=2) + "\n")
    with (assets / "latency-data.csv").open("w") as f:
        writer = csv.DictWriter(f, fieldnames=[key for key in rows[0] if key != "samples_ms"])
        writer.writeheader()
        writer.writerows({key: value for key, value in row.items() if key != "samples_ms"} for row in rows + mac_rows)
    gpu_table = []
    for questions in (1, 16):
        for tokens in (8, 512, 2048, 4096):
            selected = [r for r in rows if r["questions"] == questions and r["text_tokens"] == tokens]
            cells = " | ".join(f"{r['median_ms']:,.0f} ms" for r in selected)
            gpu_table.append(f"| {tokens:,} | {questions} | {cells} |")
    mac_table = [f"| {r['text_tokens']} | {r['questions']} | {r['median_ms']:,.0f} ms |" for r in mac_rows]
    return payload, "\n".join(gpu_table), "\n".join(mac_table)
