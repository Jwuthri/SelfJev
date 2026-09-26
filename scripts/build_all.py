"""All of our data in one file + a generated catalog.

  uv run python scripts/build_all.py

- data/all.jsonl.gz: every ORIGINAL question once (one JSON line per question, the usual schema) with one extra field,
  `dataset`. Derived views (option-list transforms, subsets, teacher labels, fixtures) are left out and listed in the
  catalog instead. Rows keep their own `split`: filter on it, and never train on `test` rows.
  Load: personal_jev.data.load(["data/all.jsonl.gz"]) or gzip + json. Rebuildable, so it is not tracked in git.
- `jev` field: Jev's prediction for the row (P(yes) or per-candidate probabilities, answer, confidence, correct, Jev
  version) from data/jev/predictions.jsonl (scripts/jev_predictions.py), only when the text and question are unchanged.
- data/README.md: the catalog (generated; edit DATASETS / DERIVED below, not the file).
"""
import gzip
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from personal_jev.data import load, sha256_file  # noqa: E402

# name, file, what it is, role, write-up
DATASETS = [
    ("hf", "data/hf.jsonl", "public human-labeled sets (Banking77, AG News, TweetEval, MNLI, CLINC150, DBpedia, TREC, emotion, BoolQ, SST-2, ...) in our schema",
     "training + dev-benchmark test", "docs/data.md"),
    ("synthetic", "data/synthetic.jsonl", "round 1: trap-heavy authored texts, 6 families (12 Claude Sonnet agents)", "training", "docs/data.md"),
    ("hardcases", "data/hardcases.jsonl", "round 2: verified hard cases (4 OpenRouter models + 8 Sonnet agents, blind Astra judge)", "training",
     "docs/hardcases_round2.md"),
    ("hardcases_r3", "data/hardcases_r3.jsonl", "round 3: verified hard cases (Luna, Gemini 3.8 Flash, Grok 4.7; blind Astra judge)", "training",
     "docs/data.md"),
    ("hardcases_llm", "data/hardcases_llm.jsonl", "LLM evaluation: score, judge, verify, guardrail, jailbreak (Luna, Gemini, Grok, DeepSeek; Astra judge; "
     "strict + safety-reviewed)", "training", "docs/llm_eval_data.md"),
    ("eval", "data/eval.jsonl", "authored evaluation set, 7 families (7 Claude Opus agents); its test split is part of the dev benchmark",
     "dev benchmark", "docs/data.md"),
    ("eval2", "data/eval2.jsonl", "FROZEN target-task test set (Opus 5.5, Kimi K3, GLM 5.3; two blind judges)", "frozen test",
     "data/eval2/REVIEW.md"),
    ("eval_llm", "data/eval_llm.jsonl", "FROZEN LLM-evaluation test set (Opus 5.5, Kimi K3, GLM 5.3; Astra + Sonnet 5)", "frozen test",
     "docs/llm_eval_data.md"),
    ("compact_challenge_v1", "data/compact_challenge_v1.jsonl", "FROZEN programmatic challenge: explicit-record reasoning with evidence/absence "
     "contrasts (Codex session)", "frozen test", "scripts/build_compact_challenge.py"),
]
TEST_DATASETS = {"eval", "eval2", "eval_llm", "compact_challenge_v1"}  # never train on these (eval: dev-benchmark validation/test)


def datasets():
    """DATASETS + every grown batch: data/batches/<name>.jsonl (training data; description = first line of
    data/batches/<name>/README.md). A batch needs no edit here: build it and rerun this script."""
    out = list(DATASETS)
    for f in sorted((ROOT / "data/batches").glob("*.jsonl")):
        readme = f.parent / f.stem / "README.md"
        what = next((l.strip("# ").strip() for l in readme.read_text().splitlines() if l.strip()), "") if readme.exists() else ""
        out.append((f.stem, f"data/batches/{f.name}", f"batch: {what or 'no README.md yet'}", "training",
                    f"data/batches/{f.stem}/README.md"))
    return out


