# Serving benchmark

- x86_64 / cuda / bfloat16; torch 2.14.0+cu130, transformers 5.17.0; 2026-09-23T20:46:03+0000
- model `Qwen/Qwen3-Reranker-4B` @ `22e683669b` (stock reranker pairs), adapter/checkpoint `None`, prompt `task-v1`
- batching: max_batch_tokens=16384 (padded), max_batch_size=64; warmup 1; samples per row in the `n` column (up to 20, at least 3, ~60 s budget per row)
- cold start: load 1762 ms + first request (3 pairs) 794 ms
- e2e = parse + tokenize + forward + result assembly; model = forward passes incl. device sync

| state tok | questions | cand | type | pairs | state encodes | tokens processed | n | e2e p50 ms | e2e p95 ms | model p50 ms | pairs/s | tokens/s | cuda_peak_allocated_mb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 512 | 1 | 3 | multiclass | 3 | 3 | 1803 | 10 | 99 | 100 | 98 | 30.2 | 18150 | 7871 |
| 512 | 4 | 3 | multiclass | 12 | 12 | 7212 | 10 | 439 | 439 | 435 | 27.3 | 16435 | 8277 |
| 512 | 16 | 3 | multiclass | 48 | 48 | 28869 | 10 | 1867 | 1869 | 1850 | 25.7 | 15465 | 8957 |
| 2048 | 1 | 3 | multiclass | 3 | 3 | 6411 | 10 | 390 | 393 | 385 | 7.7 | 16440 | 8217 |
| 2048 | 4 | 3 | multiclass | 12 | 12 | 25644 | 10 | 1698 | 1700 | 1683 | 7.1 | 15103 | 8862 |
| 2048 | 16 | 3 | multiclass | 48 | 48 | 102597 | 9 | 7121 | 7193 | 7061 | 6.7 | 14408 | 8892 |
| 8192 | 1 | 3 | multiclass | 3 | 3 | 24843 | 10 | 1793 | 1805 | 1773 | 1.7 | 13859 | 8362 |
| 8192 | 4 | 3 | multiclass | 12 | 12 | 99372 | 9 | 7109 | 7152 | 7049 | 1.7 | 13978 | 8362 |
| 8192 | 16 | 3 | multiclass | 48 | 48 | 397509 | 3 | 29076 | 29325 | 28819 | 1.7 | 13672 | 8362 |
| 2048 | 4 | 2 | multiclass | 8 | 8 | 17096 | 10 | 1131 | 1137 | 1121 | 7.1 | 15112 | 8862 |
| 2048 | 4 | 8 | multiclass | 32 | 32 | 68384 | 10 | 4550 | 4677 | 4510 | 7.0 | 15030 | 8862 |
| 2048 | 16 | 1 | binary | 16 | 16 | 34055 | 10 | 2420 | 2423 | 2400 | 6.6 | 14073 | 8886 |
