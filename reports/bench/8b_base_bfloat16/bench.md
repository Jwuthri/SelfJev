# Serving benchmark

- x86_64 / cuda / bfloat16; torch 2.14.0+cu130, transformers 5.17.0; 2026-09-23T22:16:14+0000
- model `Qwen/Qwen3-Reranker-8B` @ `77d193c791` (stock reranker pairs), adapter/checkpoint `None`, prompt `task-v1`
- batching: max_batch_tokens=16384 (padded), max_batch_size=64; warmup 1; samples per row in the `n` column (up to 20, at least 3, ~60 s budget per row)
- cold start: load 2310 ms + first request (3 pairs) 855 ms
- e2e = parse + tokenize + forward + result assembly; model = forward passes incl. device sync

| state tok | questions | cand | type | pairs | state encodes | tokens processed | n | e2e p50 ms | e2e p95 ms | model p50 ms | pairs/s | tokens/s | cuda_peak_allocated_mb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 512 | 1 | 3 | multiclass | 3 | 3 | 1803 | 10 | 162 | 164 | 161 | 18.5 | 11117 | 15810 |
| 512 | 4 | 3 | multiclass | 12 | 12 | 7212 | 10 | 709 | 725 | 705 | 16.9 | 10167 | 16363 |
| 512 | 16 | 3 | multiclass | 48 | 48 | 28869 | 10 | 2898 | 2934 | 2879 | 16.6 | 9960 | 17276 |
| 2048 | 1 | 3 | multiclass | 3 | 3 | 6411 | 10 | 661 | 667 | 656 | 4.5 | 9705 | 16279 |
| 2048 | 4 | 3 | multiclass | 12 | 12 | 25644 | 10 | 2688 | 2715 | 2672 | 4.5 | 9541 | 17148 |
| 2048 | 16 | 3 | multiclass | 48 | 48 | 102597 | 6 | 11043 | 11152 | 10984 | 4.3 | 9290 | 17179 |
| 8192 | 1 | 3 | multiclass | 3 | 3 | 24843 | 10 | 2886 | 2896 | 2867 | 1.0 | 8608 | 16473 |
| 8192 | 4 | 3 | multiclass | 12 | 12 | 99372 | 6 | 11304 | 11400 | 11244 | 1.1 | 8791 | 16473 |
| 8192 | 16 | 3 | multiclass | 48 | 48 | 397509 | 3 | 43813 | 45251 | 43559 | 1.1 | 9073 | 16473 |
| 2048 | 4 | 2 | multiclass | 8 | 8 | 17096 | 10 | 1786 | 1789 | 1776 | 4.5 | 9571 | 17148 |
| 2048 | 4 | 8 | multiclass | 32 | 32 | 68384 | 9 | 7238 | 7254 | 7198 | 4.4 | 9448 | 17148 |
| 2048 | 16 | 1 | binary | 16 | 16 | 34055 | 10 | 3759 | 3800 | 3738 | 4.3 | 9060 | 17175 |
