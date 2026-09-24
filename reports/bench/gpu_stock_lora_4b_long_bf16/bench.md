# Serving benchmark

- x86_64 / cuda / bfloat16; torch 2.14.0+cu130, transformers 5.17.0; 2026-09-24T01:04:11+0000
- model `Qwen/Qwen3-Reranker-4B` @ `22e683669b` (stock reranker pairs), adapter/checkpoint `runs/lora_4b/adapter`, prompt `task-v1`
- batching: max_batch_tokens=16384 (padded), max_batch_size=64; warmup 1; samples per row in the `n` column (up to 20, at least 3, ~60 s budget per row)
- cold start: load 9428 ms + first request (3 pairs) 3037 ms
- e2e = parse + tokenize + forward + result assembly; model = forward passes incl. device sync

| state tok | questions | cand | type | pairs | state encodes | tokens processed | n | e2e p50 ms | e2e p95 ms | model p50 ms | pairs/s | tokens/s | cuda_peak_allocated_mb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 16384 | 1 | 1 | binary | 1 | 1 | 16464 | 2 | 4324 | 4325 | 4294 | 0.2 | 3808 | 9027 |
| 16384 | 16 | 3 | multiclass | 48 | 48 | 790725 | 2 | 206915 | 206916 | 206228 | 0.2 | 3821 | 9027 |
