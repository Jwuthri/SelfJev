**Use a GPU for the current server.** `selfjev serve` selects CUDA by default and does not offer a CPU device flag. The engine has a lower-level CPU path for tiny tests, but full-model CPU serving has not been validated or benchmarked.

## A practical starting point

| Workload | GPU / VRAM | System RAM | CPU | Status |
|---|---|---|---|---|
| Light inference | NVIDIA, 24 GB | 16–32 GB | 4 vCPUs | Planning recommendation; A10G engine correctness checked |
| Smaller-memory experiment | NVIDIA, 16 GB | 16–32 GB | 4+ vCPUs | Documented floor; workload-dependent, not a measured minimum |
| Long inputs or more concurrency | NVIDIA, 48 GB | 32 GB+ | 8 vCPUs | Conservative starting point; measure your workload |
| Fine-tuning | L40S, 48 GB | 64 GB used on g6e.2xlarge | 8 vCPUs | Training recipe run on this class of machine |
| CPU-only | None | 32 GB budget for an experiment | Modern multicore CPU | Unsupported CLI path; no measured latency or minimum |
| Marketing and docs site | None | No dedicated runtime required | None at runtime | Static Next.js export |

System RAM and GPU VRAM are separate resources. Extra system RAM does not automatically compensate for too little VRAM in this engine.

## Compare measured GPU response times

The [interactive hardware comparison](/#hardware) shows server-side median request times on A10G, L40S, and H100 for short through long inputs and either 1 or 16 questions about the same text. It helps show how much GPU choice can change latency. These runs used the earlier Qwen3-4B tree model on vLLM, **not** the current SelfJev-4B / TreeServer. Treat them as historical measurements, not a performance promise for the current model. The chart links each GPU to its raw request log.

## Why not an 8 GB machine?

A nominal 4-billion-parameter model needs approximately **8 GB for bf16 weights alone**, or **16 GB for float32**. That excludes the adapter, temporary loading copies, activations, attention masks, recurrent state, and the Python runtime. The downloaded base checkpoint is about 9 GB.

A **16 GB RAM CPU machine is not a supported minimum**. A 32 GB budget gives more room for experimentation, but long inputs can still exceed it and the CPU speed is unknown. No quantized CPU artifact or llama.cpp/GGUF serving path is provided. Supporting one is engineering work, not a configuration switch.

## Context length and concurrency matter

Memory use grows with document length, the number of question/candidate branches, and batching. The current tree builds a dense attention mask; long packed sequences can be expensive even when the weights fit.

Start with short inputs and conservative batching. The controls are:

```bash
uv run --no-sync selfjev serve \
  --max-length 4096 \
  --max-batch-tokens 4096
```

`--max-length` limits the state plus the longest question/candidate path. `--max-batch-tokens` controls packing; it is not a hard memory cap for a single large request tree. Reduce question and candidate counts as well if you run out of memory. Longer-than-allowed input is rejected, not silently truncated.

## Disk and first startup

Budget **50 GB of free disk** for the checkout, Python/CUDA dependencies, adapter, model cache, and temporary files. This is a planning allowance, not a measured minimum. Building a Docker image with baked-in weights may require additional space.

## What has actually been measured?

The current engine was checked on an A10G and the training recipe ran on an L40S. Current TreeServer accuracy is verified, but there is **no controlled GPU latency benchmark for current SelfJev-4B**, and no full-model CPU benchmark. Historic H100 and A10G speed figures belong to archived Qwen3 models.

Sources: [deployment notes](https://github.com/Jwuthri/SelfJev/blob/master/docs/deploy.md), [engine loader](https://github.com/Jwuthri/SelfJev/blob/master/src/selfjev/engine/qwen35.py), [tree packing](https://github.com/Jwuthri/SelfJev/blob/master/src/selfjev/engine/tree.py), [GPU engine check](https://github.com/Jwuthri/SelfJev/tree/master/reports/selfjev_4b_treeserver), and [latency methodology](https://jwuthri.github.io/SelfJev/speed/).
