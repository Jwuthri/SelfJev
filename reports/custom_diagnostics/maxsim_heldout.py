"""Parameter-free MaxSim on held-out multiclass test families, using the SAME frozen features and standardization
as a custom checkpoint: score(candidate) = mean over its description tokens of the max cosine to any state token.
Compare with the trained custom model on the same questions (reports/<run>/test/report.json).

usage: HF_HUB_OFFLINE=1 .venv/bin/python reports/custom_diagnostics/maxsim_heldout.py runs/custom_frozen/checkpoint reports/custom_frozen/test/report.json
"""
import json
import sys
from collections import defaultdict

import torch
import torch.nn.functional as F

from personal_jev.custom import CustomScorer, candidate_texts, state_text
from personal_jev.data import load
from personal_jev.schemas import parse_question

N = 100  # questions per family
ck, report = sys.argv[1], json.load(open(sys.argv[2]))
trained = {r["id"]: r["correct"] for r in report["predictions"]}
sc = CustomScorer(ck, device="cpu", dtype="float32")
m, tok = sc.model, sc.tokenizer
by_fam = defaultdict(list)
for e in load("data/hf.jsonl", {"test"}):
    if e["question"]["type"] == "multiclass" and len(by_fam[e["family"]]) < N:
        by_fam[e["family"]].append(e)


@torch.no_grad()
def feats(text, kind):
    H, _ = m.hidden(sc.tokenize([text]), kind)  # standardized last hidden states, as the model sees them
    return H[0]


for fam, exs in sorted(by_fam.items()):
    ok = 0
    for e in exs:
        q = parse_question({"id": "q", **e["question"]})
        S = F.normalize(feats(state_text(e["state"]), "state")[1:], dim=-1)
        sims = []
        for text in candidate_texts(q):
            n_prefix = len(sc.tokenize([text.split("Proposed answer:")[0] + "Proposed answer:"])[0])
            C = F.normalize(feats(text, "candidate")[n_prefix:], dim=-1)
            sims.append((C @ S.T).max(1).values.mean().item())
        ok += q.candidates[max(range(len(sims)), key=sims.__getitem__)].id == e["target"]
    tr = [trained[e["id"]] for e in exs]
    print(f"{fam:28s} n={len(exs)}  MaxSim (no training) {100 * ok / len(exs):5.1f}%   trained custom model {100 * sum(tr) / len(tr):5.1f}%", flush=True)
