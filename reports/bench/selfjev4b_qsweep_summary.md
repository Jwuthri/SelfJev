# Many questions on one document: latency, memory and throughput of `selfjev-4b` on A10G, L40S and H100

2026-09-30, `selfjev bench` (the default `TreeServer` engine, `weights/selfjev_4b_vision` merged into Qwen3.5-4B, bf16).
One document, 1 / 5 / 10 / 25 / 50 questions with 3 options each, documents of 512 to 32,000 tokens. One request at a time,
in process (parse + tokenize + forward + result assembly; no HTTP or network), p50 over up to 20 warm calls
(at least 3, ~60 s per cell). Raw data: `selfjev4b_qsweep_{a10g,l40s,h100}/bench.json` (+ `bench.md`, `nvidia-smi.txt`). JOURNAL 2026-09-30 10:45.

| box | GPU | usable VRAM | $/h | wall time | cost |
|---|---|---|---|---|---|
| g5.xlarge, us-east-1 | A10G 24 GB | 22.5 GiB | 1.006 | ≈ 32 min | ≈ $0.54 |
| g6e.xlarge, us-east-2 | L40S 48 GB | 45.0 GiB | 1.861 | ≈ 23 min | ≈ $0.71 |
| p5.4xlarge spot, us-east-2 | H100 80 GB | 79.6 GiB | 2.457 | ≈ 22 min (2 launches) | ≈ $0.90 |

## What it shows

- **Memory barely moves with the number of questions.** The weights take 8 GiB. For a fixed document, going from 1 to 50
  questions adds at most 1.4 GiB allocated (512 tokens: 8.0 → 9.4). Memory follows document length instead: from
  8.0 GiB at 512 tokens to 14.2 GiB allocated (20.2 reserved by PyTorch) at 32K. **Every cell fits on the 24 GB A10G.**
  The largest, a 32K document with 25 questions, reserved 21.1 of 22.5 GiB. No run went out of memory.
- **Latency grows far slower than the number of questions.** 50 questions cost 1.3–6.1× one question, and the
  longer the document, the smaller the factor: the text is read once, and each question only adds its own short branch.
  Each extra question costs 3–24 ms on the H100, 10–49 ms on the L40S and 25–117 ms on the A10G, growing with document
  length because every branch attends to the whole text.
- **Throughput rises with questions.** On a 2K document, one request answers 1.7 → 25.7 decisions/s on the A10G,
  4.1 → 55.9 on the L40S and 6.0 → 124 on the H100 as it goes from 1 to 50 questions.
- **Against 50 separate requests** of one question each (same engine, same GPU): 8–40× faster, the gain growing with
  document length (40× at 32K on every GPU).
- **GPU class:** the H100 is 1.7× (512 tokens, 1 question) to 5.3× (32K, 50 questions) faster than the A10G; memory use
  is the same on all three (±0.03 GiB).

### Latency, p50 ms (one request, one document, 3 options per question)

| GPU | doc tokens | 1 q | 5 q | 10 q | 25 q | 50 q | 50 q ÷ 1 q |
|---|---|---|---|---|---|---|---|
| A10G 24 GB | 512 | 241 | 319 | 401 | 735 | 1,470 | 6.1× |
| A10G 24 GB | 2,048 | 584 | 653 | 741 | 1,165 | 1,945 | 3.3× |
| A10G 24 GB | 8,192 | 2,558 | 2,678 | 2,825 | 3,436 | 4,576 | 1.8× |
| A10G 24 GB | 16,384 | 7,157 | 6,991 | 7,404 | 7,545 | 9,607 | 1.3× |
| A10G 24 GB | 32,000 | 22,019 | 22,434 | 22,978 | 24,643 | 27,760 | 1.3× |
| L40S 48 GB | 512 | 145 | 156 | 179 | 311 | 644 | 4.4× |
| L40S 48 GB | 2,048 | 243 | 269 | 300 | 484 | 894 | 3.7× |
| L40S 48 GB | 8,192 | 1,173 | 1,235 | 1,328 | 1,616 | 2,220 | 1.9× |
| L40S 48 GB | 16,384 | 3,129 | 3,236 | 3,340 | 3,815 | 4,626 | 1.5× |
| L40S 48 GB | 32,000 | 9,146 | 9,335 | 9,478 | 10,337 | 11,544 | 1.3× |
| H100 80 GB | 512 | 146 | 148 | 154 | 187 | 309 | 2.1× |
| H100 80 GB | 2,048 | 166 | 176 | 189 | 252 | 404 | 2.4× |
| H100 80 GB | 8,192 | 506 | 532 | 560 | 672 | 907 | 1.8× |
| H100 80 GB | 16,384 | 1,290 | 1,340 | 1,385 | 1,580 | 1,941 | 1.5× |
| H100 80 GB | 32,000 | 4,033 | 4,122 | 4,200 | 4,574 | 5,206 | 1.3× |

### Decisions per second inside one request (questions ÷ latency)

