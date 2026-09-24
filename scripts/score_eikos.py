"""Score Eikos-4B (caiovicentino1/Eikos-4B, MIT; Qwen3.5-4B full fine-tune, letter-logit readout) with our evaluator.

Eikos's own code (decision_core.py, letter_adapter.py, downloaded with the checkpoint) builds its prompt and reads the
letter probabilities; questions are mapped exactly as compare_external.py maps them for Jev: binary -> noul,
multiclass -> choice over candidate descriptions, multilabel -> one noul per candidate ("... Does this apply: X?").
Probabilities are turned back into scores (logit / log p) so classify.decide reproduces them at T = 1, threshold 0.5.
Zero-shot: nothing is fitted. GPU only (AGENTS.md: no model jobs on the laptop).

usage (on the GPU box): python scripts/score_eikos.py --data data/eval2.jsonl --out reports/eikos_4b/eval2
"""
import argparse, json, math, os, sys, time

from huggingface_hub import snapshot_download

REPO, REV = "caiovicentino1/Eikos-4B", "99336c237636288bcddc7f84a7adfc31b20acbd3"
NOUL = {"true": "Yes: the text supports this", "false": "No: the text contradicts this or does not say"}


def logit(p):
    p = min(max(p, 1e-6), 1 - 1e-6)
    return math.log(p / (1 - p))


class EikosScorer:
    def __init__(self, path):
        cfg = json.load(open(os.path.join(path, "decision_config.json")))
        os.environ["PROMPT_STYLE"] = cfg["prompt_version"].rsplit("-", 1)[-1]  # before decision_core is imported
        sys.path.insert(0, path)
        from decision_core import PROMPT_VERSION, options_of
        from letter_adapter import LetterAdapter
        self.options_of = options_of
        self.ad = LetterAdapter(path, device="cuda", max_tokens=40000)  # T = 1, as shipped (calib.json is identity)
        self.tokenizer = self.ad.load()[1]
        self.meta = {"model": REPO, "revision": REV, "adapter": None, "adapter_sha256": None, "device": "cuda",
                     "dtype": "bfloat16", "architecture": "Eikos letter readout (external open model)", "prompt": PROMPT_VERSION,
                     "prompt_sha": PROMPT_VERSION, "max_length": 40000, "truncation": "none"}

    def questions(self, q):
        """-> list of (eikos question, reader) where reader(probs) gives this question's score list parts."""
        if q.type == "binary":
            return [({"type": "noul", "instructions": q.instruction, "criteria": NOUL}, lambda p: [logit(p["yes"])])]
        if q.type == "multiclass":
            crit = {c.id: c.description for c in q.candidates}
            return [({"type": "choice", "instructions": q.instruction, "criteria": crit},
                     lambda p: [math.log(max(p[c.id], 1e-9)) for c in q.candidates])]
        return [({"type": "noul", "instructions": f"{q.instruction} Does this apply: {c.description}?", "criteria": NOUL},
                 lambda p: [logit(p["yes"])]) for c in q.candidates]

    def score_requests(self, reqs):
        """Questions of every request that share a text go through one dist_many_cached call (prefix computed once)."""
        t0 = time.perf_counter(); by_state = {}
        for ri, r in enumerate(reqs):
            for qi, q in enumerate(r.questions):
                for eq, reader in self.questions(q):
                    by_state.setdefault(r.state, []).append((ri, qi, eq, reader))
        per = [[[] for _ in r.questions] for r in reqs]; n = 0
        for state, group in by_state.items():
            res = self.ad.dist_many_cached(state, [(eq, self.options_of(eq)) for _, _, eq, _ in group])
            for (ri, qi, _, reader), (probs, _) in zip(group, res):
                per[ri][qi] += reader(probs)
            n += len(group)
        return per, {"pairs": n, "model_ms": 1e3 * (time.perf_counter() - t0), "tokenize_ms": 0.0}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", nargs="+", default=["data/eval2.jsonl"])
    ap.add_argument("--split")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    path = snapshot_download(REPO, revision=REV)
    from personal_jev import evaluate
    r = evaluate.run(EikosScorer(path), a.data, [a.split] if a.split else None, out_dir=a.out)
    print("EVAL eikos_4b", a.out, round(r["metrics"]["question_accuracy"], 4), flush=True)
