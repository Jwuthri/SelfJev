"""Import the LocalLLaMA/typed-decisions TRAIN split (Apache-2.0) as batch `typed_decisions_train_v1` (raw sources).

Each case becomes one source: the dataset's `state` + `questions` go through the server's own Jev mapping
(selfjev.server.compat.to_native), so training sees exactly what serving sees (noul with criteria -> 2-way choice,
score -> choice over the levels). Targets are the dataset's gold `label`: the argmax of a ≈ 4B teacher's 3-sample mean
(its card), so NOT ground truth: `grow_batch.sh typed_decisions_train_v1 judge` re-labels every question blind with
GPT-6 Astra and `build` keeps only agreements (AGENTS.md: LLM labels are not ground truth). The test split is never read.

usage: uv run python scripts/data/import_typed_decisions.py   (then bash scripts/data/grow_batch.sh typed_decisions_train_v1 judge)
"""

import json
from pathlib import Path

import pyarrow.parquet as pq
from huggingface_hub import HfApi, hf_hub_download

from selfjev.data import expand_source, write_jsonl
from selfjev.server.compat import to_native
from selfjev.types import DecisionRequest

ROOT = Path(__file__).resolve().parents[2]
REPO = "LocalLLaMA/typed-decisions"
OUT = ROOT / "data/batches/typed_decisions_train_v1/raw/td.jsonl"


def target(qtype: str, label: str):
    return label == "true" if qtype == "binary" else label  # 2-way noul choice ids are "true"/"false"; score ids "0".."k"


def main():
    rev = HfApi().dataset_info(REPO).sha
    path = hf_hub_download(REPO, "all/train-00000-of-00001.parquet", repo_type="dataset", revision=rev)
    cases = pq.read_table(path).to_pylist()
    assert all(c["split"] == "train" for c in cases), "train split only"
    rows = []
    for c in cases:
        qs, gold = json.loads(c["questions"]), json.loads(c["gold"])
        native = to_native(DecisionRequest.model_validate({"model": "x", "state": json.loads(c["state"]), "questions": qs}))
        questions = []
        for q in native["questions"]:
            q = {k: v for k, v in q.items() if k != "id"} | {
                "target": target(q["type"], gold[q["id"]]["label"]),
                "hard_cases": ["json_record"],
                "notes": f"typed-decisions {q['id']}: teacher p(label) {max(gold[q['id']]['probabilities'].values()):.2f}",
            }
            questions.append(q)
        src = {
            "source_id": f"td-{c['id']}",
            "family": f"td_{c['workflow']}",
            "provenance": f"import:hf/{REPO}@{rev[:10]} train (Apache-2.0, teacher label, re-judged, len={len(native['state']) // 4})",
            "state": native["state"],
            "questions": questions,
        }
        expand_source(src)  # validates
        rows.append(src)
    write_jsonl(OUT, rows)
    print(f"{len(rows)} sources, {sum(len(r['questions']) for r in rows)} questions -> {OUT.relative_to(ROOT)} (rev {rev})")


if __name__ == "__main__":
    main()
