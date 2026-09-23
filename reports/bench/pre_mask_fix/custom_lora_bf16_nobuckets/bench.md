# Serving benchmark

- Apple M5 Pro / mps / bfloat16; torch 2.14.0, transformers 5.17.0; 2026-09-23T13:52:34-0700
- model `Qwen/Qwen3-Reranker-0.6B` @ `e61197ed45` (shared-state cross-attention (custom-v1)), adapter/checkpoint `runs/custom_lora/checkpoint`, prompt `custom-v1`
- batching: max_batch_tokens=16384 (padded), max_batch_size=64; warmup 1; samples per row in the `n` column (up to 20, at least 3, ~60 s budget per row)
- cold start: load 998 ms + first request (3 pairs) 579 ms
- e2e = parse + tokenize + forward + result assembly; model = forward passes incl. device sync

| state tok | questions | cand | type | pairs | state encodes | tokens processed | n | e2e p50 ms | e2e p95 ms | model p50 ms | pairs/s | tokens/s | mps_driver_allocated_mb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 512 | 1 | 3 | multiclass | 3 | 1 | 640 | 20 | 138 | 177 | 136 | 21.8 | 4652 | 1225 |
| 512 | 4 | 3 | multiclass | 12 | 1 | 1018 | 20 | 210 | 235 | 209 | 57.1 | 4845 | 1225 |
| 512 | 16 | 3 | multiclass | 48 | 1 | 2551 | 20 | 568 | 646 | 565 | 84.5 | 4489 | 2241 |
| 2048 | 1 | 3 | multiclass | 3 | 1 | 2176 | 20 | 511 | 680 | 506 | 5.9 | 4259 | 2250 |
| 2048 | 4 | 3 | multiclass | 12 | 1 | 2554 | 20 | 526 | 581 | 522 | 22.8 | 4860 | 2250 |
| 2048 | 16 | 3 | multiclass | 48 | 1 | 4087 | 20 | 817 | 872 | 813 | 58.7 | 5002 | 2242 |
| 8192 | 1 | 3 | multiclass | 3 | 1 | 8320 | 20 | 2698 | 3008 | 2680 | 1.1 | 3084 | 2218 |
| 8192 | 4 | 3 | multiclass | 12 | 1 | 8698 | 20 | 2818 | 3134 | 2807 | 4.3 | 3087 | 2218 |
| 8192 | 16 | 3 | multiclass | 48 | 1 | 10231 | 20 | 2987 | 3393 | 2974 | 16.1 | 3426 | 2210 |
| 2048 | 4 | 2 | multiclass | 8 | 1 | 2386 | 20 | 501 | 544 | 497 | 16.0 | 4765 | 2250 |
| 2048 | 4 | 8 | multiclass | 32 | 1 | 3394 | 20 | 660 | 763 | 656 | 48.5 | 5140 | 2242 |
| 2048 | 16 | 1 | binary | 16 | 1 | 2425 | 20 | 505 | 565 | 502 | 31.7 | 4800 | 2250 |
