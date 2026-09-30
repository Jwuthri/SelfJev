# Blind judge review (round 2)

Author = the model in `provenance`; judge = GPT-6 Astra (reasoning low) via batch; Jev = `~typesafe/jev-latest` decisions API. A question is kept by build_hardcases.py only if author = judge.

### family

| family | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| cc_hard | 583 | 99.7 | 0 | — | 0 |
| cc_simple | 183 | 98.9 | 0 | — | 0 |
| cc_very_hard | 548 | 99.5 | 0 | — | 0 |
| **all** | 1314 | 99.5 | 0 | — | 0 |

### author

| author | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| claude-code/claude-opus-5-5 | 334 | 98.8 | 0 | — | 0 |
| claude-code/claude-sonnet-5-5 | 980 | 99.7 | 0 | — | 0 |
| **all** | 1314 | 99.5 | 0 | — | 0 |

### type

| type | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| binary | 580 | 99.5 | 0 | — | 0 |
| multiclass | 400 | 100.0 | 0 | — | 0 |
| multilabel | 334 | 98.8 | 0 | — | 0 |
| **all** | 1314 | 99.5 | 0 | — | 0 |

### length bucket (tokens)

| length bucket (tokens) | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| ? | 1314 | 99.5 | 0 | — | 0 |
| **all** | 1314 | 99.5 | 0 | — | 0 |

### hard case

| hard case | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| (none) | 150 | 99.3 | 0 | — | 0 |
| distractor | 57 | 100.0 | 0 | — | 0 |
| double_negation | 22 | 100.0 | 0 | — | 0 |
| evidence_end | 1 | 100.0 | 0 | — | 0 |
| exception | 91 | 98.9 | 0 | — | 0 |
| hypothetical | 33 | 100.0 | 0 | — | 0 |
| injection | 27 | 96.3 | 0 | — | 0 |
| lexical_overlap | 13 | 100.0 | 0 | — | 0 |
| long_state | 32 | 96.9 | 0 | — | 0 |
| missing_evidence | 12 | 100.0 | 0 | — | 0 |
| multi_positive | 12 | 91.7 | 0 | — | 0 |
| multi_turn | 125 | 100.0 | 0 | — | 0 |
| negation | 34 | 100.0 | 0 | — | 0 |
| nota | 18 | 100.0 | 0 | — | 0 |
| numeric_reasoning | 290 | 99.7 | 0 | — | 0 |
| paraphrase | 48 | 97.9 | 0 | — | 0 |
| role_reversal | 79 | 100.0 | 0 | — | 0 |
| sarcasm | 8 | 100.0 | 0 | — | 0 |
| temporal_reasoning | 234 | 100.0 | 0 | — | 0 |
| zero_positive | 28 | 100.0 | 0 | — | 0 |
| **all** | 1314 | 99.5 | 0 | — | 0 |
