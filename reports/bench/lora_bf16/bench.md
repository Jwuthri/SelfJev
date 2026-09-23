# Serving benchmark

- Apple M5 Pro / mps / bfloat16; torch 2.14.0, transformers 5.17.0; 2026-09-23T14:13:04-0700
- model `Qwen/Qwen3-Reranker-0.6B` @ `e61197ed45` (stock reranker pairs), adapter/checkpoint `runs/lora_pilot/adapter`, prompt `task-v1`
- batching: max_batch_tokens=16384 (padded), max_batch_size=64; warmup 1; samples per row in the `n` column (up to 20, at least 3, ~60 s budget per row)
- cold start: load 944 ms + first request (3 pairs) 322 ms
- e2e = parse + tokenize + forward + result assembly; model = forward passes incl. device sync

| state tok | questions | cand | type | pairs | state encodes | tokens processed | n | e2e p50 ms | e2e p95 ms | model p50 ms | pairs/s | tokens/s | mps_driver_allocated_mb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 512 | 1 | 3 | multiclass | 3 | 3 | 1803 | 20 | 337 | 408 | 335 | 8.9 | 5351 | 2235 |
| 512 | 4 | 3 | multiclass | 12 | 12 | 7212 | 20 | 1622 | 1689 | 1620 | 7.4 | 4445 | 2205 |
| 512 | 16 | 3 | multiclass | 48 | 48 | 28869 | 9 | 6702 | 6786 | 6695 | 7.2 | 4308 | 3241 |
| 2048 | 1 | 3 | multiclass | 3 | 3 | 6411 | 20 | 1496 | 1547 | 1492 | 2.0 | 4284 | 2203 |
| 2048 | 4 | 3 | multiclass | 12 | 12 | 25644 | 10 | 6258 | 6462 | 6252 | 1.9 | 4098 | 3237 |
| 2048 | 16 | 3 | multiclass | 48 | 48 | 102597 | 3 | 25941 | 25958 | 25921 | 1.9 | 3955 | 3237 |
| 8192 | 1 | 3 | multiclass | 3 | 3 | 24843 | 9 | 7413 | 7623 | 7399 | 0.4 | 3351 | 2201 |
| 8192 | 4 | 3 | multiclass | 12 | 12 | 99372 | 3 | 29662 | 29800 | 29641 | 0.4 | 3350 | 2201 |
| 8192 | 16 | 3 | multiclass | 48 | 48 | 397509 | 3 | 128583 | 128738 | 128503 | 0.4 | 3091 | 2201 |
| 2048 | 4 | 2 | multiclass | 8 | 8 | 17096 | 15 | 4115 | 4346 | 4110 | 1.9 | 4154 | 3237 |
| 2048 | 4 | 8 | multiclass | 32 | 32 | 68384 | 4 | 16383 | 16624 | 16371 | 2.0 | 4174 | 3237 |
| 2048 | 16 | 1 | binary | 16 | 16 | 34055 | 7 | 8702 | 8960 | 8695 | 1.8 | 3914 | 3238 |
