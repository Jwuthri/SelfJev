# Serving benchmark

- Apple M5 Pro / mps / float32; torch 2.14.0, transformers 5.17.0; 2026-09-23T01:46:34-0700
- model `Qwen/Qwen3-Reranker-0.6B` @ `e61197ed45`, adapter `runs/lora_pilot/adapter`, prompt `task-v1`
- batching: max_batch_tokens=16384 (padded), max_batch_size=64; warmup 1; samples per row in the `n` column (up to 20, at least 3, ~60 s budget per row)
- cold start: load 1726 ms + first request (3 pairs) 463 ms
- e2e = parse + tokenize + forward + result assembly; model = forward passes incl. device sync

| state tok | questions | cand | type | pairs | tokens processed | n | e2e p50 ms | e2e p95 ms | model p50 ms | pairs/s | tokens/s | mps_driver_allocated_mb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 512 | 1 | 3 | multiclass | 3 | 1803 | 20 | 383 | 415 | 382 | 7.8 | 4706 | 2713 |
| 512 | 4 | 3 | multiclass | 12 | 7212 | 20 | 1492 | 1545 | 1491 | 8.0 | 4833 | 3737 |
| 512 | 16 | 3 | multiclass | 48 | 28869 | 10 | 6008 | 6480 | 6004 | 8.0 | 4805 | 4769 |
| 2048 | 1 | 3 | multiclass | 3 | 6411 | 20 | 1529 | 1583 | 1527 | 2.0 | 4192 | 3737 |
| 2048 | 4 | 3 | multiclass | 12 | 25644 | 10 | 6066 | 6072 | 6061 | 2.0 | 4228 | 4769 |
| 2048 | 16 | 3 | multiclass | 48 | 102597 | 3 | 26642 | 26772 | 26628 | 1.8 | 3851 | 5793 |
| 8192 | 1 | 3 | multiclass | 3 | 24843 | 7 | 9375 | 9914 | 9365 | 0.3 | 2650 | 3737 |
| 8192 | 4 | 3 | multiclass | 12 | 99372 | 3 | 38266 | 38895 | 38250 | 0.3 | 2597 | 3737 |
| 8192 | 16 | 3 | multiclass | 48 | 397509 | 3 | 149794 | 161857 | 149738 | 0.3 | 2654 | 3737 |
| 2048 | 4 | 2 | multiclass | 8 | 17096 | 15 | 4133 | 4151 | 4129 | 1.9 | 4137 | 4769 |
| 2048 | 4 | 8 | multiclass | 32 | 68384 | 4 | 16159 | 16470 | 16150 | 2.0 | 4232 | 4769 |
| 2048 | 16 | 1 | binary | 16 | 34055 | 7 | 9115 | 9279 | 9110 | 1.8 | 3736 | 4769 |
