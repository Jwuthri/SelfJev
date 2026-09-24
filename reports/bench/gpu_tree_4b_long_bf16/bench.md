# Serving benchmark

- x86_64 / cuda / bfloat16; torch 2.14.0+cu130, transformers 5.17.0; 2026-09-24T00:53:17+0000
- model `Qwen/Qwen3-Reranker-4B` @ `22e683669b` (shared-prefix tree (tree-v1)), adapter/checkpoint `runs/tree_4b/adapter`, prompt `tree-v1`
- batching: max_batch_tokens=16384 (padded), max_batch_size=64; warmup 1; samples per row in the `n` column (up to 20, at least 3, ~60 s budget per row)
- cold start: load 4023 ms + first request (3 pairs) 1664 ms
- e2e = parse + tokenize + forward + result assembly; model = forward passes incl. device sync

| state tok | questions | cand | type | pairs | state encodes | tokens processed | n | e2e p50 ms | e2e p95 ms | model p50 ms | pairs/s | tokens/s | cuda_peak_allocated_mb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 16384 | 1 | 1 | binary | 1 | 1 | 16483 | 3 | 4483 | 4484 | 4455 | 0.2 | 3676 | 11332 |
| 32000 | 1 | 1 | binary | 1 | 1 | 32099 | 3 | 11840 | 11859 | 11782 | 0.1 | 2711 | 14710 |
| 16384 | 16 | 3 | multiclass | 48 | 1 | 18546 | 3 | 5638 | 5638 | 5608 | 8.5 | 3289 | 11332 |
| 32000 | 16 | 3 | multiclass | 48 | 1 | 34162 | 3 | 14235 | 14238 | 14175 | 3.4 | 2400 | 14710 |
