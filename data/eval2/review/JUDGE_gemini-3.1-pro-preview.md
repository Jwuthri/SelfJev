# Blind judge review (round 2)

Author = the model in `provenance`; judge = GPT-6 Astra (reasoning low) via batch; Jev = `~typesafe/jev-latest` decisions API. A question is kept by build_hardcases.py only if author = judge.

### family

| family | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| e2_hard | 702 | 96.7 | 0 | — | 0 |
| e2_simple | 684 | 97.5 | 0 | — | 0 |
| e2_very_hard | 684 | 96.6 | 0 | — | 0 |
| **all** | 2070 | 97.0 | 0 | — | 0 |

### author

| author | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| openrouter/anthropic/claude-opus-5.5 | 566 | 99.1 | 0 | — | 0 |
| openrouter/moonshotai/kimi-k3 | 678 | 96.6 | 0 | — | 0 |
| openrouter/z-ai/glm-5.3 | 826 | 95.8 | 0 | — | 0 |
| **all** | 2070 | 97.0 | 0 | — | 0 |

### type

| type | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| binary | 1050 | 97.2 | 0 | — | 0 |
| multiclass | 611 | 98.0 | 0 | — | 0 |
| multilabel | 409 | 94.6 | 0 | — | 0 |
| **all** | 2070 | 97.0 | 0 | — | 0 |

### length bucket (tokens)

| length bucket (tokens) | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| 1024 | 225 | 96.4 | 0 | — | 0 |
| 128 | 231 | 97.4 | 0 | — | 0 |
| 2048 | 197 | 98.0 | 0 | — | 0 |
| 256 | 198 | 97.5 | 0 | — | 0 |
| 32 | 217 | 94.0 | 0 | — | 0 |
| 4096 | 200 | 99.5 | 0 | — | 0 |
| 512 | 194 | 97.9 | 0 | — | 0 |
| 64 | 217 | 98.6 | 0 | — | 0 |
| 8 | 208 | 92.8 | 0 | — | 0 |
| 8192 | 183 | 97.8 | 0 | — | 0 |
| **all** | 2070 | 97.0 | 0 | — | 0 |

### hard case

| hard case | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| (none) | 588 | 97.3 | 0 | — | 0 |
| contradiction | 91 | 94.5 | 0 | — | 0 |
| distractor | 53 | 98.1 | 0 | — | 0 |
| double_negation | 89 | 96.6 | 0 | — | 0 |
| evidence_end | 1 | 100.0 | 0 | — | 0 |
| evidence_middle | 1 | 100.0 | 0 | — | 0 |
| exception | 58 | 89.7 | 0 | — | 0 |
| hypothetical | 78 | 96.2 | 0 | — | 0 |
| injection | 53 | 94.3 | 0 | — | 0 |
| lexical_overlap | 70 | 97.1 | 0 | — | 0 |
| long_state | 89 | 98.9 | 0 | — | 0 |
| missing_evidence | 74 | 98.6 | 0 | — | 0 |
| multi_positive | 110 | 99.1 | 0 | — | 0 |
| multi_turn | 43 | 86.0 | 0 | — | 0 |
| negation | 101 | 99.0 | 0 | — | 0 |
| nota | 64 | 100.0 | 0 | — | 0 |
| numeric_reasoning | 105 | 96.2 | 0 | — | 0 |
| paraphrase | 58 | 100.0 | 0 | — | 0 |
| role_reversal | 95 | 96.8 | 0 | — | 0 |
| sarcasm | 101 | 96.0 | 0 | — | 0 |
| temporal_reasoning | 104 | 99.0 | 0 | — | 0 |
| zero_positive | 44 | 95.5 | 0 | — | 0 |
| **all** | 2070 | 97.0 | 0 | — | 0 |
