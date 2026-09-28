"""Build the HF card and figures from saved predictions; never loads a model.

Run: uv run --no-project --with matplotlib==3.11.1 python scripts/docs/build_model_card.py
Requires the canonical data/all.jsonl.gz. Generated assets ship alongside README.md on HF.
"""

import csv
import gzip
import hashlib
import json
import shutil
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from model_card_figures import architecture, latency

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "weights/selfjev_4b"
ASSETS = OUT / "assets"
BG, PANEL, FG, MUTED, GRID = "#111211", "#1c201b", "#eeeee7", "#a9afa1", "#343c32"
ORANGE, GREEN, BLUE = "#ff7547", "#bad68e", "#9eb9d3"
GH = "https://github.com/Jwuthri/SelfJev/blob/master/"
SOURCES = {}
FAMILIES = [
    ("heldout_intent_clinc", "CLINC150", "Intent routing", "held-out source"),
    ("heldout_topic_dbpedia", "DBpedia", "Topic classification", "held-out source"),
    ("heldout_question_type_trec", "TREC", "Question type", "held-out source"),
    ("heldout_emotion_multiclass", "Emotion", "Emotion classification", "held-out source"),
    ("heldout_boolq", "BoolQ", "Reading comprehension", "held-out source"),
    ("heldout_sentiment_sst2", "SST-2", "Sentiment", "held-out source"),
    ("hf_intent_banking77", "Banking77", "Banking intent", "seen source"),
    ("hf_topic_agnews", "AG News", "News topic", "seen source"),
    ("hf_sentiment_tweets", "TweetEval", "Tweet sentiment", "seen source"),
    ("hf_nli", "MNLI", "Entailment (binary)", "seen source"),
    ("hf_emotions_multilabel", "GoEmotions", "Emotion tags (exact set)", "seen source"),
]


def record(path):
    p = ROOT / path
    SOURCES[path] = hashlib.sha256(p.read_bytes()).hexdigest()
    return p


def report(run, split="test", ids=None):
    path = f"reports/{run}/{split}/report.json"
    d = json.loads(record(path).read_text())
    ps = {p["id"]: p for p in d["predictions"]}
    assert len(ps) == len(d["predictions"]) == d["meta"]["n"], path
    assert abs(sum(p["correct"] for p in ps.values()) / len(ps) - d["metrics"]["question_accuracy"]) < 1e-10, path
    if ids is not None:
        assert set(ids) <= ps.keys(), path
        ps = {i: ps[i] for i in ids}
    return ps, path


def accuracy(ps):
    return 100 * sum(p["correct"] for p in ps.values()) / len(ps)


def same_questions(a, b):
    assert a.keys() == b.keys()
    for i, p in a.items():
        q = b[i]
        assert p["target"] == q["target"] and p["type"] == q["type"], i
        assert set(p["candidate_ids"]) == set(q["candidate_ids"]), i


def frame(title, subtitle, height=6.8):
    fig = plt.figure(figsize=(14, height), facecolor=BG)
    fig.text(0.045, 0.94, "SELFJEV   /   RESEARCH NOTES", color=ORANGE, size=10, weight="bold")
    fig.text(0.045, 0.865, title, color=FG, size=24, weight="bold")
    fig.text(0.045, 0.81, subtitle, color=MUTED, size=11)
    return fig


def save(fig, name):
    for ext in ("png", "svg"):
        fig.savefig(ASSETS / f"{name}.{ext}", dpi=160, facecolor=BG, metadata={"Date": None} if ext == "svg" else None)
    plt.close(fig)


def axes_style(ax):
    ax.set_facecolor(BG)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(colors=MUTED, length=0, pad=8)
    ax.xaxis.label.set_color(MUTED)
    ax.yaxis.label.set_color(MUTED)
    ax.grid(axis="x", color=GRID, lw=0.7)
    ax.set_axisbelow(True)


