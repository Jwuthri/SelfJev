"""Content-safety screen of generated sources with OpenAI's moderation endpoint (free).

  zsh -ic 'uv run python scripts/moderate_texts.py data/hardcases_llm/raw data/eval_llm/raw --out reports/hardcases_llm/moderation.jsonl'

Each source = state + every instruction and candidate description, split into <= 8,000-character pieces; a source's
score per category is its max over pieces. Writes one row per source {source_id, file, flagged, scores}; resumable
(sources already in --out are skipped). Guardrail and jailbreak data name harmful goals on purpose, so a flag is a
prompt to read the text, not a verdict: see docs/llm_eval_data.md for what was removed and why.
"""
import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "scripts")]
from judge_hardcases import oa  # noqa: E402
from selfjev.data import read_jsonl  # noqa: E402


def text_of(src):
    parts = [src["state"]]
    for q in src["questions"]:
        parts.append(q.get("instruction", ""))
        parts += [str(c.get("description", "")) for c in q.get("candidates") or [] if isinstance(c, dict)]
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raw_dirs", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="omni-moderation-latest")
    a = ap.parse_args()
    out = ROOT / a.out
    done = {r["source_id"] for r in read_jsonl(out)} if out.exists() else set()
    todo = [(f, s) for d in a.raw_dirs for f in sorted((ROOT / d).glob("*.jsonl")) for s in read_jsonl(f) if s["source_id"] not in done]
    print(f"{len(todo)} sources to screen ({len(done)} done)", flush=True)
    with open(out, "a") as fh:
        for k in range(0, len(todo), 16):
            batch = todo[k:k + 16]
            pieces, owner = [], []
            for j, (_, s) in enumerate(batch):
                t = text_of(s)
                for i in range(0, len(t), 8000):
                    pieces.append(t[i:i + 8000])
                    owner.append(j)
            for attempt in range(8):
                try:
                    res = json.loads(oa("POST", "/v1/moderations", {"model": a.model, "input": pieces}))["results"]
                    break
                except RuntimeError as e:  # 429: back off
                    if "429" not in str(e) or attempt == 7:
                        raise
                    time.sleep(10 * 2 ** attempt)
            agg = [{"flagged": False, "scores": {}} for _ in batch]
            for j, r in zip(owner, res):
                agg[j]["flagged"] |= r["flagged"]
                for c, v in r["category_scores"].items():
                    agg[j]["scores"][c] = max(agg[j]["scores"].get(c, 0.0), round(v, 4))
            for (f, s), g in zip(batch, agg):
                fh.write(json.dumps({"source_id": s["source_id"], "file": str(f.relative_to(ROOT)), **g}) + "\n")
            fh.flush()
            if k % 800 == 0:
                print(f"  {k + len(batch)} / {len(todo)}", flush=True)


if __name__ == "__main__":
    main()
