# Serving benchmark

- x86_64 / cuda / bfloat16; torch 2.14.0+cu130, transformers 5.17.0; 2026-10-01T06:37:07+0000
- model `Qwen/Qwen3.5-4B` @ `851bf6e806` (shared-prefix tree, forward only: text once per request, each question once, then each candidate), adapter/checkpoint `weights/selfjev_4b_vision`, prompt `challenger-state-first-v1`
- batching: max_batch_tokens=4096 (padded), max_batch_size=None; warmup 1; samples per row in the `n` column (up to 20, at least 3, ~60 s budget per row)
- cold start: load 6648 ms + first request (3 pairs) 1192 ms
- e2e = parse + tokenize + forward + result assembly; model = forward passes incl. device sync

| state tok | questions | cand | type | pairs | state encodes | tokens processed | n | e2e p50 ms | e2e p95 ms | model p50 ms | pairs/s | tokens/s | cuda_peak_allocated_mb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2048 | 1 | 3 | multiclass | 3 | None | 2190 | 5 | 604 | 604 | 603 | 5.0 | 3627 | 3533 |
| 2048 | 10 | 3 | multiclass | 30 | None | 3064 | 5 | 761 | 762 | 757 | 39.4 | 4027 | 3551 |
| 8192 | 1 | 3 | multiclass | 3 | None | 8333 | 5 | 2559 | 2561 | 2558 | 1.2 | 3257 | 4609 |
| 8192 | 10 | 3 | multiclass | 30 | None | 9207 | 5 | 2823 | 2825 | 2820 | 10.6 | 3261 | 4636 |
| 16384 | 1 | 3 | multiclass | 3 | None | 16526 | 5 | 7178 | 7181 | 7177 | 0.4 | 2302 | 6157 |
| 16384 | 10 | 3 | multiclass | 30 | None | 17400 | 5 | 7260 | 7342 | 7256 | 4.1 | 2397 | 6198 |
| 2048 | 4 | 2 | multiclass | 8 | None | 2377 | 5 | 636 | 638 | 634 | 12.6 | 3738 | 3538 |
| 2048 | 4 | 8 | multiclass | 32 | None | 3001 | 5 | 756 | 757 | 752 | 42.3 | 3969 | 3550 |
| 2048 | 16 | 1 | binary | 16 | None | 2532 | 5 | 653 | 654 | 651 | 24.5 | 3878 | 3539 |
