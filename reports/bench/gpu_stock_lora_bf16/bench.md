# Serving benchmark

- x86_64 / cuda / bfloat16; torch 2.14.0+cu130, transformers 5.17.0; 2026-09-23T21:46:32+0000
- model `Qwen/Qwen3-Reranker-0.6B` @ `e61197ed45` (stock reranker pairs), adapter/checkpoint `runs/lora_pilot/adapter`, prompt `task-v1`
- batching: max_batch_tokens=16384 (padded), max_batch_size=64; warmup 1; samples per row in the `n` column (up to 20, at least 3, ~60 s budget per row)
- cold start: load 1689 ms + first request (3 pairs) 924 ms
- e2e = parse + tokenize + forward + result assembly; model = forward passes incl. device sync

| state tok | questions | cand | type | pairs | state encodes | tokens processed | n | e2e p50 ms | e2e p95 ms | model p50 ms | pairs/s | tokens/s | cuda_peak_allocated_mb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 512 | 1 | 3 | multiclass | 3 | 3 | 1803 | 10 | 96 | 96 | 94 | 31.3 | 18799 | 1226 |
| 512 | 4 | 3 | multiclass | 12 | 12 | 7212 | 10 | 334 | 334 | 329 | 35.9 | 21590 | 1416 |
| 512 | 16 | 3 | multiclass | 48 | 48 | 28869 | 10 | 1312 | 1313 | 1293 | 36.6 | 21996 | 1735 |
| 2048 | 1 | 3 | multiclass | 3 | 3 | 6411 | 10 | 323 | 324 | 317 | 9.3 | 19825 | 1391 |
| 2048 | 4 | 3 | multiclass | 12 | 12 | 25644 | 10 | 1245 | 1245 | 1226 | 9.6 | 20605 | 1690 |
| 2048 | 16 | 3 | multiclass | 48 | 48 | 102597 | 10 | 5138 | 5141 | 5065 | 9.3 | 19967 | 1721 |
| 8192 | 1 | 3 | multiclass | 3 | 3 | 24843 | 10 | 1505 | 1506 | 1482 | 2.0 | 16507 | 1457 |
| 8192 | 4 | 3 | multiclass | 12 | 12 | 99372 | 10 | 6000 | 6008 | 5923 | 2.0 | 16562 | 1457 |
| 8192 | 16 | 3 | multiclass | 48 | 48 | 397509 | 3 | 24024 | 24024 | 23698 | 2.0 | 16546 | 1457 |
| 2048 | 4 | 2 | multiclass | 8 | 8 | 17096 | 10 | 835 | 836 | 822 | 9.6 | 20473 | 1690 |
| 2048 | 4 | 8 | multiclass | 32 | 32 | 68384 | 10 | 3287 | 3289 | 3238 | 9.7 | 20804 | 1690 |
| 2048 | 16 | 1 | binary | 16 | 16 | 34055 | 10 | 1857 | 1857 | 1832 | 8.6 | 18343 | 1718 |
