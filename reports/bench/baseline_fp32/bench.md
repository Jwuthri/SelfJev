# Serving benchmark

- Apple M5 Pro / mps / float32; torch 2.14.0, transformers 5.17.0; 2026-09-23T01:11:56-0700
- model `Qwen/Qwen3-Reranker-0.6B` @ `e61197ed45`, adapter `None`, prompt `task-v1`
- batching: max_batch_tokens=16384 (padded), max_batch_size=64; warmup 1; samples per row in the `n` column (up to 20, at least 3, ~60 s budget per row)
- cold start: load 1111 ms + first request (3 pairs) 446 ms
- e2e = parse + tokenize + forward + result assembly; model = forward passes incl. device sync

| state tok | questions | cand | type | pairs | tokens processed | n | e2e p50 ms | e2e p95 ms | model p50 ms | pairs/s | tokens/s | mps_driver_allocated_mb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 512 | 1 | 3 | multiclass | 3 | 1803 | 20 | 351 | 351 | 350 | 8.5 | 5137 | 2697 |
| 512 | 4 | 3 | multiclass | 12 | 7212 | 20 | 1358 | 1360 | 1356 | 8.8 | 5311 | 3721 |
| 512 | 16 | 3 | multiclass | 48 | 28869 | 12 | 5435 | 5442 | 5431 | 8.8 | 5312 | 5777 |
| 2048 | 1 | 3 | multiclass | 3 | 6411 | 20 | 1410 | 1412 | 1408 | 2.1 | 4546 | 3721 |
| 2048 | 4 | 3 | multiclass | 12 | 25644 | 11 | 5612 | 5620 | 5607 | 2.1 | 4570 | 4745 |
| 2048 | 16 | 3 | multiclass | 48 | 102597 | 3 | 23292 | 23294 | 23279 | 2.1 | 4405 | 5769 |
| 8192 | 1 | 3 | multiclass | 3 | 24843 | 7 | 8646 | 8651 | 8636 | 0.3 | 2873 | 3721 |
| 8192 | 4 | 3 | multiclass | 12 | 99372 | 3 | 34533 | 35248 | 34518 | 0.3 | 2878 | 3721 |
| 8192 | 16 | 3 | multiclass | 48 | 397509 | 3 | 149918 | 150158 | 149870 | 0.3 | 2652 | 3721 |
| 2048 | 4 | 2 | multiclass | 8 | 17096 | 16 | 3907 | 3939 | 3903 | 2.0 | 4376 | 4745 |
| 2048 | 4 | 8 | multiclass | 32 | 68384 | 4 | 15518 | 15576 | 15509 | 2.1 | 4407 | 4745 |
| 2048 | 16 | 1 | binary | 16 | 34055 | 7 | 8595 | 8602 | 8590 | 1.9 | 3962 | 4745 |
