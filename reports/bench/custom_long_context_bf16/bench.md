# Serving benchmark

- Apple M5 Pro / mps / bfloat16; torch 2.14.0, transformers 5.17.0; 2026-09-23T14:47:33-0700
- model `Qwen/Qwen3-Reranker-0.6B` @ `e61197ed45` (shared-state cross-attention (custom-v1)), adapter/checkpoint `runs/custom_lora/checkpoint`, prompt `custom-v1`
- batching: max_batch_tokens=16384 (padded), max_batch_size=64; warmup 1; samples per row in the `n` column (up to 20, at least 3, ~60 s budget per row)
- cold start: load 966 ms + first request (3 pairs) 245 ms
- e2e = parse + tokenize + forward + result assembly; model = forward passes incl. device sync

| state tok | questions | cand | type | pairs | state encodes | tokens processed | n | e2e p50 ms | e2e p95 ms | model p50 ms | pairs/s | tokens/s | mps_driver_allocated_mb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 16384 | 1 | 1 | binary | 1 | 1 | 16409 | 3 | 11129 | 11309 | 11108 | 0.1 | 1474 | 3233 |
| 32000 | 1 | 1 | binary | 1 | 1 | 32025 | 3 | 24418 | 24499 | 24374 | 0.0 | 1312 | 4283 |
| 16384 | 16 | 3 | multiclass | 48 | 1 | 18423 | 3 | 11680 | 11817 | 11642 | 4.1 | 1577 | 3234 |
| 32000 | 16 | 3 | multiclass | 48 | 1 | 34039 | 3 | 22566 | 22834 | 22524 | 2.1 | 1508 | 4276 |
