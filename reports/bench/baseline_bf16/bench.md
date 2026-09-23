# Serving benchmark

- Apple M5 Pro / mps / bfloat16; torch 2.14.0, transformers 5.17.0; 2026-09-23T01:23:34-0700
- model `Qwen/Qwen3-Reranker-0.6B` @ `e61197ed45`, adapter `None`, prompt `task-v1`
- batching: max_batch_tokens=16384 (padded), max_batch_size=64; warmup 1; samples per row in the `n` column (up to 20, at least 3, ~60 s budget per row)
- cold start: load 1201 ms + first request (3 pairs) 273 ms
- e2e = parse + tokenize + forward + result assembly; model = forward passes incl. device sync

| state tok | questions | cand | type | pairs | tokens processed | n | e2e p50 ms | e2e p95 ms | model p50 ms | pairs/s | tokens/s | mps_driver_allocated_mb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 512 | 1 | 3 | multiclass | 3 | 1803 | 20 | 150 | 151 | 149 | 20.0 | 12012 | 2219 |
| 512 | 4 | 3 | multiclass | 12 | 7212 | 20 | 608 | 618 | 606 | 19.7 | 11869 | 2189 |
| 512 | 16 | 3 | multiclass | 48 | 28869 | 20 | 2452 | 2507 | 2447 | 19.6 | 11774 | 3225 |
| 2048 | 1 | 3 | multiclass | 3 | 6411 | 20 | 568 | 592 | 565 | 5.3 | 11290 | 2195 |
| 2048 | 4 | 3 | multiclass | 12 | 25644 | 20 | 2282 | 2393 | 2277 | 5.3 | 11238 | 3215 |
| 2048 | 16 | 3 | multiclass | 48 | 102597 | 7 | 9598 | 9959 | 9584 | 5.0 | 10690 | 3221 |
| 8192 | 1 | 3 | multiclass | 3 | 24843 | 20 | 2873 | 2984 | 2863 | 1.0 | 8647 | 2185 |
| 8192 | 4 | 3 | multiclass | 12 | 99372 | 6 | 11343 | 11475 | 11326 | 1.1 | 8761 | 2185 |
| 8192 | 16 | 3 | multiclass | 48 | 397509 | 3 | 46664 | 46785 | 46616 | 1.0 | 8519 | 2185 |
| 2048 | 4 | 2 | multiclass | 8 | 17096 | 20 | 1507 | 1528 | 1503 | 5.3 | 11347 | 3221 |
| 2048 | 4 | 8 | multiclass | 32 | 68384 | 10 | 6068 | 6224 | 6059 | 5.3 | 11270 | 3213 |
| 2048 | 16 | 1 | binary | 16 | 34055 | 18 | 3343 | 3428 | 3338 | 4.8 | 10187 | 3221 |
