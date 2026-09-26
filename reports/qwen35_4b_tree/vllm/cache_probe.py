"""16-question requests (3 options, option lists) through VllmQwen35Scorer under one vLLM cache setting: model_ms, cache hits."""
import json, random, statistics, sys
sys.path.insert(0, "src"); sys.path.insert(0, "scripts")
from latency_sweep import body
from personal_jev.options import with_options
from personal_jev.schemas import parse_request
from personal_jev.server import compat_to_request
from personal_jev.vllm_qwen35 import VllmQwen35Scorer
if __name__ == "__main__":
    kw = json.loads(sys.argv[1])
    sc = VllmQwen35Scorer("runs/qwen35_4b_tree/merged", max_length=16384, gpu_memory_utilization=0.85, **kw)
    rng = random.Random(0)
    for n, nq in ((256, 16), (1024, 16), (2048, 16), (4096, 16), (1024, 1)):
        rows = []
        for rep in range(4):
            r = compat_to_request(body(sc.tokenizer, n, nq, rng.randrange(10 ** 6)))[0]
            r = r | {"questions": [with_options(q, str(q["id"])) for q in r["questions"]]}
            _, m = sc.score_requests([parse_request(r)])
            rows.append(m) if rep else None  # rep 0 = warm-up
        print(json.dumps({"cfg": kw, "tokens": n, "questions": nq, "model_ms": round(statistics.median(m["model_ms"] for m in rows)),
                          "cached_per_prompt": round(statistics.median(m["cached_tokens"] for m in rows) / rows[0]["pairs"]),
                          "prompt_tokens": round(rows[0]["padded_tokens"] / rows[0]["pairs"])}), flush=True)
