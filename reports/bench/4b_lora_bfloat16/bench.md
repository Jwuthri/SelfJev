# Serving benchmark

- x86_64 / cuda / bfloat16; torch 2.14.0+cu130, transformers 5.17.0; 2026-09-23T20:54:16+0000
- model `Qwen/Qwen3-Reranker-4B` @ `22e683669b` (stock reranker pairs), adapter/checkpoint `runs/lora_4b/adapter`, prompt `task-v1`
- batching: max_batch_tokens=16384 (padded), max_batch_size=64; warmup 1; samples per row in the `n` column (up to 20, at least 3, ~60 s budget per row)
- cold start: load 2220 ms + first request (3 pairs) 856 ms
- e2e = parse + tokenize + forward + result assembly; model = forward passes incl. device sync

| state tok | questions | cand | type | pairs | state encodes | tokens processed | n | e2e p50 ms | e2e p95 ms | model p50 ms | pairs/s | tokens/s | cuda_peak_allocated_mb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 512 | 1 | 3 | multiclass | 3 | 3 | 1803 | 10 | 116 | 116 | 114 | 25.9 | 15572 | 7916 |
| 512 | 4 | 3 | multiclass | 12 | 12 | 7212 | 10 | 555 | 555 | 550 | 21.6 | 13006 | 8322 |
| 512 | 16 | 3 | multiclass | 48 | 48 | 28869 | 10 | 2383 | 2384 | 2367 | 20.1 | 12113 | 9002 |
| 2048 | 1 | 3 | multiclass | 3 | 3 | 6411 | 10 | 480 | 482 | 475 | 6.2 | 13343 | 8262 |
| 2048 | 4 | 3 | multiclass | 12 | 12 | 25644 | 10 | 2153 | 2156 | 2138 | 5.6 | 11910 | 8907 |
| 2048 | 16 | 3 | multiclass | 48 | 48 | 102597 | 7 | 8994 | 9039 | 8934 | 5.3 | 11407 | 8937 |
| 8192 | 1 | 3 | multiclass | 3 | 3 | 24843 | 10 | 2200 | 2201 | 2181 | 1.4 | 11292 | 8407 |
| 8192 | 4 | 3 | multiclass | 12 | 12 | 99372 | 7 | 8829 | 8859 | 8769 | 1.4 | 11255 | 8407 |
| 8192 | 16 | 3 | multiclass | 48 | 48 | 397509 | 3 | 35335 | 35404 | 35083 | 1.4 | 11250 | 8407 |
| 2048 | 4 | 2 | multiclass | 8 | 8 | 17096 | 10 | 1428 | 1432 | 1418 | 5.6 | 11972 | 8907 |
| 2048 | 4 | 8 | multiclass | 32 | 32 | 68384 | 10 | 5808 | 5822 | 5769 | 5.5 | 11774 | 8907 |
| 2048 | 16 | 1 | binary | 16 | 16 | 34055 | 10 | 3063 | 3069 | 3043 | 5.2 | 11119 | 8931 |