def main():
    ASSETS.mkdir(exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "svg.fonttype": "none", "svg.hashsalt": "selfjev-model-card"})
    rows = defaultdict(dict)
    source = record("data/all.jsonl.gz")
    with gzip.open(source, "rt") as f:
        for line in f:
            r = json.loads(line)
            if r["dataset"] in {"hf", "eval2", "eval_llm"} and r["split"] == "test":
                assert r["id"] not in rows[r["dataset"]]
                rows[r["dataset"]][r["id"]] = r

    public, public_path = report("selfjev_4b_treeserver", ids=rows["hf"])
    jev, jev_path = report("external/full", "typesafe_jev-latest", ids=public)
    same_questions(public, jev)
    e2, e2_path = report("selfjev_4b_treeserver", "eval2")
    je2, je2_path = report("external/eval2", "typesafe_jev-latest")
    llm, llm_path = report("selfjev_4b_treeserver", "eval_llm")
    same_questions(e2, je2)
    for ds, ps in (("hf", public), ("eval2", e2), ("eval_llm", llm)):
        assert ps.keys() == rows[ds].keys()
        assert all(p["target"] == rows[ds][i]["target"] for i, p in ps.items())
    jllm = {i: r["jev"] for i, r in rows["eval_llm"].items()}
    assert len({p["model"] for p in jllm.values()}) == 1
    overview = [
        {"label": "Text decisions", "n": len(e2), "ours": accuracy(e2), "jev": accuracy(je2), "source": e2_path, "reference": je2_path},
        {
            "label": "AI response review",
            "n": len(llm),
            "ours": accuracy(llm),
            "jev": accuracy(jllm),
            "source": llm_path,
            "reference": "data/all.jsonl.gz: eval_llm / jev",
            "reference_model": next(iter(jllm.values()))["model"],
        },
        {
            "label": "Public-source tasks",
            "n": len(public),
            "ours": accuracy(public),
            "jev": accuracy(jev),
            "source": public_path,
            "reference": jev_path,
        },
    ]

    public_rows = []
    for family, label, task, exposure in FAMILIES:
        subset = {i: p for i, p in public.items() if p["family"] == family}
        ref = {i: jev[i] for i in subset}
        assert len(subset) == 300
        provenance = rows["hf"][next(iter(subset))]["provenance"]
        public_rows.append(
            {
                "family": family,
                "dataset": label,
                "task": task,
                "exposure": exposure,
                "n": len(subset),
                "ours": accuracy(subset),
                "jev": accuracy(ref),
                "dataset_url": "https://huggingface.co/datasets/" + provenance.split("hf:")[1].split("@")[0],
                "source": public_path,
                "reference": jev_path,
            }
        )
    assert sum(r["n"] for r in public_rows) == len(public)

    size_rows = []
    for run, size, label, regime in [
        ("baseline", 0.6, "Qwen3 reranker 0.6B", "stock"),
        ("baseline_4b", 4, "Qwen3 reranker 4B", "stock"),
        ("baseline_8b", 8, "Qwen3 reranker 8B", "stock"),
        ("lora_pilot", 0.6, "Qwen3 + LoRA 0.6B", "early fine-tune"),
        ("lora_4b", 4, "Qwen3 + LoRA 4B", "early fine-tune"),
        ("lora_8b", 8, "Qwen3 + LoRA 8B", "early fine-tune"),
        ("selfjev_4b_treeserver", 4, "SelfJev-4B", "current release"),
    ]:
        ps, path = report(run, ids=public)
        same_questions(public, ps)
        size_rows.append(
            {"model": label, "nominal_backbone_billions": size, "regime": regime, "accuracy": accuracy(ps), "n": len(ps), "source": path}
        )

    journey = []
    for run, label, split in [
        ("tree_4b", "Initial tree", "eval2"),
        ("tree_4b_r2b", "Verified hard cases", "eval2"),
        ("tree_4b_instruct_r2x64", "Instruct backbone", "eval2"),
        ("tree_4b_combo", "Broader data + options", "eval2"),
        ("qwen35_4b_tree", "Qwen3.5 + tree training", "eval2"),
        ("selfjev_4b_treeserver", "SelfJev / current engine", "eval2"),
    ]:
        ps, path = report(run, split)
        same_questions(e2, ps)
        journey.append({"model": label, "accuracy": accuracy(ps), "source": path, "n": len(ps)})
    eikos, eikos_path = report("eikos_4b", "eval2")
    same_questions(e2, eikos)

    # Hero: a diagram of the shared-prefix computation, not an inference trace.
    fig = plt.figure(figsize=(14, 4.6), facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=(0, 14), ylim=(0, 4.6))
    ax.axis("off")
    ax.text(0.6, 3.96, "SELFJEV / 4B", color=ORANGE, fontsize=13, weight="bold")
    ax.text(0.6, 3.18, "Read once.\nDecide across questions.", color=FG, fontsize=29, weight="bold", va="top")
    ax.text(0.6, 0.82, "YOUR TEXT  /  YOUR OPTIONS  /  YOUR GPU", color=MUTED, fontsize=10)

    def box(x, y, w, h, text, color=FG):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.13", facecolor=PANEL, edgecolor=GRID))
        ax.text(x + w / 2, y + h / 2, text, color=color, fontsize=11, ha="center", va="center", linespacing=1.6)

    box(7.1, 1.8, 1.7, 0.9, "Shared\ndocument", ORANGE)
    for y, label in [(3.35, "Route"), (2.05, "Verify"), (0.75, "Review")]:
        ax.add_patch(FancyArrowPatch((8.95, 2.25), (10, y + 0.23), arrowstyle="->", mutation_scale=10, color=ORANGE))
        box(10.1, y, 1.35, 0.46, label)
        for dy in [-0.16, 0.16]:
            ax.plot([11.6, 12.1, 12.6], [y + 0.23, y + 0.23 + dy, y + 0.23 + dy], color=GRID)
            ax.scatter([12.75], [y + 0.23 + dy], s=24, color=GREEN)
    ax.text(10.05, 0.17, "Questions       Candidate scores", color=MUTED, fontsize=9)
    save(fig, "hero")

    fig = frame("Three views of decision quality", "Current SelfJev engine and Jev on matching questions. Higher is better.")
    ax = fig.add_axes([0.235, 0.22, 0.65, 0.51])
    axes_style(ax)
    for i, r in enumerate(overview):
        y = 2 - i
        ax.barh(y + 0.15, r["ours"], 0.23, color=ORANGE, label="SelfJev-4B" if i == 0 else None)
        ax.barh(y - 0.15, r["jev"], 0.23, color=GREEN, label="Jev API" if i == 0 else None)
        ax.text(r["ours"] + 1, y + 0.15, f"{r['ours']:.1f}", color=ORANGE, va="center", weight="bold")
        ax.text(r["jev"] + 1, y - 0.15, f"{r['jev']:.1f}", color=GREEN, va="center")
    ax.set(
        xlim=(0, 108),
        xticks=[0, 25, 50, 75, 100],
        yticks=[2, 1, 0],
        yticklabels=[f"{r['label']}\n{r['n']:,} questions" for r in overview],
        xlabel="Question accuracy (%)",
    )
    ax.legend(loc="lower left", bbox_to_anchor=(0, 1.03), ncol=2, frameon=False, labelcolor=FG)
    fig.text(
        0.045,
        0.06,
        "Public-source tasks: our adapted development benchmark. Authored tests use AI-checked labels.\n"
        "Different suites measure different tasks; do not combine these scores into one ranking.",
        color=MUTED,
        size=10,
    )
    save(fig, "overview")

    fig = frame(
        "Public datasets, task by task",
        "11 sources · 300 adapted questions each · identical questions and answer sets for both models",
        9.5,
    )
    ax = fig.add_axes([0.23, 0.22, 0.51, 0.53])
    axes_style(ax)
    for i, r in enumerate(public_rows):
        y = 10 - i
        ax.plot([r["ours"], r["jev"]], [y, y], color=GRID, lw=3)
        ax.scatter(r["jev"], y, marker="s", s=38, color=GREEN, zorder=3)
        ax.scatter(r["ours"], y, marker="o", s=47, color=ORANGE, zorder=4)
        ax.text(106, y, f"{r['ours']:.1f}", color=ORANGE, va="center", ha="right")
        ax.text(121, y, f"{r['jev']:.1f}", color=GREEN, va="center", ha="right")
    ax.axhline(4.5, color=GRID, ls="--")
    ax.set(
        xlim=(0, 100),
        ylim=(-0.6, 11),
        xticks=[0, 25, 50, 75, 100],
        yticks=list(range(10, -1, -1)),
        yticklabels=[r["dataset"] for r in public_rows],
        xlabel="Accuracy / exact set match (%)",
    )
    ax.text(106, 10.85, "SelfJev", color=ORANGE, ha="right", fontsize=10, weight="bold")
    ax.text(121, 10.85, "Jev", color=GREEN, ha="right", fontsize=10, weight="bold")
    fig.text(
        0.045,
        0.095,
        "Above divider: sources excluded from task-specific training. Below: held-out rows from training sources.\n"
        "All rows belong to a reused development benchmark; these are not official full-dataset leaderboard scores.",
        color=MUTED,
        size=10,
    )
    save(fig, "public-datasets")

    fig = frame(
        "What does model size buy you?",
        "Same 3,300 public-source questions · our adapted development protocol · nominal backbone size",
        7.4,
    )
    ax = fig.add_axes([0.08, 0.24, 0.84, 0.49])
    axes_style(ax)
    styles = {"stock": (BLUE, "s"), "early fine-tune": (GREEN, "o"), "current release": (ORANGE, "*")}
    offsets = [(12, -17), (-12, -18), (-12, -18), (12, 9), (-15, -26), (-12, 10), (14, 11)]
    for r, offset in zip(size_rows, offsets):
        c, m = styles[r["regime"]]
        x, y = r["nominal_backbone_billions"], r["accuracy"]
        ax.scatter(x, y, s=200 if m == "*" else 65, marker=m, color=c, zorder=3)
        ax.annotate(
            f"{r['model']}  {y:.1f}%",
            (x, y),
            xytext=offset,
            textcoords="offset points",
            color=c,
            size=10,
            ha="right" if x == 8 or (x == 4 and m != "*") else "left",
            weight="bold" if m == "*" else "normal",
        )
    ax.axhline(accuracy(jev), color=MUTED, ls="--", lw=0.8)
    ax.text(0.35, accuracy(jev) + 0.5, f"Jev API {accuracy(jev):.1f}% · size undisclosed", color=MUTED, size=9)
    ax.set(
        xlim=(0.2, 8.8),
        ylim=(56, 91),
        xticks=[0.6, 2, 4, 6, 8],
        xlabel="Nominal backbone parameters (billions)",
        ylabel="Question accuracy (%)",
    )
    ax.grid(axis="y", color=GRID, lw=0.7)
    fig.text(0.08, 0.13, "■  Stock rerankers          ●  Earlier fine-tunes          ★  Current SelfJev", color=FG, size=10)
    fig.text(
        0.045,
        0.055,
        "Recipes, data and backbones differ: this is a comparison of measured systems, not a controlled scaling study.\n"
        "Parameter count includes the backbone; the 230 MB adapter is not the size of the complete model.",
        color=MUTED,
        size=10,
    )
    save(fig, "accuracy-size")

    fig = frame("How we arrived at SelfJev", "Selected research checkpoints · same 1,991 text-decision questions · accuracy (%)", 7.2)
    ax = fig.add_axes([0.31, 0.22, 0.57, 0.51])
    axes_style(ax)
    for i, r in enumerate(journey):
        c = ORANGE if i == len(journey) - 1 else GREEN
        ax.barh(5 - i, r["accuracy"], 0.5, color=c, alpha=1 if c == ORANGE else 0.75)
        ax.text(r["accuracy"] + 1, 5 - i, f"{r['accuracy']:.1f}", color=c, va="center", weight="bold")
    ax.set(xlim=(0, 105), xticks=[0, 25, 50, 75, 100], yticks=list(range(5, -1, -1)), yticklabels=[r["model"] for r in journey])
    fig.text(
        0.045,
        0.075,
        "These runs change multiple ingredients; differences are not isolated causal gains.\n"
        "The final point uses the current TreeServer. Earlier checkpoints use their recorded historical engines.",
        color=MUTED,
        size=10,
    )
    save(fig, "research-path")

    architecture(frame, save)
    latency_data, gpu_table, mac_table = latency(ASSETS, record, frame, save, axes_style)
    bundle = {
        "schema_version": 1,
        "overview": overview,
        "public_datasets": public_rows,
        "accuracy_vs_size": size_rows,
        "research_path": journey,
        "latency": latency_data,
        "external_text_decisions": {"model": "Eikos-4B", "accuracy": accuracy(eikos), "source": eikos_path},
        "provenance_sha256": SOURCES,
        "scope": "Saved results only. No new inference. Public datasets adapted; no S1Bench claim.",
    }
    (ASSETS / "chart-data.json").write_text(json.dumps(bundle, indent=2) + "\n")
    with (ASSETS / "public-datasets.csv").open("w") as f:
        writer = csv.DictWriter(f, fieldnames=list(public_rows[0]))
        writer.writeheader()
        writer.writerows(public_rows)

    public_table = "\n".join(
        f"| [{r['dataset']}]({r['dataset_url']}) | {r['task']} | {r['exposure']} | {r['n']} | {r['ours']:.1f}% | {r['jev']:.1f}% |"
        for r in public_rows
    )
    overview_table = "\n".join(
        f"| {r['label']} | {r['n']:,} | **{r['ours']:.1f}%** | {r['jev']:.1f}% | [report]({GH}{r['source']}) |" for r in overview
    )
    size_table = "\n".join(
        f"| {r['model']} | {r['nominal_backbone_billions']:g}B | {r['regime']} | {r['accuracy']:.1f}% | [report]({GH}{r['source']}) |"
        for r in size_rows
    )
    llm_table = []
    for slug, label in [
        ("verify", "Factual verification"),
        ("judge", "Response judging"),
        ("score", "Quality scoring"),
        ("guardrail", "Policy guardrails"),
        ("jailbreak", "Jailbreak detection"),
    ]:
        ps = {i: p for i, p in llm.items() if p["family"].startswith(f"tllm_{slug}_")}
        llm_table.append(f"| {label} | {len(ps)} | {accuracy(ps):.1f}% | {accuracy({i: jllm[i] for i in ps}):.1f}% |")
    card = (ROOT / "scripts/docs/model_card.template.md").read_text()
    for key, value in {
        "OVERVIEW": overview_table,
        "PUBLIC": public_table,
        "SIZE": size_table,
        "LLM": "\n".join(llm_table),
        "EIKOS": f"{accuracy(eikos):.1f}",
        "PUBLIC_SCORE": f"{accuracy(public):.1f}",
        "GPU_LATENCY": gpu_table,
        "MAC_LATENCY": mac_table,
    }.items():
        card = card.replace("{{" + key + "}}", value)
    assert "{{" not in card
    (OUT / "README.md").write_text(card)
    reproduce = OUT / "reproduce"
    reproduce.mkdir(exist_ok=True)
    for name in ("build_model_card.py", "model_card_figures.py", "model_card.template.md"):
        shutil.copyfile(ROOT / "scripts/docs" / name, reproduce / name)
    print(f"Built card, 8 figures (PNG + SVG), CSV and JSON; {len(SOURCES)} hashed sources; comparisons and latency samples checked.")


if __name__ == "__main__":
    main()
