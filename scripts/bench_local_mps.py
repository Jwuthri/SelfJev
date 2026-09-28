"""Measure the current TreeServer on Apple Silicon, without network or HTTP overhead.

Run only when local model work is authorized. The base checkpoint must be downloaded once.
Example: uv run python scripts/bench_local_mps.py --lengths 8 512
"""

import argparse
import json
import platform
import statistics
import subprocess
import time
from pathlib import Path

import torch

from selfjev.core.schemas import Candidate, Question, Request
from selfjev.engine.tree import TreeServer


def _sysctl(name):
    return subprocess.check_output(["sysctl", "-n", name], text=True).strip()


def _save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(data, indent=2) + "\n")
    temp.replace(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lengths", nargs="+", type=int, default=[8, 512, 2048, 4096])
    parser.add_argument("--reps", type=int, default=10)
    parser.add_argument("--warmup", type=int, default=2)
    parser.add_argument("--output", type=Path, default=Path("reports/latency/mac_m5_pro_selfjev4b.json"))
    args = parser.parse_args()
    if not torch.backends.mps.is_available():
        raise RuntimeError("MPS is unavailable")
    if args.reps < 1 or args.warmup < 1 or any(n < 1 for n in args.lengths):
        raise ValueError("reps, warmup, and lengths must be positive")

    engine = TreeServer("weights/selfjev_4b", device="mps", dtype="bfloat16", max_length=8192)
    report = {
        "meta": {
            "date": time.strftime("%Y-%m-%d"),
            "chip": _sysctl("machdep.cpu.brand_string"),
            "gpu_cores": 20,
            "unified_memory_gb": round(int(_sysctl("hw.memsize")) / 1024**3),
            "platform": platform.platform(),
            "torch": torch.__version__,
            "model": engine.meta,
            "input_text": "synthetic `blue ` repeated to exactly the stated tokenizer-token length",
            "method": (
                "TreeServer.score_requests, one request at a time; MPS synchronized before and after each call; "
                "wall time includes tokenization and model work, excludes HTTP/network; 3-option multiclass questions"
            ),
            "warmup": args.warmup,
            "reps": args.reps,
            "local_cost_usd": 0,
        },
        "cells": [],
    }
    for tokens in args.lengths:
        state = "blue " * (tokens - 1)
        actual = len(engine.sc.tokens(state))
        if actual != tokens:
            raise RuntimeError(f"Expected {tokens} text tokens, got {actual}")
        for count in (1, 16):
            qs = tuple(
                Question(
                    str(i),
                    "multiclass",
                    f"What color is object number {i}?",
                    (Candidate("red", "red"), Candidate("blue", "blue"), Candidate("green", "green")),
                )
                for i in range(1, count + 1)
            )
            req = Request(state, qs)
            samples = []
            packed_tokens = None
            for rep in range(args.warmup + args.reps):
                torch.mps.synchronize()
                start = time.perf_counter()
                values, stats = engine.score_requests([req])
                torch.mps.synchronize()
                ms = (time.perf_counter() - start) * 1000
                if len(values[0]) != count or any(len(v) != 3 for v in values[0]):
                    raise RuntimeError("Unexpected score shape")
                packed_tokens = stats["input_tokens"]
                if rep >= args.warmup:
                    samples.append(round(ms, 3))
            cell = {
                "text_tokens": tokens,
                "questions": count,
                "candidates_per_question": 3,
                "packed_tokens": packed_tokens,
                "samples_ms": samples,
                "median_ms": round(statistics.median(samples), 3),
            }
            report["cells"].append(cell)
            _save(args.output, report)
            print(json.dumps(cell), flush=True)


if __name__ == "__main__":
    main()
