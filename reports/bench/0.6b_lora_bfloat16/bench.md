# Serving benchmark

- x86_64 / cuda / bfloat16; torch 2.14.0+cu130, transformers 5.17.0; 2026-09-23T22:33:09+0000
- model `Qwen/Qwen3-Reranker-0.6B` @ `e61197ed45` (stock reranker pairs), adapter/checkpoint `runs/lora_pilot/adapter`, prompt `task-v1`
- batching: max_batch_tokens=16384 (padded), max_batch_size=64; warmup 1; samples per row in the `n` column (up to 20, at least 3, ~60 s budget per row)
- cold start: load 1426 ms + first request (3 pairs) 791 ms
- e2e = parse + tokenize + forward + result assembly; model = forward passes incl. device sync

| state tok | questions | cand | type | pairs | state encodes | tokens processed | n | e2e p50 ms | e2e p95 ms | model p50 ms | pairs/s | tokens/s | cuda_peak_allocated_mb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 512 | 1 | 3 | multiclass | 3 | 3 | 1803 | 10 | 43 | 43 | 41 | 70.5 | 42367 | 1226 |
| 512 | 4 | 3 | multiclass | 12 | 12 | 7212 | 10 | 123 | 123 | 119 | 97.6 | 58655 | 1416 |
| 512 | 16 | 3 | multiclass | 48 | 48 | 28869 | 10 | 608 | 608 | 592 | 79.0 | 47497 | 1735 |
| 2048 | 1 | 3 | multiclass | 3 | 3 | 6411 | 10 | 110 | 110 | 105 | 27.2 | 58134 | 1391 |
| 2048 | 4 | 3 | multiclass | 12 | 12 | 25644 | 10 | 553 | 553 | 538 | 21.7 | 46399 | 1690 |
| 2048 | 16 | 3 | multiclass | 48 | 48 | 102597 | 10 | 2371 | 2375 | 2312 | 20.2 | 43267 | 1721 |
| 8192 | 1 | 3 | multiclass | 3 | 3 | 24843 | 10 | 553 | 553 | 533 | 5.4 | 44960 | 1457 |
| 8192 | 4 | 3 | multiclass | 12 | 12 | 99372 | 10 | 2194 | 2194 | 2133 | 5.5 | 45302 | 1457 |
| 8192 | 16 | 3 | multiclass | 48 | 48 | 397509 | 7 | 8780 | 8798 | 8526 | 5.5 | 45276 | 1457 |
| 2048 | 4 | 2 | multiclass | 8 | 8 | 17096 | 10 | 382 | 384 | 372 | 21.0 | 44789 | 1690 |
| 2048 | 4 | 8 | multiclass | 32 | 32 | 68384 | 10 | 1513 | 1514 | 1474 | 21.1 | 45185 | 1690 |
| 2048 | 16 | 1 | binary | 16 | 16 | 34055 | 10 | 819 | 820 | 800 | 19.5 | 41557 | 1718 |
