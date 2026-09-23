# Serving benchmark

- x86_64 / cuda / bfloat16; torch 2.14.0+cu130, transformers 5.17.0; 2026-09-23T21:47:16+0000
- model `Qwen/Qwen3-Reranker-0.6B` @ `e61197ed45` (shared-state cross-attention (custom-v1)), adapter/checkpoint `runs/custom_sim_lora/checkpoint`, prompt `custom-v1`
- batching: max_batch_tokens=16384 (padded), max_batch_size=64; warmup 1; samples per row in the `n` column (up to 20, at least 3, ~60 s budget per row)
- cold start: load 1699 ms + first request (3 pairs) 1095 ms
- e2e = parse + tokenize + forward + result assembly; model = forward passes incl. device sync

| state tok | questions | cand | type | pairs | state encodes | tokens processed | n | e2e p50 ms | e2e p95 ms | model p50 ms | pairs/s | tokens/s | cuda_peak_allocated_mb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 512 | 1 | 3 | multiclass | 3 | 1 | 640 | 10 | 95 | 96 | 94 | 31.5 | 6714 | 1192 |
| 512 | 4 | 3 | multiclass | 12 | 1 | 1018 | 10 | 97 | 98 | 95 | 124.1 | 10530 | 1192 |
| 512 | 16 | 3 | multiclass | 48 | 1 | 2551 | 10 | 158 | 159 | 154 | 304.8 | 16197 | 1245 |
| 2048 | 1 | 3 | multiclass | 3 | 1 | 2176 | 10 | 164 | 165 | 160 | 18.3 | 13253 | 1243 |
| 2048 | 4 | 3 | multiclass | 12 | 1 | 2554 | 10 | 166 | 166 | 161 | 72.4 | 15413 | 1243 |
| 2048 | 16 | 3 | multiclass | 48 | 1 | 4087 | 10 | 227 | 227 | 221 | 211.4 | 18000 | 1253 |
| 8192 | 1 | 3 | multiclass | 3 | 1 | 8320 | 10 | 558 | 559 | 542 | 5.4 | 14915 | 1462 |
| 8192 | 4 | 3 | multiclass | 12 | 1 | 8698 | 10 | 560 | 561 | 544 | 21.4 | 15532 | 1462 |
| 8192 | 16 | 3 | multiclass | 48 | 1 | 10231 | 10 | 626 | 627 | 608 | 76.6 | 16334 | 1462 |
| 2048 | 4 | 2 | multiclass | 8 | 1 | 2386 | 10 | 164 | 166 | 160 | 48.7 | 14523 | 1243 |
| 2048 | 4 | 8 | multiclass | 32 | 1 | 3394 | 10 | 191 | 191 | 185 | 167.7 | 17786 | 1243 |
| 2048 | 16 | 1 | binary | 16 | 1 | 2425 | 10 | 164 | 165 | 160 | 97.3 | 14752 | 1243 |
