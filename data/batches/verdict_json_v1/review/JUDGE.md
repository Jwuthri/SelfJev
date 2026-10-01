# Blind judge review (round 2)

Author = the model in `provenance`; judge = GPT-6 Astra (reasoning low) via batch; Jev = `~typesafe/jev-latest` decisions API. A question is kept by build_hardcases.py only if author = judge.

### family

| family | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| r3_hard | 1483 | 96.4 | 0 | — | 0 |
| r3_simple | 1492 | 97.0 | 0 | — | 0 |
| r3_very_hard | 1459 | 94.4 | 0 | — | 0 |
| **all** | 4434 | 95.9 | 0 | — | 0 |

### author

| author | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| openrouter/openai/gpt-6-luna | 4434 | 95.9 | 0 | — | 0 |
| **all** | 4434 | 95.9 | 0 | — | 0 |

### type

| type | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| binary | 1999 | 96.4 | 0 | — | 0 |
| multiclass | 1444 | 96.6 | 0 | — | 0 |
| multilabel | 991 | 94.0 | 0 | — | 0 |
| **all** | 4434 | 95.9 | 0 | — | 0 |

### length bucket (tokens)

| length bucket (tokens) | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| 1024 | 445 | 96.2 | 0 | — | 0 |
| 128 | 499 | 97.6 | 0 | — | 0 |
| 2048 | 398 | 98.5 | 0 | — | 0 |
| 256 | 448 | 96.7 | 0 | — | 0 |
| 32 | 419 | 92.6 | 0 | — | 0 |
| 4096 | 444 | 96.2 | 0 | — | 0 |
| 512 | 488 | 98.2 | 0 | — | 0 |
| 64 | 435 | 95.2 | 0 | — | 0 |
| 8 | 414 | 90.6 | 0 | — | 0 |
| 8192 | 444 | 97.1 | 0 | — | 0 |
| **all** | 4434 | 95.9 | 0 | — | 0 |

### hard case

| hard case | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| json_record | 2342 | 96.0 | 0 | — | 0 |
| planted_verdict | 2092 | 95.8 | 0 | — | 0 |
| **all** | 4434 | 95.9 | 0 | — | 0 |
