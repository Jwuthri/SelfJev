# Blind judge review (round 2)

Author = the model in `provenance`; judge = GPT-6 Astra (reasoning low) via batch; Jev = `~typesafe/jev-latest` decisions API. A question is kept by build_hardcases.py only if author = judge.

### family

| family | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| r3_hard | 215 | 89.3 | 0 | — | 0 |
| r3_simple | 215 | 93.5 | 0 | — | 0 |
| r3_very_hard | 213 | 96.2 | 0 | — | 0 |
| **all** | 643 | 93.0 | 0 | — | 0 |

### author

| author | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| openrouter/openai/gpt-6-luna | 643 | 93.0 | 0 | — | 0 |
| **all** | 643 | 93.0 | 0 | — | 0 |

### type

| type | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| binary | 316 | 94.9 | 0 | — | 0 |
| multiclass | 197 | 94.9 | 0 | — | 0 |
| multilabel | 130 | 85.4 | 0 | — | 0 |
| **all** | 643 | 93.0 | 0 | — | 0 |

### length bucket (tokens)

| length bucket (tokens) | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| 1024 | 80 | 95.0 | 0 | — | 0 |
| 128 | 60 | 90.0 | 0 | — | 0 |
| 2048 | 63 | 96.8 | 0 | — | 0 |
| 256 | 63 | 88.9 | 0 | — | 0 |
| 32 | 52 | 88.5 | 0 | — | 0 |
| 4096 | 75 | 96.0 | 0 | — | 0 |
| 512 | 68 | 92.6 | 0 | — | 0 |
| 64 | 57 | 93.0 | 0 | — | 0 |
| 8 | 60 | 90.0 | 0 | — | 0 |
| 8192 | 65 | 96.9 | 0 | — | 0 |
| **all** | 643 | 93.0 | 0 | — | 0 |

### hard case

| hard case | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| double_negation | 193 | 97.9 | 0 | — | 0 |
| numeric_reasoning | 211 | 91.0 | 0 | — | 0 |
| temporal_reasoning | 239 | 90.8 | 0 | — | 0 |
| **all** | 643 | 93.0 | 0 | — | 0 |