| GPU | doc tokens | 1 q | 5 q | 10 q | 25 q | 50 q |
|---|---|---|---|---|---|---|
| A10G 24 GB | 512 | 4.1 | 15.7 | 24.9 | 34.0 | 34.0 |
| A10G 24 GB | 2,048 | 1.7 | 7.7 | 13.5 | 21.5 | 25.7 |
| A10G 24 GB | 8,192 | 0.39 | 1.9 | 3.5 | 7.3 | 10.9 |
| A10G 24 GB | 16,384 | 0.14 | 0.72 | 1.4 | 3.3 | 5.2 |
| A10G 24 GB | 32,000 | 0.05 | 0.22 | 0.44 | 1.0 | 1.8 |
| L40S 48 GB | 512 | 6.9 | 32.1 | 55.8 | 80.3 | 77.6 |
| L40S 48 GB | 2,048 | 4.1 | 18.6 | 33.4 | 51.7 | 55.9 |
| L40S 48 GB | 8,192 | 0.85 | 4.0 | 7.5 | 15.5 | 22.5 |
| L40S 48 GB | 16,384 | 0.32 | 1.5 | 3.0 | 6.6 | 10.8 |
| L40S 48 GB | 32,000 | 0.11 | 0.54 | 1.1 | 2.4 | 4.3 |
| H100 80 GB | 512 | 6.8 | 33.7 | 65.1 | 133.9 | 161.8 |
| H100 80 GB | 2,048 | 6.0 | 28.4 | 52.9 | 99.4 | 123.8 |
| H100 80 GB | 8,192 | 2.0 | 9.4 | 17.9 | 37.2 | 55.1 |
| H100 80 GB | 16,384 | 0.78 | 3.7 | 7.2 | 15.8 | 25.8 |
| H100 80 GB | 32,000 | 0.25 | 1.2 | 2.4 | 5.5 | 9.6 |

### Peak GPU memory, GiB: allocated by tensors / reserved by PyTorch (identical on the three GPUs to ±0.03 GiB; A10G shown)

| doc tokens | 1 q | 5 q | 10 q | 25 q | 50 q |
|---|---|---|---|---|---|
| 512 | 8.0 / 8.1 | 8.3 / 8.6 | 8.4 / 8.6 | 8.7 / 8.8 | 9.4 / 9.6 |
| 2,048 | 8.3 / 8.5 | 8.3 / 8.5 | 8.3 / 8.5 | 8.7 / 9.0 | 9.5 / 9.6 |
| 8,192 | 9.3 / 9.7 | 9.3 / 10.0 | 9.4 / 10.0 | 9.4 / 10.9 | 9.7 / 11.3 |
| 16,384 | 10.8 / 13.2 | 10.9 / 13.1 | 10.9 / 12.7 | 11.0 / 13.6 | 11.1 / 13.9 |
| 32,000 | 14.2 / 20.2 | 14.3 / 20.3 | 14.1 / 18.5 | 15.0 / 21.1 | 14.4 / 19.5 |

### Extra time per added question, ms ((50 q − 1 q) ÷ 49)

| doc tokens | A10G 24 GB | L40S 48 GB | H100 80 GB |
|---|---|---|---|
| 512 | 25.1 | 10.2 | 3.3 |
| 2,048 | 27.8 | 13.3 | 4.9 |
| 8,192 | 41.2 | 21.4 | 8.2 |
| 16,384 | 50.0 | 30.6 | 13.3 |
| 32,000 | 117.2 | 48.9 | 23.9 |

### 50 questions: one request vs 50 separate one-question requests (same engine, same GPU)

| doc tokens | A10G 24 GB | L40S 48 GB | H100 80 GB |
|---|---|---|---|
| 512 | 1,470 vs 12,050 ms (8×) | 644 vs 7,272 ms (11×) | 309 vs 7,310 ms (24×) |
| 2,048 | 1,945 vs 29,220 ms (15×) | 894 vs 12,133 ms (14×) | 404 vs 8,302 ms (21×) |
| 8,192 | 4,576 vs 127,908 ms (28×) | 2,220 vs 58,626 ms (26×) | 907 vs 25,276 ms (28×) |
| 16,384 | 9,607 vs 357,854 ms (37×) | 4,626 vs 156,459 ms (34×) | 1,941 vs 64,514 ms (33×) |
| 32,000 | 27,760 vs 1,100,942 ms (40×) | 11,544 vs 457,310 ms (40×) | 5,206 vs 201,663 ms (39×) |

The three extra rows of the default grid (2K document: 4 questions × 2 or 8 options, 16 binary questions) are in each
`bench.md`: e.g. 16 binary questions take 627 / 270 / 174 ms on A10G / L40S / H100.

## Limits

- Synthetic document (a repeated support-ticket paragraph) and synthetic questions; 3 options per question. Latency
  depends on token counts, not wording, but real prompts differ in length.
- One request at a time. Throughput here is within one request; concurrent requests batched together are not measured.
- Memory: "allocated" is `torch.cuda.max_memory_allocated`, "reserved" what PyTorch's caching allocator held (the part
  that must fit on the card; it varies by ±1.5 GiB between neighbouring cells, e.g. 32K: 20.2 / 20.3 / 18.5 / 21.1 / 19.5).
  The CUDA context (≈ 0.5 GiB) comes on top of both.
- Few samples at the longest texts on the slowest GPU (A10G: 3 per 32K cell, 7–9 per 16K cell); at 16K the 5-question
  cell is 2% faster than the 1-question one, which is noise.
- Training texts went up to 16K tokens, so 32K is timed here but its accuracy is not validated.
- Cold start, not in the tables: loading 17 s (L40S, H100) to 52 s (A10G, first read of a fresh disk), then the first
  request 39–75 s (kernel compilation). `selfjev serve` sends a warm-up request before it answers `/health`.
- The H100 ran with cuDNN attention switched off: PyTorch picks it on H100 and it failed to load there
  (`CUDNN_STATUS_SUBLIBRARY_LOADING_FAILED` on the first launch, whose log is not kept). `TreeServer` now disables
  it everywhere; A10G and L40S never pick it, so all three use the same attention kernel.

## Reproduce

```bash
uv sync --extra serve --extra gpu
uv run selfjev bench --lengths 512,2048,8192,16384,32000 --questions 1,5,10,25,50 --out reports/bench/<name>
```
