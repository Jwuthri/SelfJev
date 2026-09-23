# Serving benchmark

- x86_64 / cuda / bfloat16; torch 2.14.0+cu130, transformers 5.17.0; 2026-09-23T22:27:11+0000
- model `Qwen/Qwen3-Reranker-8B` @ `77d193c791` (stock reranker pairs), adapter/checkpoint `runs/lora_8b/adapter`, prompt `task-v1`
- batching: max_batch_tokens=16384 (padded), max_batch_size=64; warmup 1; samples per row in the `n` column (up to 20, at least 3, ~60 s budget per row)
- cold start: load 2811 ms + first request (3 pairs) 926 ms
- e2e = parse + tokenize + forward + result assembly; model = forward passes incl. device sync

| state tok | questions | cand | type | pairs | state encodes | tokens processed | n | e2e p50 ms | e2e p95 ms | model p50 ms | pairs/s | tokens/s | cuda_peak_allocated_mb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 512 | 1 | 3 | multiclass | 3 | 3 | 1803 | 10 | 188 | 189 | 186 | 16.0 | 9610 | 15869 |
| 512 | 4 | 3 | multiclass | 12 | 12 | 7212 | 10 | 874 | 876 | 869 | 13.7 | 8254 | 16421 |
| 512 | 16 | 3 | multiclass | 48 | 48 | 28869 | 10 | 3577 | 3636 | 3561 | 13.4 | 8070 | 17335 |
| 2048 | 1 | 3 | multiclass | 3 | 3 | 6411 | 10 | 768 | 769 | 763 | 3.9 | 8347 | 16337 |
| 2048 | 4 | 3 | multiclass | 12 | 12 | 25644 | 10 | 3239 | 3259 | 3224 | 3.7 | 7917 | 17206 |
| 2048 | 16 | 3 | multiclass | 48 | 48 | 102597 | 5 | 13206 | 13255 | 13146 | 3.6 | 7769 | 17237 |
| 8192 | 1 | 3 | multiclass | 3 | 3 | 24843 | 10 | 3299 | 3320 | 3279 | 0.9 | 7531 | 16532 |
| 8192 | 4 | 3 | multiclass | 12 | 12 | 99372 | 5 | 13141 | 13293 | 13080 | 0.9 | 7562 | 16532 |
| 8192 | 16 | 3 | multiclass | 48 | 48 | 397509 | 3 | 51880 | 51979 | 51629 | 0.9 | 7662 | 16532 |
| 2048 | 4 | 2 | multiclass | 8 | 8 | 17096 | 10 | 2129 | 2138 | 2119 | 3.8 | 8030 | 17206 |
| 2048 | 4 | 8 | multiclass | 32 | 32 | 68384 | 8 | 8520 | 8605 | 8480 | 3.8 | 8026 | 17206 |
| 2048 | 16 | 1 | binary | 16 | 16 | 34055 | 10 | 4415 | 4457 | 4395 | 3.6 | 7713 | 17232 |
