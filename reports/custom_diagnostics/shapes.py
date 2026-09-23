"""Heap growth vs batch shapes: 160 Stage-A-style training steps (frozen backbone, backward through new modules).
usage: python shapes.py <bucket 0|1>"""
import os, random, subprocess, sys, torch
from personal_jev import custom
from personal_jev.data import load
from personal_jev.train_custom import DEFAULTS, build, encode_items, forward_items, micro_batches
if hasattr(custom, "SHAPE_BUCKETS"):
    custom.SHAPE_BUCKETS = sys.argv[1] == "1"
def heap_mb():
    out = subprocess.run(["footprint", "-p", str(os.getpid())], capture_output=True, text=True).stdout
    v, unit = next(l.split()[:2] for l in out.splitlines() if "MALLOC_SMALL" in l)
    return float(v) * {"KB": 1 / 1024, "MB": 1, "GB": 1024}[unit]
tok, model, _ = build(DEFAULTS | {"backbone": "frozen", "dtype": "bfloat16"})
model.to("mps").train()
ex = load(["data/hf.jsonl", "data/synthetic.jsonl"], {"train"})
random.Random(0).shuffle(ex)
items, states, _ = encode_items(tok, ex[:6000], 2048, 256)
batches = micro_batches(items, states, 8192, random.Random(0))
print(f"bucketing={getattr(custom, 'SHAPE_BUCKETS', 'n/a')} start heap {heap_mb():.0f} MB", flush=True)
import time; t0 = time.perf_counter()
for i, b in enumerate(batches[:160], 1):
    forward_items(model, [items[j] for j in b], states, 8192).sum().backward()
    if i % 40 == 0:
        torch.mps.synchronize()
        print(f"after {i} steps heap {heap_mb():.0f} MB, {time.perf_counter() - t0:.1f} s", flush=True)
