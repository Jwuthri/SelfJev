"""Frozen-feature diagnostics behind the custom model's standardization and tied init (CPU, fp32, no training).

1. Anisotropy: mean pairwise cosine of state-token hidden states and the share of E|x|^2 in the mean direction.
2. Parameter-free MaxSim: score each candidate by the mean over its description tokens of the max cosine to any
   state token, and pick the argmax. Tells whether the features carry matching signal before any training.

usage: HF_HUB_OFFLINE=1 .venv/bin/python reports/custom_diagnostics/features.py > reports/custom_diagnostics/logs/features.log
"""
import random

import torch
import torch.nn.functional as F
from transformers import AutoModel, AutoTokenizer

from personal_jev.custom import TOKENIZE, candidate_texts, state_text
from personal_jev.data import load
from personal_jev.model import MODEL_ID, MODEL_REVISION
from personal_jev.schemas import parse_question

torch.manual_seed(0)
LAYERS = [8, 14, 20, 24, 28]  # 28 = last_hidden_state (after the final norm), the layer the custom model reads
tok = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION)
model = AutoModel.from_pretrained(MODEL_ID, revision=MODEL_REVISION, dtype=torch.float32).eval()


@torch.no_grad()
def feats(text):
    ids = tok(text, return_tensors="pt", **TOKENIZE)["input_ids"]
    out = model(input_ids=ids, output_hidden_states=True)
    hs = list(out.hidden_states)
    hs[28] = out.last_hidden_state
    return {k: hs[k][0] for k in LAYERS}


ex = load("data/hf.jsonl", {"train"})
random.Random(0).shuffle(ex)
X = torch.cat([feats(state_text(e["state"]))[28][1:] for e in ex[:40]])  # drop position 0
idx = torch.randperm(len(X))[:2000]
for name, Y in (("raw", X), ("standardized", (X - X.mean(0)) / X.std(0))):
    Yn = F.normalize(Y, dim=-1)[idx]
    share = (Y.mean(0).norm() ** 2 / (Y.norm(dim=-1) ** 2).mean()).item()
    print(f"last_hidden_state {name}: {len(X)} tokens, mean pairwise cosine {(Yn @ Yn.T).mean().item():.3f}, "
          f"mean-direction share of E|x|^2 {share:.3f}")

for fam in ("hf_intent_banking77", "hf_topic_agnews"):
    data = []
    for e in [e for e in load("data/hf.jsonl", {"validation"}) if e["family"] == fam][:40]:
        q = parse_question({"id": "q", **e["question"]})
        cands = []
        for text in candidate_texts(q):
            n_prefix = len(tok(text.split("Proposed answer:")[0] + "Proposed answer:", **TOKENIZE)["input_ids"])
            cands.append({k: v[n_prefix:] for k, v in feats(text).items()})  # description tokens only
        data.append((feats(state_text(e["state"])), cands, [c.id for c in q.candidates].index(e["target"])))
    for k in LAYERS:
        pool = torch.cat([d[0][k][1:] for d in data] + [c[k] for d in data for c in d[1]])
        mu, sd = pool.mean(0), pool.std(0)
        for name, f in (("raw", lambda x: x), ("standardized", lambda x: (x - mu) / sd)):
            correct = 0
            for s, cands, gold in data:
                S = F.normalize(f(s[k][1:]), dim=-1)
                sims = [(F.normalize(f(c[k]), dim=-1) @ S.T).max(1).values.mean().item() for c in cands]
                correct += max(range(len(sims)), key=sims.__getitem__) == gold
            print(f"{fam} layer {k} {name}: MaxSim zero-shot {correct}/{len(data)} (chance {len(data) / len(data[0][1]):.0f}/{len(data)})")
