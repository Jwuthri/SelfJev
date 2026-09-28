**Use an NVIDIA GPU for the supported server.** `selfjev serve` selects CUDA by default and does not offer a CPU or MPS device flag. A full-model Apple Silicon experiment is measured below through the lower-level tree engine; it is not a validated Mac serving setup.

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

The [interactive hardware comparison](/#hardware) shows server-side median request times on A10G, L40S, and H100 for short through long inputs and either 1 or 16 questions about the same text. Each result is the median of 10 warmed requests, with three answer options per question and network time excluded. The GPU runs use vLLM; the Mac run uses the native tree engine on MPS. These are measured configurations, not a hardware-only comparison. The chart links each GPU to its raw request log; full model and runtime configurations are recorded in the [benchmark methodology](https://jwuthri.github.io/SelfJev/speed/).

## Apple Silicon experiment

We also ran the **current SelfJev-4B** on a local **M5 Pro with a 20-core GPU and 48 GB of unified memory**. The adapter was merged into Qwen3.5-4B in bf16 and scored through `TreeServer` on PyTorch MPS. The test used synthetic repeated text and three answer options per question. These are local call times, including tokenization but excluding HTTP and network time; each cell is the median of 10 calls after two warm-ups.

| Text length | 1 question | 16 questions |
|---|---:|---:|
| 8 tokens | 688 ms | 6,786 ms |
| 512 tokens | 2,018 ms | 8,599 ms |

The MPS path uses PyTorch's slower reference implementation for the model's gated recurrent operation. The [raw samples](https://github.com/Jwuthri/SelfJev/blob/master/reports/latency/mac_m5_pro_selfjev4b.json) and [benchmark script](https://github.com/Jwuthri/SelfJev/blob/master/scripts/bench_local_mps.py) make this small experiment reproducible. The supported CLI still requires CUDA.

## Why not an 8 GB machine?

A nominal 4-billion-parameter model needs approximately **8 GB for bf16 weights alone**, or **16 GB for float32**. That excludes the adapter, temporary loading copies, activations, attention masks, recurrent state, and the Python runtime. The downloaded base checkpoint is about 9 GB.

A **16 GB RAM CPU machine is not a supported minimum**. A 32 GB budget gives more room for experimentation, but long inputs can still exceed it and the CPU speed is unknown. No quantized CPU artifact or llama.cpp/GGUF serving path is provided. Supporting one is engineering work, not a configuration switch.

## Context length and concurrency matter

SelfJev's context limit is configurable with `--max-length`; the default is **32,768 tokens** for the formatted document plus the longest question/candidate path. Prompt formatting and options also consume this budget.

The underlying [Qwen3.5-4B configuration](https://huggingface.co/Qwen/Qwen3.5-4B/blob/main/config.json) has a native **262,144-token** context window. That is base-model capacity, not a validated SelfJev serving limit: training used texts up to 16K, and we have not validated full-window inference or accuracy in this engine. Raising the flag alone does not establish usable capacity.

For comparison, [Jev's published limits](https://docs.typesafe.ai/models) are **32K tokens for state plus the longest question**, and **64K tokens for state plus all questions combined** (checked September 28, 2026). Self-hosting lets you experiment with a larger budget, subject to memory and validation on your documents.

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

The hardware explorer includes latency runs on A10G, L40S, H100, and M5 Pro. The native tree engine also has an A10G correctness check, and the training recipe ran on an L40S. Mac serving and full-model CPU inference remain unvalidated. See the linked reports for the configuration and scope of each measurement.

Sources: [deployment notes](https://github.com/Jwuthri/SelfJev/blob/master/docs/deploy.md), [engine loader](https://github.com/Jwuthri/SelfJev/blob/master/src/selfjev/engine/qwen35.py), [tree packing](https://github.com/Jwuthri/SelfJev/blob/master/src/selfjev/engine/tree.py), [GPU engine check](https://github.com/Jwuthri/SelfJev/tree/master/reports/selfjev_4b_treeserver), and [latency methodology](https://jwuthri.github.io/SelfJev/speed/).