# left out of all.jsonl.gz on purpose: path, what it is
DERIVED = [
    ("data/hardcases_nb.jsonl", "round 2 with `none`-correct capped at 10% (round 2b; a subset of hardcases)"),
    ("data/ova/*.jsonl", "every option listed in the question (the transform the best models train and serve with); `scripts/options_in_question.py`"),
    ("data/ptr/*.jsonl", "option pointers (\"option k\"), a dead end; `scripts/options_in_question.py`"),
    ("data/curve/boolq_{100,300,1000,3000}.jsonl", "BoolQ train-split questions for the learning-curve runs only: BoolQ is a held-out family "
     "of the dev benchmark, so these never enter the combined file"),
    ("data/distill.jsonl", "teacher labels from the 0.6B reranker (not ground truth), custom-model distillation"),
    ("data/teacher/", "Qwen3.8-27B soft scores on the training split (distillation experiments)"),
    ("data/dev.jsonl", "14-text fixtures for unit tests"),
    ("data/*/raw/, data/*/review/", "per-writer source files, judge answers, agreement reports (inputs of the builds above)"),
]


def request_sha(ex):
    """Identifies the text + question a stored prediction was made for."""
    return hashlib.sha1(json.dumps([ex["state"], ex["question"]], sort_keys=True).encode()).hexdigest()[:16]


