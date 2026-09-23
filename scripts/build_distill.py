"""data/distill.jsonl: extra multiclass TRAINING questions labeled by our own stock reranker + LoRA (teacher).

Why: trained on ~120 recurring label concepts, the custom model learns label-specific shortcuts and fails on
unseen label sets (reports/custom_diagnostics/). Here every training state gets a question whose candidates are
drawn from the descriptions of *all* training families, so answering needs generic description-to-text matching.

- States: train-split states of the given files only. Candidates: 2 descriptions from the state's own family (a
  likely positive) + 4 from other families, all from train-split questions; descriptions that also occur in any
  held-out/test family are excluded, so no held-out label enters training.
- Teacher: the local stock reranker with the LoRA pilot adapter (bf16); nothing leaves this machine.
- Kept only if the teacher's max probability >= --min-p. Teacher labels are NOT ground truth: provenance says so.

usage: HF_HUB_OFFLINE=1 .venv/bin/python scripts/build_distill.py [--min-p 0.7]
"""
import argparse
import random
from collections import Counter, defaultdict

from personal_jev.classify import classify_many
from personal_jev.data import load, write_jsonl
from personal_jev.model import Scorer

ap = argparse.ArgumentParser()
ap.add_argument("--train", nargs="+", default=["data/hf.jsonl", "data/synthetic.jsonl"])
ap.add_argument("--adapter", default="runs/lora_pilot/adapter")
ap.add_argument("--min-p", type=float, default=0.7)
ap.add_argument("--out", default="data/distill.jsonl")
ap.add_argument("--seed", type=int, default=7)
a = ap.parse_args()
rng = random.Random(a.seed)
INSTRUCTIONS = ["Which of these descriptions best fits the text?", "Which of these statements best matches the message?",
                "Which option best describes what the text is about?"]

train = load(a.train, {"train"})
excluded = {c["description"] for e in load(a.train + ["data/eval.jsonl"]) if e["split"] != "train" and
            (e["family"].startswith("heldout") or e["family"].startswith("eval"))
            for c in e["question"].get("candidates") or []}
pool = defaultdict(set)
for e in train:
    pool[e["family"]] |= {c["description"] for c in e["question"].get("candidates") or []} - excluded
pool = {f: sorted(d) for f, d in pool.items() if d}
everything = sorted({(f, d) for f, ds in pool.items() for d in ds})
states = {}
for e in train:  # one distillation question per distinct training state
    states.setdefault(e["state"], e)

rows, requests = [], []
for state, e in states.items():
    own = rng.sample(pool.get(e["family"], []), min(2, len(pool.get(e["family"], []))))
    others = [d for f, d in rng.sample(everything, 12) if f != e["family"] and d not in own][:6 - len(own)]
    cands = [{"id": f"c{i}", "description": d} for i, d in enumerate(own + others)]
    rng.shuffle(cands)
    q = {"type": "multiclass", "instruction": rng.choice(INSTRUCTIONS), "candidates": cands}
    rows.append((e, q))
    requests.append({"state": state, "questions": [{"id": "q", **q}]})

scorer = Scorer(adapter=a.adapter, dtype="bfloat16", max_length=4096)
results, _ = classify_many(scorer, requests)
out, kept = [], Counter()
for (e, q), [res] in zip(rows, results):
    p = max(c["probability"] for c in res["candidates"])
    if p < a.min_p:
        continue
    kept[e["family"]] += 1
    out.append({"id": f"{e['source_id']}-distill", "source_id": e["source_id"], "family": f"distill_{e['family']}", "split": "train",
                "provenance": f"teacher:{scorer.meta['model']}@{scorer.meta['revision'][:10]}+{a.adapter} (adapter sha256 "
                              f"{scorer.meta['adapter_sha256'][:12]}, bf16) max p {p:.3f}; candidates sampled from train-split "
                              f"descriptions (seed {a.seed}); teacher label, not ground truth",
                "state": e["state"], "question": q, "target": res["selected"]})
write_jsonl(a.out, out)
print(f"{len(out)} of {len(rows)} questions kept (teacher max p >= {a.min_p}); by source family {dict(sorted(kept.items()))}; "
      f"pool {len(everything)} descriptions, {len(excluded)} held-out/eval descriptions excluded")
