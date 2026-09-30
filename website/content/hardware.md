**Use an NVIDIA GPU for the supported server.** `selfjev serve` selects CUDA by default and does not offer a CPU or MPS device flag. A full-model Apple Silicon experiment is measured below through the lower-level tree engine; it is not a validated Mac serving setup.

## A practical starting point

| Workload | GPU / VRAM | System RAM | CPU | Status |
|---|---|---|---|---|
| Light inference | NVIDIA, 24 GB | 16–32 GB | 4 vCPUs | Measured on an A10G: texts up to 32K tokens with 50 questions fit (21.1 GB peak) |
| Smaller-memory experiment | NVIDIA, 16 GB | 16–32 GB | 4+ vCPUs | Documented floor; workload-dependent, not a measured minimum |
| Long inputs or more concurrency | NVIDIA, 48 GB | 32 GB+ | 8 vCPUs | Conservative starting point; measure your workload |
| Fine-tuning | L40S, 48 GB | 64 GB used on g6e.2xlarge | 8 vCPUs | Training recipe run on this class of machine |
| CPU-only | None | 32 GB budget for an experiment | Modern multicore CPU | Unsupported CLI path; no measured latency or minimum |
| Marketing and docs site | None | No dedicated runtime required | None at runtime | Static Next.js export |

System RAM and GPU VRAM are separate resources. Extra system RAM does not automatically compensate for too little VRAM in this engine.

## Compare measured GPU response times

The [interactive hardware comparison](/#hardware) shows how long one request takes with the current **SelfJev-4B** on A10G, L40S, and H100: texts from 512 to 32,000 tokens, with 1 to 50 questions about the same text. It runs the native tree engine that `selfjev serve` uses, measured on September 30, 2026. Each value is the median of up to 20 warmed requests (at least 3), with three answer options per question. The times are measured inside the process, without HTTP or network time. The chart links each GPU to its raw benchmark; the [full tables](https://github.com/Jwuthri/SelfJev/blob/master/reports/bench/selfjev4b_qsweep_summary.md) add decisions per second and the cost of each extra question.

## Many questions about one text

The shared-prefix tree reads the text once. Each question then adds only its own short branch. On a **24 GB A10G**:

| Text tokens | 1 question | 5 | 10 | 25 | 50 | Peak GPU memory, 1 → 50 questions |
|---|---:|---:|---:|---:|---:|---|
| 512 | 241 ms | 319 | 401 | 735 | 1,470 | 8.1 → 9.6 GB |
| 2,048 | 584 ms | 653 | 741 | 1,165 | 1,945 | 8.5 → 9.6 GB |
| 8,192 | 2,558 ms | 2,678 | 2,825 | 3,436 | 4,576 | 9.7 → 11.3 GB |
| 16,384 | 7,157 ms | 6,991 | 7,404 | 7,545 | 9,607 | 13.2 → 13.9 GB |
| 32,000 | 22,019 ms | 22,434 | 22,978 | 24,643 | 27,760 | 18.5–21.1 GB |

- **Memory follows the text, not the questions.** The weights take about 8 GB, and 50 questions add at most 1.4 GB. Every workload above fits on the 24 GB card.
- **Latency grows far more slowly than the number of questions.** Fifty questions take 1.3–6.1× as long as one. One request with 50 questions is 8–40× faster than 50 requests with one question each.
- **Faster GPUs cut the time, not the memory.** Fifty questions about a 2,048-token text take 1,945 ms on the A10G, 894 ms on an L40S and 404 ms on an H100. Memory use is the same on all three.

These requests use synthetic text and are sent one at a time; concurrent requests batched together are not measured. The 32K rows measure time and memory only: the model was trained on texts up to 16K tokens.

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

Memory use grows mainly with document length, [as measured above](#many-questions-about-one-text); question and candidate branches add little, and batching adds more. The current tree builds a dense attention mask, so long packed sequences can be expensive even when the weights fit.

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

The current model's latency and memory are measured on A10G, L40S and H100, and a smaller experiment ran on an M5 Pro. The native tree engine also has an A10G correctness check, and the training recipe ran on an L40S. L4 latency, Mac serving and full-model CPU inference remain unvalidated. See the linked reports for the configuration and scope of each measurement.

Sources: [question sweep](https://github.com/Jwuthri/SelfJev/blob/master/reports/bench/selfjev4b_qsweep_summary.md), [deployment notes](https://github.com/Jwuthri/SelfJev/blob/master/docs/deploy.md), [engine loader](https://github.com/Jwuthri/SelfJev/blob/master/src/selfjev/engine/qwen35.py), [tree packing](https://github.com/Jwuthri/SelfJev/blob/master/src/selfjev/engine/tree.py), [GPU engine check](https://github.com/Jwuthri/SelfJev/tree/master/reports/selfjev_4b_treeserver), and [latency methodology](https://jwuthri.github.io/SelfJev/speed/).
