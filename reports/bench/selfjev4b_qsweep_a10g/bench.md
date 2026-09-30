# Serving benchmark

- x86_64 / cuda / bfloat16; torch 2.14.0+cu130, transformers 5.17.0; 2026-09-30T17:28:11+0000
- model `Qwen/Qwen3.5-4B` @ `851bf6e806` (shared-prefix tree, forward only: text once per request, each question once, then each candidate), adapter/checkpoint `weights/selfjev_4b_vision`, prompt `challenger-state-first-v1`
- batching: max_batch_tokens=16384 (padded), max_batch_size=None; warmup 1; samples per row in the `n` column (up to 20, at least 3, ~60 s budget per row)
- cold start: load 52251 ms + first request (3 pairs) 75418 ms
- e2e = parse + tokenize + forward + result assembly; model = forward passes incl. device sync

| state tok | questions | cand | type | pairs | state encodes | tokens processed | n | e2e p50 ms | e2e p95 ms | model p50 ms | pairs/s | tokens/s | cuda_peak_allocated_mb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 512 | 1 | 3 | multiclass | 3 | None | 654 | 20 | 241 | 247 | 240 | 12.4 | 2714 | 8225 |
| 512 | 5 | 3 | multiclass | 15 | None | 1042 | 20 | 319 | 325 | 316 | 47.0 | 3264 | 8482 |
| 512 | 10 | 3 | multiclass | 30 | None | 1528 | 20 | 401 | 403 | 396 | 74.8 | 3808 | 8571 |
| 512 | 25 | 3 | multiclass | 75 | None | 2998 | 20 | 735 | 736 | 724 | 102.0 | 4079 | 8884 |
| 512 | 50 | 3 | multiclass | 150 | None | 5448 | 20 | 1470 | 1480 | 1447 | 102.0 | 3706 | 9639 |
| 2048 | 1 | 3 | multiclass | 3 | None | 2190 | 20 | 584 | 594 | 583 | 5.1 | 3747 | 8481 |
| 2048 | 5 | 3 | multiclass | 15 | None | 2578 | 20 | 653 | 657 | 650 | 23.0 | 3946 | 8489 |
| 2048 | 10 | 3 | multiclass | 30 | None | 3064 | 20 | 741 | 743 | 736 | 40.5 | 4134 | 8499 |
| 2048 | 25 | 3 | multiclass | 75 | None | 4534 | 20 | 1165 | 1171 | 1153 | 64.4 | 3892 | 8917 |
| 2048 | 50 | 3 | multiclass | 150 | None | 6984 | 20 | 1945 | 1961 | 1923 | 77.1 | 3590 | 9678 |
| 8192 | 1 | 3 | multiclass | 3 | None | 8333 | 20 | 2558 | 2561 | 2557 | 1.2 | 3257 | 9559 |
| 8192 | 5 | 3 | multiclass | 15 | None | 8721 | 20 | 2678 | 2680 | 2675 | 5.6 | 3256 | 9571 |
| 8192 | 10 | 3 | multiclass | 30 | None | 9207 | 20 | 2825 | 2830 | 2819 | 10.6 | 3260 | 9585 |
| 8192 | 25 | 3 | multiclass | 75 | None | 10677 | 18 | 3436 | 3507 | 3423 | 21.8 | 3108 | 9636 |
| 8192 | 50 | 3 | multiclass | 150 | None | 13127 | 14 | 4576 | 4628 | 4553 | 32.8 | 2868 | 9888 |
| 16384 | 1 | 3 | multiclass | 3 | None | 16526 | 9 | 7157 | 7170 | 7156 | 0.4 | 2309 | 11104 |
| 16384 | 5 | 3 | multiclass | 15 | None | 16914 | 9 | 6991 | 7021 | 6987 | 2.1 | 2419 | 11122 |
| 16384 | 10 | 3 | multiclass | 30 | None | 17400 | 9 | 7404 | 7437 | 7398 | 4.1 | 2350 | 11145 |
| 16384 | 25 | 3 | multiclass | 75 | None | 18870 | 8 | 7545 | 7614 | 7532 | 9.9 | 2501 | 11219 |
| 16384 | 50 | 3 | multiclass | 150 | None | 21320 | 7 | 9607 | 9784 | 9584 | 15.6 | 2219 | 11349 |
| 32000 | 1 | 3 | multiclass | 3 | None | 32142 | 3 | 22019 | 22029 | 22017 | 0.1 | 1460 | 14510 |
| 32000 | 5 | 3 | multiclass | 15 | None | 32530 | 3 | 22434 | 22521 | 22431 | 0.7 | 1450 | 14644 |
| 32000 | 10 | 3 | multiclass | 30 | None | 33016 | 3 | 22978 | 23042 | 22971 | 1.3 | 1437 | 14473 |
| 32000 | 25 | 3 | multiclass | 75 | None | 34486 | 3 | 24643 | 24663 | 24630 | 3.0 | 1399 | 15356 |
| 32000 | 50 | 3 | multiclass | 150 | None | 36936 | 3 | 27760 | 28031 | 27737 | 5.4 | 1331 | 14794 |
| 2048 | 4 | 2 | multiclass | 8 | None | 2377 | 20 | 611 | 613 | 609 | 13.1 | 3892 | 8486 |
| 2048 | 4 | 8 | multiclass | 32 | None | 3001 | 20 | 738 | 746 | 733 | 43.3 | 4065 | 8595 |
| 2048 | 16 | 1 | binary | 16 | None | 2532 | 20 | 627 | 630 | 625 | 25.5 | 4036 | 8515 |
