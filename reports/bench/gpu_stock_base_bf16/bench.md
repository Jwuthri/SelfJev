# Serving benchmark

- x86_64 / cuda / bfloat16; torch 2.14.0+cu130, transformers 5.17.0; 2026-09-23T21:40:45+0000
- model `Qwen/Qwen3-Reranker-0.6B` @ `e61197ed45` (stock reranker pairs), adapter/checkpoint `None`, prompt `task-v1`
- batching: max_batch_tokens=16384 (padded), max_batch_size=64; warmup 1; samples per row in the `n` column (up to 20, at least 3, ~60 s budget per row)
- cold start: load 1337 ms + first request (3 pairs) 853 ms
- e2e = parse + tokenize + forward + result assembly; model = forward passes incl. device sync

| state tok | questions | cand | type | pairs | state encodes | tokens processed | n | e2e p50 ms | e2e p95 ms | model p50 ms | pairs/s | tokens/s | cuda_peak_allocated_mb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 512 | 1 | 3 | multiclass | 3 | 3 | 1803 | 10 | 74 | 74 | 72 | 40.8 | 24493 | 1191 |
| 512 | 4 | 3 | multiclass | 12 | 12 | 7212 | 10 | 249 | 249 | 244 | 48.1 | 28928 | 1329 |
| 512 | 16 | 3 | multiclass | 48 | 48 | 28869 | 10 | 976 | 977 | 956 | 49.2 | 29577 | 1561 |
| 2048 | 1 | 3 | multiclass | 3 | 3 | 6411 | 10 | 246 | 246 | 240 | 12.2 | 26041 | 1311 |
| 2048 | 4 | 3 | multiclass | 12 | 12 | 25644 | 10 | 946 | 946 | 927 | 12.7 | 27116 | 1529 |
| 2048 | 16 | 3 | multiclass | 48 | 48 | 102597 | 10 | 3949 | 3953 | 3875 | 12.2 | 25982 | 1622 |
| 8192 | 1 | 3 | multiclass | 3 | 3 | 24843 | 10 | 1213 | 1213 | 1189 | 2.5 | 20489 | 1360 |
| 8192 | 4 | 3 | multiclass | 12 | 12 | 99372 | 10 | 4831 | 4832 | 4754 | 2.5 | 20569 | 1360 |
| 8192 | 16 | 3 | multiclass | 48 | 48 | 397509 | 4 | 19339 | 19346 | 19015 | 2.5 | 20554 | 1360 |
| 2048 | 4 | 2 | multiclass | 8 | 8 | 17096 | 10 | 635 | 636 | 622 | 12.6 | 26920 | 1529 |
| 2048 | 4 | 8 | multiclass | 32 | 32 | 68384 | 10 | 2494 | 2495 | 2444 | 12.8 | 27418 | 1529 |
| 2048 | 16 | 1 | binary | 16 | 16 | 34055 | 10 | 1460 | 1460 | 1435 | 11.0 | 23333 | 1620 |
