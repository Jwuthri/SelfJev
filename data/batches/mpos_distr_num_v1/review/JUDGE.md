# Blind judge review (round 2)

Author = the model in `provenance`; judge = GPT-6 Astra (reasoning low) via batch; Jev = `~typesafe/jev-latest` decisions API. A question is kept by build_hardcases.py only if author = judge.

### family

| family | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| r3_hard | 1357 | 94.7 | 0 | — | 0 |
| r3_simple | 1340 | 97.8 | 0 | — | 0 |
| r3_very_hard | 1344 | 94.3 | 0 | — | 0 |
| **all** | 4041 | 95.6 | 0 | — | 0 |

### author

| author | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| openrouter/openai/gpt-6-luna | 4041 | 95.6 | 0 | — | 0 |
| **all** | 4041 | 95.6 | 0 | — | 0 |

### type

| type | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| binary | 1431 | 96.4 | 0 | — | 0 |
| multiclass | 965 | 96.8 | 0 | — | 0 |
| multilabel | 1645 | 94.2 | 0 | — | 0 |
| **all** | 4041 | 95.6 | 0 | — | 0 |

### length bucket (tokens)

| length bucket (tokens) | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| 1024 | 375 | 95.7 | 0 | — | 0 |
| 128 | 430 | 93.3 | 0 | — | 0 |
| 2048 | 385 | 97.9 | 0 | — | 0 |
| 256 | 440 | 93.9 | 0 | — | 0 |
| 32 | 383 | 95.6 | 0 | — | 0 |
| 4096 | 380 | 97.4 | 0 | — | 0 |
| 512 | 419 | 97.9 | 0 | — | 0 |
| 64 | 407 | 93.4 | 0 | — | 0 |
| 8 | 387 | 94.3 | 0 | — | 0 |
| 8192 | 435 | 96.8 | 0 | — | 0 |
| **all** | 4041 | 95.6 | 0 | — | 0 |

### hard case

| hard case | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| distractor | 1090 | 97.4 | 0 | — | 0 |
| multi_positive | 1301 | 95.4 | 0 | — | 0 |
| numeric_reasoning | 1648 | 94.5 | 0 | — | 0 |
| role_reversal | 2 | 100.0 | 0 | — | 0 |
| **all** | 4041 | 95.6 | 0 | — | 0 |
