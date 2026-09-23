# Serving benchmark

- x86_64 / cuda / bfloat16; torch 2.14.0+cu130, transformers 5.17.0; 2026-09-23T22:30:09+0000
- model `Qwen/Qwen3-Reranker-0.6B` @ `e61197ed45` (stock reranker pairs), adapter/checkpoint `None`, prompt `task-v1`
- batching: max_batch_tokens=16384 (padded), max_batch_size=64; warmup 1; samples per row in the `n` column (up to 20, at least 3, ~60 s budget per row)
- cold start: load 1071 ms + first request (3 pairs) 731 ms
- e2e = parse + tokenize + forward + result assembly; model = forward passes incl. device sync

| state tok | questions | cand | type | pairs | state encodes | tokens processed | n | e2e p50 ms | e2e p95 ms | model p50 ms | pairs/s | tokens/s | cuda_peak_allocated_mb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 512 | 1 | 3 | multiclass | 3 | 3 | 1803 | 10 | 28 | 28 | 26 | 107.7 | 64731 | 1191 |
| 512 | 4 | 3 | multiclass | 12 | 12 | 7212 | 10 | 85 | 85 | 80 | 141.4 | 84961 | 1329 |
| 512 | 16 | 3 | multiclass | 48 | 48 | 28869 | 10 | 421 | 421 | 405 | 114.1 | 68610 | 1561 |
| 2048 | 1 | 3 | multiclass | 3 | 3 | 6411 | 10 | 79 | 79 | 74 | 38.0 | 81127 | 1311 |
| 2048 | 4 | 3 | multiclass | 12 | 12 | 25644 | 10 | 386 | 387 | 371 | 31.1 | 66407 | 1529 |
| 2048 | 16 | 3 | multiclass | 48 | 48 | 102597 | 10 | 1682 | 1683 | 1622 | 28.5 | 61006 | 1622 |
| 8192 | 1 | 3 | multiclass | 3 | 3 | 24843 | 10 | 409 | 409 | 389 | 7.3 | 60797 | 1360 |
| 8192 | 4 | 3 | multiclass | 12 | 12 | 99372 | 10 | 1620 | 1625 | 1560 | 7.4 | 61323 | 1360 |
| 8192 | 16 | 3 | multiclass | 48 | 48 | 397509 | 10 | 6579 | 6632 | 6326 | 7.3 | 60417 | 1360 |
| 2048 | 4 | 2 | multiclass | 8 | 8 | 17096 | 10 | 263 | 264 | 253 | 30.4 | 64881 | 1529 |
| 2048 | 4 | 8 | multiclass | 32 | 32 | 68384 | 10 | 1051 | 1052 | 1012 | 30.4 | 65053 | 1529 |
| 2048 | 16 | 1 | binary | 16 | 16 | 34055 | 10 | 596 | 597 | 576 | 26.8 | 57104 | 1620 |
