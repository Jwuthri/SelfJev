# Serving benchmark

- x86_64 / cuda / bfloat16; torch 2.14.0+cu130, transformers 5.17.0; 2026-09-23T21:51:23+0000
- model `Qwen/Qwen3-Reranker-0.6B` @ `e61197ed45` (stock reranker pairs), adapter/checkpoint `runs/lora_pilot/adapter`, prompt `task-v1`
- batching: max_batch_tokens=16384 (padded), max_batch_size=64; warmup 1; samples per row in the `n` column (up to 20, at least 3, ~60 s budget per row)
- cold start: load 1647 ms + first request (3 pairs) 927 ms
- e2e = parse + tokenize + forward + result assembly; model = forward passes incl. device sync

| state tok | questions | cand | type | pairs | state encodes | tokens processed | n | e2e p50 ms | e2e p95 ms | model p50 ms | pairs/s | tokens/s | cuda_peak_allocated_mb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 16384 | 1 | 1 | binary | 1 | 1 | 16464 | 2 | 1254 | 1254 | 1223 | 0.8 | 13133 | 1749 |
| 32000 | 1 | 1 | binary | 1 | 1 | 32080 | 2 | 3362 | 3365 | 3305 | 0.3 | 9543 | 2308 |
| 16384 | 16 | 3 | multiclass | 48 | 48 | 790725 | 2 | 59392 | 59399 | 58698 | 0.8 | 13314 | 1750 |
