# Serving benchmark

- x86_64 / cuda / bfloat16; torch 2.14.0+cu130, transformers 5.17.0; 2026-09-30T17:20:37+0000
- model `Qwen/Qwen3.5-4B` @ `851bf6e806` (shared-prefix tree, forward only: text once per request, each question once, then each candidate), adapter/checkpoint `weights/selfjev_4b_vision`, prompt `challenger-state-first-v1`
- batching: max_batch_tokens=16384 (padded), max_batch_size=None; warmup 1; samples per row in the `n` column (up to 20, at least 3, ~60 s budget per row)
- cold start: load 16764 ms + first request (3 pairs) 47461 ms
- e2e = parse + tokenize + forward + result assembly; model = forward passes incl. device sync

| state tok | questions | cand | type | pairs | state encodes | tokens processed | n | e2e p50 ms | e2e p95 ms | model p50 ms | pairs/s | tokens/s | cuda_peak_allocated_mb |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 512 | 1 | 3 | multiclass | 3 | None | 654 | 20 | 146 | 147 | 146 | 20.5 | 4473 | 8248 |
| 512 | 5 | 3 | multiclass | 15 | None | 1042 | 20 | 148 | 150 | 146 | 101.2 | 7033 | 8506 |
| 512 | 10 | 3 | multiclass | 30 | None | 1528 | 20 | 154 | 154 | 150 | 195.4 | 9953 | 8594 |
| 512 | 25 | 3 | multiclass | 75 | None | 2998 | 20 | 187 | 187 | 177 | 401.7 | 16058 | 8906 |
| 512 | 50 | 3 | multiclass | 150 | None | 5448 | 20 | 309 | 311 | 289 | 485.5 | 17635 | 9662 |
| 2048 | 1 | 3 | multiclass | 3 | None | 2190 | 20 | 166 | 166 | 165 | 18.1 | 13189 | 8505 |
| 2048 | 5 | 3 | multiclass | 15 | None | 2578 | 20 | 176 | 177 | 174 | 85.1 | 14628 | 8513 |
| 2048 | 10 | 3 | multiclass | 30 | None | 3064 | 20 | 189 | 190 | 184 | 158.6 | 16203 | 8523 |
| 2048 | 25 | 3 | multiclass | 75 | None | 4534 | 20 | 252 | 252 | 241 | 298.2 | 18026 | 8940 |
| 2048 | 50 | 3 | multiclass | 150 | None | 6984 | 20 | 404 | 407 | 384 | 371.5 | 17297 | 9704 |
| 8192 | 1 | 3 | multiclass | 3 | None | 8333 | 20 | 506 | 509 | 504 | 5.9 | 16484 | 9583 |
| 8192 | 5 | 3 | multiclass | 15 | None | 8721 | 20 | 532 | 533 | 529 | 28.2 | 16388 | 9595 |
| 8192 | 10 | 3 | multiclass | 30 | None | 9207 | 20 | 560 | 560 | 555 | 53.6 | 16443 | 9609 |
| 8192 | 25 | 3 | multiclass | 75 | None | 10677 | 20 | 672 | 674 | 661 | 111.5 | 15880 | 9659 |
| 8192 | 50 | 3 | multiclass | 150 | None | 13127 | 20 | 907 | 908 | 887 | 165.4 | 14474 | 9911 |
| 16384 | 1 | 3 | multiclass | 3 | None | 16526 | 20 | 1290 | 1306 | 1289 | 2.3 | 12808 | 11128 |
| 16384 | 5 | 3 | multiclass | 15 | None | 16914 | 20 | 1340 | 1347 | 1337 | 11.2 | 12618 | 11146 |
| 16384 | 10 | 3 | multiclass | 30 | None | 17400 | 20 | 1385 | 1385 | 1379 | 21.7 | 12567 | 11168 |
| 16384 | 25 | 3 | multiclass | 75 | None | 18870 | 20 | 1580 | 1584 | 1568 | 47.5 | 11945 | 11242 |
| 16384 | 50 | 3 | multiclass | 150 | None | 21320 | 20 | 1941 | 1942 | 1920 | 77.3 | 10987 | 11372 |
| 32000 | 1 | 3 | multiclass | 3 | None | 32142 | 15 | 4033 | 4035 | 4032 | 0.7 | 7969 | 14534 |
| 32000 | 5 | 3 | multiclass | 15 | None | 32530 | 15 | 4122 | 4126 | 4118 | 3.6 | 7893 | 14668 |
| 32000 | 10 | 3 | multiclass | 30 | None | 33016 | 15 | 4200 | 4202 | 4195 | 7.1 | 7860 | 14497 |
| 32000 | 25 | 3 | multiclass | 75 | None | 34486 | 14 | 4574 | 4579 | 4562 | 16.4 | 7539 | 15380 |
| 32000 | 50 | 3 | multiclass | 150 | None | 36936 | 12 | 5206 | 5212 | 5185 | 28.8 | 7095 | 14817 |
| 2048 | 4 | 2 | multiclass | 8 | None | 2377 | 20 | 171 | 171 | 169 | 46.8 | 13914 | 8509 |
| 2048 | 4 | 8 | multiclass | 32 | None | 3001 | 20 | 187 | 188 | 182 | 171.0 | 16040 | 8619 |
| 2048 | 16 | 1 | binary | 16 | None | 2532 | 20 | 174 | 174 | 172 | 91.9 | 14546 | 8540 |
