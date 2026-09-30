# Serving benchmark

- x86_64 / cuda / bfloat16; torch 2.14.0+cu130, transformers 5.17.0; 2026-09-30T17:19:28+0000
- model `Qwen/Qwen3.5-4B` @ `851bf6e806` (shared-prefix tree, forward only: text once per request, each question once, then each candidate), adapter/checkpoint `weights/selfjev_4b_vision`, prompt `challenger-state-first-v1`
- batching: max_batch_tokens=16384 (padded), max_batch_size=None; warmup 1; samples per row in the `n` column (up to 20, at least 3, ~60 s budget per row)
- cold start: load 16656 ms + first request (3 pairs) 39210 ms
- e2e = parse + tokenize + forward + result assembly; model = forward passes incl. device sync

| state tok | questions | cand | type | pairs | state encodes | tokens processed | n | e2e p50 ms | e2e p95 ms | model p50 ms | pairs/s | tokens/s | cuda_peak_allocated_mb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 512 | 1 | 3 | multiclass | 3 | None | 654 | 20 | 145 | 149 | 145 | 20.6 | 4497 | 8225 |
| 512 | 5 | 3 | multiclass | 15 | None | 1042 | 20 | 156 | 158 | 154 | 96.2 | 6680 | 8482 |
| 512 | 10 | 3 | multiclass | 30 | None | 1528 | 20 | 179 | 180 | 175 | 167.4 | 8525 | 8571 |
| 512 | 25 | 3 | multiclass | 75 | None | 2998 | 20 | 311 | 313 | 301 | 240.8 | 9626 | 8884 |
| 512 | 50 | 3 | multiclass | 150 | None | 5448 | 20 | 644 | 648 | 625 | 232.8 | 8456 | 9639 |
| 2048 | 1 | 3 | multiclass | 3 | None | 2190 | 20 | 243 | 245 | 242 | 12.4 | 9025 | 8481 |
| 2048 | 5 | 3 | multiclass | 15 | None | 2578 | 20 | 269 | 271 | 266 | 55.8 | 9586 | 8489 |
| 2048 | 10 | 3 | multiclass | 30 | None | 3064 | 20 | 300 | 302 | 295 | 100.1 | 10225 | 8499 |
| 2048 | 25 | 3 | multiclass | 75 | None | 4534 | 20 | 484 | 502 | 473 | 155.1 | 9376 | 8917 |
| 2048 | 50 | 3 | multiclass | 150 | None | 6984 | 20 | 894 | 897 | 875 | 167.7 | 7810 | 9678 |
| 8192 | 1 | 3 | multiclass | 3 | None | 8333 | 20 | 1173 | 1177 | 1171 | 2.6 | 7107 | 9559 |
| 8192 | 5 | 3 | multiclass | 15 | None | 8721 | 20 | 1235 | 1241 | 1232 | 12.1 | 7059 | 9571 |
| 8192 | 10 | 3 | multiclass | 30 | None | 9207 | 20 | 1328 | 1343 | 1323 | 22.6 | 6933 | 9585 |
| 8192 | 25 | 3 | multiclass | 75 | None | 10677 | 20 | 1616 | 1622 | 1605 | 46.4 | 6605 | 9636 |
| 8192 | 50 | 3 | multiclass | 150 | None | 13127 | 20 | 2220 | 2223 | 2200 | 67.6 | 5914 | 9888 |
| 16384 | 1 | 3 | multiclass | 3 | None | 16526 | 20 | 3129 | 3138 | 3128 | 1.0 | 5281 | 11104 |
| 16384 | 5 | 3 | multiclass | 15 | None | 16914 | 19 | 3236 | 3244 | 3233 | 4.6 | 5226 | 11122 |
| 16384 | 10 | 3 | multiclass | 30 | None | 17400 | 18 | 3340 | 3345 | 3335 | 9.0 | 5209 | 11145 |
| 16384 | 25 | 3 | multiclass | 75 | None | 18870 | 16 | 3815 | 3819 | 3803 | 19.7 | 4947 | 11219 |
| 16384 | 50 | 3 | multiclass | 150 | None | 21320 | 13 | 4626 | 4629 | 4606 | 32.4 | 4609 | 11349 |
| 32000 | 1 | 3 | multiclass | 3 | None | 32142 | 7 | 9146 | 9287 | 9144 | 0.3 | 3514 | 14510 |
| 32000 | 5 | 3 | multiclass | 15 | None | 32530 | 7 | 9335 | 9443 | 9331 | 1.6 | 3485 | 14644 |
| 32000 | 10 | 3 | multiclass | 30 | None | 33016 | 7 | 9478 | 9659 | 9472 | 3.2 | 3483 | 14473 |
| 32000 | 25 | 3 | multiclass | 75 | None | 34486 | 6 | 10337 | 10374 | 10325 | 7.3 | 3336 | 15356 |
| 32000 | 50 | 3 | multiclass | 150 | None | 36936 | 6 | 11544 | 11696 | 11522 | 13.0 | 3200 | 14794 |
| 2048 | 4 | 2 | multiclass | 8 | None | 2377 | 20 | 255 | 256 | 253 | 31.4 | 9329 | 8486 |
| 2048 | 4 | 8 | multiclass | 32 | None | 3001 | 20 | 300 | 302 | 295 | 106.7 | 10006 | 8595 |
| 2048 | 16 | 1 | binary | 16 | None | 2532 | 20 | 270 | 272 | 267 | 59.3 | 9389 | 8515 |
