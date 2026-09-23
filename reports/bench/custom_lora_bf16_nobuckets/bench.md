# Serving benchmark

- Apple M5 Pro / mps / bfloat16; torch 2.14.0, transformers 5.17.0; 2026-09-23T14:42:53-0700
- model `Qwen/Qwen3-Reranker-0.6B` @ `e61197ed45` (shared-state cross-attention (custom-v1)), adapter/checkpoint `runs/custom_lora/checkpoint`, prompt `custom-v1`
- batching: max_batch_tokens=16384 (padded), max_batch_size=64; warmup 1; samples per row in the `n` column (up to 20, at least 3, ~60 s budget per row)
- cold start: load 982 ms + first request (3 pairs) 230 ms
- e2e = parse + tokenize + forward + result assembly; model = forward passes incl. device sync

| state tok | questions | cand | type | pairs | state encodes | tokens processed | n | e2e p50 ms | e2e p95 ms | model p50 ms | pairs/s | tokens/s | mps_driver_allocated_mb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 512 | 1 | 3 | multiclass | 3 | 1 | 640 | 20 | 102 | 179 | 101 | 29.4 | 6275 | 1225 |
| 512 | 4 | 3 | multiclass | 12 | 1 | 1018 | 20 | 216 | 256 | 214 | 55.6 | 4714 | 1225 |
| 512 | 16 | 3 | multiclass | 48 | 1 | 2551 | 20 | 574 | 639 | 572 | 83.6 | 4442 | 2241 |
| 2048 | 1 | 3 | multiclass | 3 | 1 | 2176 | 20 | 534 | 608 | 531 | 5.6 | 4071 | 2249 |
| 2048 | 4 | 3 | multiclass | 12 | 1 | 2554 | 20 | 591 | 682 | 587 | 20.3 | 4321 | 2249 |
| 2048 | 16 | 3 | multiclass | 48 | 1 | 4087 | 20 | 958 | 1046 | 953 | 50.1 | 4268 | 2241 |
| 8192 | 1 | 3 | multiclass | 3 | 1 | 8320 | 20 | 2952 | 3026 | 2941 | 1.0 | 2818 | 2218 |
| 8192 | 4 | 3 | multiclass | 12 | 1 | 8698 | 20 | 3044 | 3203 | 3031 | 3.9 | 2857 | 2218 |
| 8192 | 16 | 3 | multiclass | 48 | 1 | 10231 | 18 | 3385 | 3446 | 3372 | 14.2 | 3022 | 2210 |
| 2048 | 4 | 2 | multiclass | 8 | 1 | 2386 | 20 | 567 | 641 | 564 | 14.1 | 4206 | 2250 |
| 2048 | 4 | 8 | multiclass | 32 | 1 | 3394 | 20 | 790 | 842 | 784 | 40.5 | 4294 | 2242 |
| 2048 | 16 | 1 | binary | 16 | 1 | 2425 | 20 | 576 | 673 | 572 | 27.8 | 4210 | 2250 |
