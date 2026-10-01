# Serving benchmark

- x86_64 / cuda / bfloat16; torch 2.14.0+cu130, transformers 5.17.0; 2026-10-01T07:06:00+0000
- model `Qwen/Qwen3.5-4B` @ `851bf6e806` (shared-prefix tree, forward only: text once per request, each question once, then each candidate), adapter/checkpoint `weights/selfjev_4b_vision`, prompt `challenger-state-first-v1`
- batching: max_batch_tokens=4096 (padded), max_batch_size=None; warmup 1; samples per row in the `n` column (up to 20, at least 3, ~60 s budget per row)
- cold start: load 15385 ms + first request (3 pairs) 1191 ms
- e2e = parse + tokenize + forward + result assembly; model = forward passes incl. device sync

| state tok | questions | cand | type | pairs | state encodes | tokens processed | n | e2e p50 ms | e2e p95 ms | model p50 ms | pairs/s | tokens/s | cuda_peak_allocated_mb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2048 | 1 | 3 | multiclass | 3 | None | 2190 | 5 | 824 | 825 | 823 | 3.6 | 2658 | 4987 |
| 2048 | 10 | 3 | multiclass | 30 | None | 3064 | 5 | 988 | 991 | 984 | 30.4 | 3101 | 5004 |
| 8192 | 1 | 3 | multiclass | 3 | None | 8333 | 5 | 2941 | 2993 | 2940 | 1.0 | 2833 | 6064 |
| 8192 | 10 | 3 | multiclass | 30 | None | 9207 | 5 | 3214 | 3217 | 3210 | 9.3 | 2865 | 6091 |
| 16384 | 1 | 3 | multiclass | out of GPU memory |
| 16384 | 10 | 3 | multiclass | out of GPU memory |
| 2048 | 4 | 2 | multiclass | 8 | None | 2377 | 5 | 862 | 864 | 860 | 9.3 | 2757 | 4991 |
| 2048 | 4 | 8 | multiclass | 32 | None | 3001 | 5 | 984 | 987 | 980 | 32.5 | 3048 | 5004 |
| 2048 | 16 | 1 | binary | 16 | None | 2532 | 5 | 879 | 883 | 876 | 18.2 | 2880 | 4993 |
