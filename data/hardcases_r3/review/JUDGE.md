# Blind judge review (round 2)

Author = the model in `provenance`; judge = GPT-6 Astra (reasoning low) via batch; Jev = `~typesafe/jev-latest` decisions API. A question is kept by build_hardcases.py only if author = judge.

### family

| family | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| r3_hard | 13325 | 96.5 | 0 | — | 0 |
| r3_simple | 13284 | 98.8 | 0 | — | 0 |
| r3_very_hard | 13224 | 95.6 | 0 | — | 0 |
| **all** | 39833 | 97.0 | 0 | — | 0 |

### author

| author | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| openrouter/google/gemini-3.8-flash | 10023 | 97.5 | 0 | — | 0 |
| openrouter/openai/gpt-6-luna | 24246 | 96.2 | 0 | — | 0 |
| openrouter/x-ai/grok-4.7 | 5564 | 99.2 | 0 | — | 0 |
| **all** | 39833 | 97.0 | 0 | — | 0 |

### type

| type | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| binary | 17179 | 97.6 | 0 | — | 0 |
| multiclass | 12699 | 97.7 | 0 | — | 0 |
| multilabel | 9955 | 95.0 | 0 | — | 0 |
| **all** | 39833 | 97.0 | 0 | — | 0 |

### length bucket (tokens)

| length bucket (tokens) | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| 1024 | 4030 | 97.9 | 0 | — | 0 |
| 128 | 3898 | 96.2 | 0 | — | 0 |
| 2048 | 3880 | 98.2 | 0 | — | 0 |
| 256 | 4025 | 96.8 | 0 | — | 0 |
| 32 | 3760 | 96.2 | 0 | — | 0 |
| 4096 | 4266 | 97.6 | 0 | — | 0 |
| 512 | 4126 | 97.3 | 0 | — | 0 |
| 64 | 3737 | 95.9 | 0 | — | 0 |
| 8 | 3718 | 95.4 | 0 | — | 0 |
| 8192 | 4393 | 97.9 | 0 | — | 0 |
| **all** | 39833 | 97.0 | 0 | — | 0 |

### hard case

| hard case | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| (none) | 11593 | 98.8 | 0 | — | 0 |
| contradiction | 829 | 97.3 | 0 | — | 0 |
| distractor | 1347 | 96.4 | 0 | — | 0 |
| double_negation | 760 | 95.3 | 0 | — | 0 |
| evidence_middle | 10 | 100.0 | 0 | — | 0 |
| exception | 821 | 93.4 | 0 | — | 0 |
| hypothetical | 622 | 98.2 | 0 | — | 0 |
| injection | 1743 | 98.0 | 0 | — | 0 |
| lexical_overlap | 1780 | 97.9 | 0 | — | 0 |
| long_state | 2413 | 97.4 | 0 | — | 0 |
| missing_evidence | 691 | 98.7 | 0 | — | 0 |
| multi_positive | 1516 | 96.9 | 0 | — | 0 |
| multi_turn | 797 | 97.4 | 0 | — | 0 |
| negation | 1650 | 97.6 | 0 | — | 0 |
| nota | 601 | 93.7 | 0 | — | 0 |
| numeric_reasoning | 3159 | 93.8 | 0 | — | 0 |
| paraphrase | 1451 | 97.0 | 0 | — | 0 |
| role_reversal | 3037 | 95.7 | 0 | — | 0 |
| sarcasm | 2314 | 97.6 | 0 | — | 0 |
| temporal_reasoning | 2015 | 91.9 | 0 | — | 0 |
| very_hard | 6 | 100.0 | 0 | — | 0 |
| zero_positive | 678 | 97.1 | 0 | — | 0 |
| **all** | 39833 | 97.0 | 0 | — | 0 |
