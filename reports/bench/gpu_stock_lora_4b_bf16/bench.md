# Serving benchmark

- x86_64 / cuda / bfloat16; torch 2.14.0+cu130, transformers 5.17.0; 2026-09-24T00:50:37+0000
- model `Qwen/Qwen3-Reranker-4B` @ `22e683669b` (stock reranker pairs), adapter/checkpoint `runs/lora_4b/adapter`, prompt `task-v1`
- batching: max_batch_tokens=16384 (padded), max_batch_size=64; warmup 1; samples per row in the `n` column (up to 20, at least 3, ~60 s budget per row)
- cold start: load 23922 ms + first request (3 pairs) 3920 ms
- e2e = parse + tokenize + forward + result assembly; model = forward passes incl. device sync

| state tok | questions | cand | type | pairs | state encodes | tokens processed | n | e2e p50 ms | e2e p95 ms | model p50 ms | pairs/s | tokens/s | cuda_peak_allocated_mb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 512 | 1 | 3 | multiclass | 3 | 3 | 1803 | 10 | 375 | 375 | 373 | 8.0 | 4809 | 7916 |
| 512 | 4 | 3 | multiclass | 12 | 12 | 7212 | 10 | 1402 | 1402 | 1397 | 8.6 | 5144 | 8322 |
| 512 | 16 | 3 | multiclass | 48 | 48 | 28869 | 10 | 5414 | 5415 | 5394 | 8.9 | 5332 | 9002 |
| 2048 | 1 | 3 | multiclass | 3 | 3 | 6411 | 10 | 1299 | 1299 | 1293 | 2.3 | 4936 | 8262 |
| 2048 | 4 | 3 | multiclass | 12 | 12 | 25644 | 10 | 5005 | 5006 | 4987 | 2.4 | 5123 | 8907 |
| 2048 | 16 | 3 | multiclass | 48 | 48 | 102597 | 3 | 20460 | 20461 | 20387 | 2.3 | 5014 | 8937 |
| 8192 | 1 | 3 | multiclass | 3 | 3 | 24843 | 10 | 5657 | 5657 | 5633 | 0.5 | 4392 | 8407 |
| 8192 | 4 | 3 | multiclass | 12 | 12 | 99372 | 3 | 22607 | 22607 | 22531 | 0.5 | 4396 | 8407 |
| 8192 | 16 | 3 | multiclass | 48 | 48 | 397509 | 3 | 90449 | 90450 | 90124 | 0.5 | 4395 | 8407 |
| 2048 | 4 | 2 | multiclass | 8 | 8 | 17096 | 10 | 3374 | 3375 | 3362 | 2.4 | 5067 | 8907 |
| 2048 | 4 | 8 | multiclass | 32 | 32 | 68384 | 5 | 13317 | 13318 | 13268 | 2.4 | 5135 | 8907 |
| 2048 | 16 | 1 | binary | 16 | 16 | 34055 | 9 | 7176 | 7177 | 7152 | 2.2 | 4745 | 8931 |
