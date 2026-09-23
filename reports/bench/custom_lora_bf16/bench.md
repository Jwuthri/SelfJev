# Serving benchmark

- Apple M5 Pro / mps / bfloat16; torch 2.14.0, transformers 5.17.0; 2026-09-23T14:37:52-0700
- model `Qwen/Qwen3-Reranker-0.6B` @ `e61197ed45` (shared-state cross-attention (custom-v1)), adapter/checkpoint `runs/custom_lora/checkpoint`, prompt `custom-v1`
- batching: max_batch_tokens=16384 (padded), max_batch_size=64; warmup 1; samples per row in the `n` column (up to 20, at least 3, ~60 s budget per row)
- cold start: load 1036 ms + first request (3 pairs) 243 ms
- e2e = parse + tokenize + forward + result assembly; model = forward passes incl. device sync

| state tok | questions | cand | type | pairs | state encodes | tokens processed | n | e2e p50 ms | e2e p95 ms | model p50 ms | pairs/s | tokens/s | mps_driver_allocated_mb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 512 | 1 | 3 | multiclass | 3 | 1 | 640 | 20 | 180 | 200 | 179 | 16.6 | 3551 | 1257 |
| 512 | 4 | 3 | multiclass | 12 | 1 | 1018 | 20 | 238 | 302 | 237 | 50.3 | 4271 | 1257 |
| 512 | 16 | 3 | multiclass | 48 | 1 | 2551 | 20 | 638 | 723 | 636 | 75.2 | 3998 | 2273 |
| 2048 | 1 | 3 | multiclass | 3 | 1 | 2176 | 20 | 664 | 732 | 661 | 4.5 | 3277 | 2281 |
| 2048 | 4 | 3 | multiclass | 12 | 1 | 2554 | 20 | 736 | 786 | 732 | 16.3 | 3470 | 2273 |
| 2048 | 16 | 3 | multiclass | 48 | 1 | 4087 | 20 | 1150 | 1207 | 1146 | 41.7 | 3553 | 2273 |
| 8192 | 1 | 3 | multiclass | 3 | 1 | 8320 | 16 | 3937 | 4081 | 3926 | 0.8 | 2113 | 2217 |
| 8192 | 4 | 3 | multiclass | 12 | 1 | 8698 | 15 | 4086 | 4164 | 4075 | 2.9 | 2129 | 2209 |
| 8192 | 16 | 3 | multiclass | 48 | 1 | 10231 | 14 | 4496 | 4559 | 4483 | 10.7 | 2276 | 2209 |
| 2048 | 4 | 2 | multiclass | 8 | 1 | 2386 | 20 | 724 | 760 | 720 | 11.1 | 3298 | 2281 |
| 2048 | 4 | 8 | multiclass | 32 | 1 | 3394 | 20 | 968 | 1103 | 963 | 33.1 | 3507 | 2273 |
| 2048 | 16 | 1 | binary | 16 | 1 | 2425 | 20 | 729 | 781 | 726 | 21.9 | 3326 | 2281 |
