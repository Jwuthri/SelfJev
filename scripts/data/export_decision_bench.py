"""Export only the three frozen authored suites from the canonical corpus; never change their labels.

uv run --no-project --with datasets python scripts/data/export_decision_bench.py --out runs/decision-bench
"""

import argparse
import gzip
import hashlib
import json
import shutil
from collections import Counter
from pathlib import Path

from datasets import Dataset, Features, List, Value

ROOT = Path(__file__).resolve().parents[2]
SUITES = {
    "eval2": ("text-decisions", 1991),
    "eval_llm": ("ai-response-review", 946),
    "compact_challenge_v1": ("record-reasoning", 720),
}


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    out = args.out
    for folder in ("data", "selfjev", "tools"):
        (out / folder).mkdir(parents=True, exist_ok=True)
    corpus = ROOT / "data/all.jsonl.gz"
    with gzip.open(corpus, "rt", encoding="utf-8") as stream:
        all_rows = [json.loads(line) for line in stream]
    training_texts = {
        hashlib.sha256(r["state"].encode()).hexdigest() for r in all_rows if r["split"] != "test" and r["dataset"] not in {*SUITES, "eval"}
    }
    features = Features(
        {
            **{
                k: Value("string")
                for k in (
                    "id",
                    "source_id",
                    "suite",
                    "original_dataset",
                    "family",
                    "split",
                    "state",
                    "question_type",
                    "instruction",
                    "question_json",
                    "provenance",
                    "notes",
                    "paraphrase_group",
                )
            },
            "candidates": List({"id": Value("string"), "description": Value("string")}),
            "answer": List(Value("string")),
            "hard_cases": List(Value("string")),
        }
    )
    stats = {}
    for original, (suite, expected) in SUITES.items():
        rows = [{k: v for k, v in r.items() if k != "jev"} for r in all_rows if r["dataset"] == original]
        assert len(rows) == expected and len({r["id"] for r in rows}) == expected
        assert all(r["split"] == "test" for r in rows)
        assert not any(hashlib.sha256(r["state"].encode()).hexdigest() in training_texts for r in rows)
        normalized = []
        for r in rows:
            q, target = r["question"], r["target"]
            answer = [str(target).lower()] if isinstance(target, bool) else [target] if isinstance(target, str) else target
            normalized.append(
                {
                    **{k: r[k] for k in ("id", "source_id", "family", "split", "state", "provenance")},
                    "suite": suite,
                    "original_dataset": original,
                    "question_type": q["type"],
                    "instruction": q["instruction"],
                    "candidates": q.get("candidates", []),
                    "answer": answer,
                    "question_json": json.dumps(q, ensure_ascii=False, sort_keys=True),
                    "hard_cases": r.get("hard_cases", []),
                    "notes": r.get("notes", ""),
                    "paraphrase_group": r.get("paraphrase_group", ""),
                }
            )
        dataset = Dataset.from_list(normalized, features=features)
        dataset.to_parquet(out / "data" / f"{suite}.parquet")
        # Deterministic gzip; original types, IDs, texts, labels and question dictionaries survive unchanged.
        payload = "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows).encode()
        (out / "selfjev" / f"{suite}.jsonl.gz").write_bytes(gzip.compress(payload, mtime=0))
        stats[suite] = {
            "original_dataset": original,
            "questions": len(rows),
            "texts": len({r["source_id"] for r in rows}),
            "types": dict(Counter(r["question"]["type"] for r in rows)),
            "families": dict(sorted(Counter(r["family"] for r in rows).items())),
            "source_file_sha256": digest(ROOT / "data" / f"{original}.jsonl"),
            "exact_text_matches_in_non_test_training_rows": 0,
        }
    shutil.copyfile(ROOT / "scripts/data/score_decision_bench.py", out / "tools/score.py")
    shutil.copyfile(Path(__file__), out / "tools/export_from_selfjev.py")
    manifest = {
        "version": "1.0",
        "source": "data/all.jsonl.gz",
        "source_sha256": digest(corpus),
        "excluded_fields": ["jev"],
        "suites": stats,
        "overlap_check": "Exact state SHA-256 against all non-test rows of training datasets; not a new fuzzy-overlap audit.",
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    shutil.copyfile(ROOT / "docs/decision_bench_card.md", out / "README.md")
    files = sorted(p for p in out.rglob("*") if p.is_file() and p.name != "SHA256SUMS" and ".cache" not in p.parts)
    (out / "SHA256SUMS").write_text("".join(f"{digest(p)}  {p.relative_to(out).as_posix()}\n" for p in files))
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
