# Serving benchmark

- x86_64 / cuda / bfloat16; torch 2.14.0+cu130, transformers 5.17.0; 2026-09-24T00:34:26+0000
- model `Qwen/Qwen3-Reranker-4B` @ `22e683669b` (shared-prefix tree (tree-v1)), adapter/checkpoint `runs/tree_4b/adapter`, prompt `tree-v1`
- batching: max_batch_tokens=16384 (padded), max_batch_size=64; warmup 1; samples per row in the `n` column (up to 20, at least 3, ~60 s budget per row)
- cold start: load 32306 ms + first request (3 pairs) 1113 ms
- e2e = parse + tokenize + forward + result assembly; model = forward passes incl. device sync

| state tok | questions | cand | type | pairs | state encodes | tokens processed | n | e2e p50 ms | e2e p95 ms | model p50 ms | pairs/s | tokens/s | cuda_peak_allocated_mb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 512 | 1 | 3 | multiclass | 3 | 1 | 687 | 10 | 192 | 193 | 191 | 15.6 | 3575 | 7916 |
| 512 | 4 | 3 | multiclass | 12 | 1 | 1083 | 10 | 267 | 267 | 265 | 44.9 | 4054 | 7995 |
| 512 | 16 | 3 | multiclass | 48 | 1 | 2674 | 10 | 686 | 691 | 683 | 70.0 | 3900 | 8345 |
| 2048 | 1 | 3 | multiclass | 3 | 1 | 2223 | 10 | 526 | 527 | 522 | 5.7 | 4224 | 8230 |
| 2048 | 4 | 3 | multiclass | 12 | 1 | 2619 | 10 | 621 | 622 | 617 | 19.3 | 4215 | 8230 |
| 2048 | 16 | 3 | multiclass | 48 | 1 | 4210 | 10 | 1091 | 1095 | 1085 | 44.0 | 3858 | 8553 |
| 8192 | 1 | 3 | multiclass | 3 | 1 | 8367 | 10 | 2012 | 2014 | 1998 | 1.5 | 4158 | 9560 |
| 8192 | 4 | 3 | multiclass | 12 | 1 | 8763 | 10 | 2147 | 2148 | 2132 | 5.6 | 4081 | 9560 |
| 8192 | 16 | 3 | multiclass | 48 | 1 | 10354 | 10 | 2798 | 2798 | 2782 | 17.2 | 3700 | 9560 |
| 2048 | 4 | 2 | multiclass | 8 | 1 | 2503 | 10 | 582 | 587 | 578 | 13.7 | 4300 | 8230 |
| 2048 | 4 | 8 | multiclass | 32 | 1 | 3199 | 10 | 789 | 796 | 784 | 40.6 | 4055 | 8329 |
| 2048 | 16 | 1 | binary | 16 | 1 | 2994 | 10 | 712 | 717 | 707 | 22.5 | 4207 | 8296 |