def main():
    out, stats, total = ROOT / "data/all.jsonl.gz", [], 0
    seen = set()
    jp = ROOT / "data/jev/predictions.jsonl"
    jev = {r["id"]: r for r in map(json.loads, open(jp))} if jp.exists() else {}
    with gzip.open(out, "wt", encoding="utf-8") as f:
        for name, path, *_ in datasets():
            rows = load([ROOT / path])
            dup = seen & {r["id"] for r in rows}
            if dup:
                sys.exit(f"{path}: {len(dup)} ids already in another dataset, e.g. {sorted(dup)[:3]}")
            seen |= {r["id"] for r in rows}
            for r in rows:
                p = jev.get(r["id"])
                if p and p["request"] == request_sha(r):
                    r["jev"] = {k: v for k, v in p.items() if k not in ("id", "dataset", "request")}
                f.write(json.dumps({"dataset": name, **r}, ensure_ascii=False) + "\n")
            total += len(rows)
            stats.append((name, rows, sha256_file(ROOT / path)))
            print(f"{name}: {len(rows)} questions", flush=True)

    def jev_cell(rows):
        j = [r["jev"]["correct"] for r in rows if "jev" in r]
        return f"{len(j):,} / {100 * sum(j) / len(j):.1f}%" if j else "—"

    def fmt(c):
        return ", ".join(f"{k} {v:,}" for k, v in c.most_common())

    lines = [
        "# Our data", "",
        "Generated by `uv run python scripts/build_all.py` (edit the lists in that script, not this file). "
        "Every row is one question about one text: `id`, `source_id`, `family`, `split`, `provenance`, `state`, "
        "`question` (`type`, `instruction`, `candidates`), `target`, `hard_cases`; schema and labeling policy in "
        "[docs/data.md](../docs/data.md).", "",
        f"**All original questions in one file: `data/all.jsonl.gz`**: {total:,} questions from {len(stats)} datasets, "
        "each row tagged with `dataset`. Built locally by the command above (not tracked in git). Load it with "
        "`personal_jev.data.load([\"data/all.jsonl.gz\"])`, then filter on `dataset` and `split`.", "",
        "**Jev's prediction** is stored on each row it exists for, as `jev`: `p_yes` (binary) or `probs` per candidate, `answer`, "
        "`confidence`, `correct` (vs `target`), `model` (Jev version). Source: `data/jev/predictions.jsonl` "
        "(`scripts/jev_predictions.py`). Jev's outputs never replace `target`.", "",
        "**Rules:** never train on, or tune anything on, `test` rows. `eval2`, `eval_llm` and `compact_challenge_v1` are frozen test sets. "
        "The `test` rows of `hf` and `eval` form the development benchmark (3,471 questions), reused for many decisions.", "",
        "## Always use this file", "",
        "Every training mix, evaluation and analysis starts from `data/all.jsonl.gz` (run the build command if it is missing):", "",
        "```python",
        "from personal_jev.data import load",
        "rows = load([\"data/all.jsonl.gz\"])",
        "TEST = {\"eval\", \"eval2\", \"eval_llm\", \"compact_challenge_v1\"}          # scripts/build_all.py TEST_DATASETS",
        "train = [r for r in rows if r[\"dataset\"] not in TEST and r[\"split\"] == \"train\"]",
        "val   = [r for r in rows if r[\"dataset\"] not in TEST and r[\"split\"] == \"validation\"]",
        "eval2 = [r for r in rows if r[\"dataset\"] == \"eval2\"]                    # frozen: report only",
        "teacher = [r[\"jev\"] for r in train if \"jev\" in r]                     # Jev's probabilities, never the label",
        "```", "",
        "Recipes on top (not baked into the file): the best models cap `none`-correct round-2 questions at 10% "
        "(`scripts/rebalance_nota.py`), list every option in the question (`scripts/options_in_question.py`, also at serving "
        "time) and cap public families at 1,600 questions ([docs/data.md](../docs/data.md#the-training-mixes)).", "",
        "## Grow it: add a batch, never a new stand-alone dataset", "",
        "1. **Write** into a named batch (any brief/mode flag works; one run per writer model; each paid run needs the user's OK "
        "with a price): `zsh -ic 'uv run python scripts/gen_hardcases.py --batch <name> --model <writer> --budget <usd> [--usecases train | --round3]'`. "
        "Balance and variety come from the generator (tiers, text lengths 8 to 8K tokens, traps, instruction styles). "
        "Default writers: GPT-6 Luna and Gemini 3.8 Flash. Not Grok 4.7 (mandatory hidden reasoning, ~20K output tokens per call, "
        "2-3x the cost per kept question), not DeepSeek V4 Flash (74% judge agreement), never the test sets' writers (Opus, "
        "Kimi, GLM). No third writer for now (user, 2026-09-26). Gemini at half price: "
        "`zsh -ic 'uv run python scripts/gen_gemini_batch.py submit --batch <name> --calls <n> [same mode flags]'`, then "
        "`... collect --batch <name> --wait` (Google Batch API, up to 24 h; plan balanced up front).",
        "2. **Judge** blind: `bash scripts/grow_batch.sh <name> judge` (GPT-6 Astra batch, ≈ $4 per 1K questions).",
        "3. **Build and screen**: `bash scripts/grow_batch.sh <name> build`: strict build (a text is dropped when any of its "
        "questions is flagged), overlap guard against every test set, OpenAI moderation screen (free). Read the flagged texts "
        "and delete unsafe ones from `data/batches/<name>/raw/` (rules: [docs/llm_eval_data.md](../docs/llm_eval_data.md)), then "
        "rerun `build`. Write one line describing the batch in `data/batches/<name>/README.md`.",
        "4. **Finish**: `bash scripts/grow_batch.sh <name> finish`: Jev's predictions for the new questions (≈ $0.03 per 1K) "
        "and a rebuild of `data/all.jsonl.gz` and this catalog. The batch is now part of the file under `dataset = <name>`.", "",
        "New frozen test sets are the exception: built on purpose with other writers and two judges (like `eval_llm`), then "
        "added to `DATASETS` and `TEST_DATASETS` in `scripts/build_all.py`.", "",
        "## Datasets in all.jsonl.gz", "",
        "| dataset | file | what | used as | questions | texts | splits | types | Jev: have / accuracy | write-up |",
        "|---|---|---|---|---|---|---|---|---|---|"]
    for (name, path, what, role, doc), (_, rows, sha) in zip(datasets(), stats):
        lines.append(f"| **{name}** | `{path}` | {what} | {role} | {len(rows):,} | {len({r['source_id'] for r in rows}):,} | "
                     f"{fmt(Counter(r['split'] for r in rows))} | {fmt(Counter(r['question']['type'] for r in rows))} | "
                     f"{jev_cell(rows)} | [link](../{doc}) |")
    by_split = Counter(r["split"] for _, rows, _ in stats for r in rows)
    lines += [f"| **total** | `data/all.jsonl.gz` | | | **{total:,}** | | {fmt(by_split)} | | {jev_cell([r for _, rows, _ in stats for r in rows])} | |", "",
              "## Left out on purpose (derived views, subsets, non-ground-truth labels, fixtures)", "",
              "| path | what |", "|---|---|"]
    lines += [f"| `{p}` | {w} |" for p, w in DERIVED]
    lines += ["", "## sha256 of the source files", ""] + [f"- `{path}`: `{sha[:16]}…`" for (_, path, *_), (_, _, sha) in zip(datasets(), stats)]
    (ROOT / "data/README.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {out} ({total} questions, {out.stat().st_size / 1e6:.0f} MB) and data/README.md")


if __name__ == "__main__":
    main()
