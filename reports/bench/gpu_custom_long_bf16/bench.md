# Serving benchmark

- x86_64 / cuda / bfloat16; torch 2.14.0+cu130, transformers 5.17.0; 2026-09-23T21:48:03+0000
- model `Qwen/Qwen3-Reranker-0.6B` @ `e61197ed45` (shared-state cross-attention (custom-v1)), adapter/checkpoint `runs/custom_sim_lora/checkpoint`, prompt `custom-v1`
- batching: max_batch_tokens=16384 (padded), max_batch_size=64; warmup 1; samples per row in the `n` column (up to 20, at least 3, ~60 s budget per row)
- cold start: load 1688 ms + first request (3 pairs) 1082 ms
- e2e = parse + tokenize + forward + result assembly; model = forward passes incl. device sync

| state tok | questions | cand | type | pairs | state encodes | tokens processed | n | e2e p50 ms | e2e p95 ms | model p50 ms | pairs/s | tokens/s | cuda_peak_allocated_mb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 16384 | 1 | 1 | binary | 1 | 1 | 16409 | 3 | 1304 | 1309 | 1273 | 0.8 | 12580 | 1755 |
| 32000 | 1 | 1 | binary | 1 | 1 | 32025 | 3 | 3428 | 3431 | 3366 | 0.3 | 9342 | 2314 |
| 16384 | 16 | 3 | multiclass | 48 | 1 | 18423 | 3 | 1379 | 1379 | 1346 | 34.8 | 13357 | 1755 |
| 32000 | 16 | 3 | multiclass | 48 | 1 | 34039 | 3 | 3524 | 3524 | 3459 | 13.6 | 9660 | 2314 |
