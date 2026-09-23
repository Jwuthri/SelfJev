# Serving benchmark

- Apple M5 Pro / mps / bfloat16; torch 2.14.0, transformers 5.17.0; 2026-09-23T13:47:53-0700
- model `Qwen/Qwen3-Reranker-0.6B` @ `e61197ed45` (shared-state cross-attention (custom-v1)), adapter/checkpoint `runs/custom_lora/checkpoint`, prompt `custom-v1`
- batching: max_batch_tokens=16384 (padded), max_batch_size=64; warmup 1; samples per row in the `n` column (up to 20, at least 3, ~60 s budget per row)
- cold start: load 1017 ms + first request (3 pairs) 674 ms
- e2e = parse + tokenize + forward + result assembly; model = forward passes incl. device sync

| state tok | questions | cand | type | pairs | state encodes | tokens processed | n | e2e p50 ms | e2e p95 ms | model p50 ms | pairs/s | tokens/s | mps_driver_allocated_mb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 512 | 1 | 3 | multiclass | 3 | 1 | 640 | 20 | 158 | 175 | 157 | 19.0 | 4054 | 1257 |
| 512 | 4 | 3 | multiclass | 12 | 1 | 1018 | 20 | 227 | 275 | 225 | 53.0 | 4492 | 1257 |
| 512 | 16 | 3 | multiclass | 48 | 1 | 2551 | 20 | 618 | 674 | 615 | 77.7 | 4129 | 2281 |
| 2048 | 1 | 3 | multiclass | 3 | 1 | 2176 | 20 | 704 | 819 | 701 | 4.3 | 3090 | 2249 |
| 2048 | 4 | 3 | multiclass | 12 | 1 | 2554 | 20 | 760 | 942 | 756 | 15.8 | 3360 | 2241 |
| 2048 | 16 | 3 | multiclass | 48 | 1 | 4087 | 20 | 1188 | 1362 | 1183 | 40.4 | 3441 | 2241 |
| 8192 | 1 | 3 | multiclass | 3 | 1 | 8320 | 10 | 6073 | 7109 | 6062 | 0.5 | 1370 | 3241 |
| 8192 | 4 | 3 | multiclass | 12 | 1 | 8698 | 10 | 6000 | 6541 | 5987 | 2.0 | 1450 | 3233 |
| 8192 | 16 | 3 | multiclass | 48 | 1 | 10231 | 10 | 6486 | 6754 | 6472 | 7.4 | 1577 | 3233 |
| 2048 | 4 | 2 | multiclass | 8 | 1 | 2386 | 20 | 753 | 876 | 748 | 10.6 | 3168 | 2249 |
| 2048 | 4 | 8 | multiclass | 32 | 1 | 3394 | 20 | 1055 | 1195 | 1051 | 30.3 | 3216 | 2241 |
| 2048 | 16 | 1 | binary | 16 | 1 | 2425 | 20 | 851 | 907 | 847 | 18.8 | 2849 | 2250 |
