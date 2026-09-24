# Blind judge review (round 2)

Author = the model in `provenance`; judge = GPT-6 Astra (reasoning low) via batch; Jev = `~typesafe/jev-latest` decisions API. A question is kept by build_hardcases.py only if author = judge.

### family

| family | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| e2_hard | 702 | 97.2 | 702 | 93.7 | 29 |
| e2_simple | 684 | 98.1 | 684 | 98.0 | 12 |
| e2_very_hard | 684 | 97.2 | 684 | 94.4 | 27 |
| **all** | 2070 | 97.5 | 2070 | 95.4 | 68 |

### author

| author | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| openrouter/anthropic/claude-opus-5.5 | 566 | 99.6 | 566 | 95.8 | 23 |
| openrouter/moonshotai/kimi-k3 | 678 | 96.8 | 678 | 96.8 | 14 |
| openrouter/z-ai/glm-5.3 | 826 | 96.6 | 826 | 93.9 | 31 |
| **all** | 2070 | 97.5 | 2070 | 95.4 | 68 |

### type

| type | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| binary | 1050 | 97.9 | 1050 | 95.8 | 32 |
| multiclass | 611 | 98.0 | 611 | 97.2 | 12 |
| multilabel | 409 | 95.6 | 409 | 91.4 | 24 |
| **all** | 2070 | 97.5 | 2070 | 95.4 | 68 |

### length bucket (tokens)

| length bucket (tokens) | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| 1024 | 225 | 95.6 | 225 | 96.4 | 6 |
| 128 | 231 | 97.4 | 231 | 95.7 | 7 |
| 2048 | 197 | 98.5 | 197 | 96.4 | 4 |
| 256 | 198 | 97.5 | 198 | 92.4 | 12 |
| 32 | 217 | 96.3 | 217 | 91.7 | 15 |
| 4096 | 200 | 98.0 | 200 | 98.5 | 1 |
| 512 | 194 | 97.9 | 194 | 95.4 | 6 |
| 64 | 217 | 99.1 | 217 | 96.8 | 5 |
| 8 | 208 | 97.6 | 208 | 94.7 | 8 |
| 8192 | 183 | 97.3 | 183 | 95.6 | 4 |
| **all** | 2070 | 97.5 | 2070 | 95.4 | 68 |

### hard case

| hard case | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| (none) | 588 | 97.8 | 588 | 98.0 | 10 |
| contradiction | 91 | 94.5 | 91 | 92.3 | 2 |
| distractor | 53 | 98.1 | 53 | 98.1 | 0 |
| double_negation | 89 | 97.8 | 89 | 97.8 | 1 |
| evidence_end | 1 | 100.0 | 1 | 100.0 | 0 |
| evidence_middle | 1 | 100.0 | 1 | 100.0 | 0 |
| exception | 58 | 94.8 | 58 | 87.9 | 5 |
| hypothetical | 78 | 98.7 | 78 | 97.4 | 2 |
| injection | 53 | 100.0 | 53 | 98.1 | 1 |
| lexical_overlap | 70 | 98.6 | 70 | 95.7 | 2 |
| long_state | 89 | 96.6 | 89 | 97.8 | 1 |
| missing_evidence | 74 | 100.0 | 74 | 100.0 | 0 |
| multi_positive | 110 | 98.2 | 110 | 98.2 | 2 |
| multi_turn | 43 | 90.7 | 43 | 83.7 | 5 |
| negation | 101 | 99.0 | 101 | 98.0 | 1 |
| nota | 64 | 100.0 | 64 | 96.9 | 2 |
| numeric_reasoning | 105 | 97.1 | 105 | 84.8 | 13 |
| paraphrase | 58 | 100.0 | 58 | 100.0 | 0 |
| role_reversal | 95 | 94.7 | 95 | 94.7 | 3 |
| sarcasm | 101 | 95.0 | 101 | 93.1 | 3 |
| temporal_reasoning | 104 | 99.0 | 104 | 85.6 | 14 |
| zero_positive | 44 | 95.5 | 44 | 93.2 | 1 |
| **all** | 2070 | 97.5 | 2070 | 95.4 | 68 |
