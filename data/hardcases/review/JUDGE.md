# Blind judge review (round 2)

Author = the model in `provenance`; judge = GPT-6 Astra (reasoning low) via batch; Jev = `~typesafe/jev-latest` decisions API. A question is kept by build_hardcases.py only if author = judge.

### family

| family | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| hard_contrastive | 240 | 97.9 | 240 | 97.1 | 6 |
| hard_injection_tone | 220 | 99.1 | 219 | 99.5 | 0 |
| hard_long_evidence | 210 | 100.0 | 210 | 98.1 | 4 |
| hard_multilabel | 226 | 93.8 | 226 | 95.1 | 5 |
| hard_numeric | 238 | 99.6 | 238 | 90.8 | 22 |
| hard_policy | 242 | 97.9 | 242 | 91.7 | 19 |
| hard_roles | 295 | 98.6 | 295 | 99.7 | 1 |
| hard_temporal | 220 | 99.5 | 220 | 82.7 | 38 |
| r2_hard | 2909 | 93.8 | 2909 | 91.2 | 141 |
| r2_simple | 2901 | 97.3 | 2901 | 96.7 | 43 |
| r2_very_hard | 2926 | 93.3 | 2926 | 90.2 | 153 |
| **all** | 10627 | 95.4 | 10626 | 93.0 | 432 |

### author

| author | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| claude-sonnet | 1891 | 98.3 | 1890 | 94.5 | 95 |
| openrouter/deepseek/deepseek-v4-flash | 1264 | 82.1 | 1264 | 81.9 | 68 |
| openrouter/google/gemini-3.8-flash | 2462 | 97.6 | 2462 | 95.2 | 89 |
| openrouter/openai/gpt-6-luna | 3988 | 96.0 | 3988 | 94.0 | 135 |
| openrouter/x-ai/grok-4.7 | 1022 | 98.9 | 1022 | 94.9 | 45 |
| **all** | 10627 | 95.4 | 10626 | 93.0 | 432 |

### type

| type | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| binary | 4652 | 96.2 | 4652 | 94.8 | 139 |
| multiclass | 3345 | 96.9 | 3344 | 95.7 | 79 |
| multilabel | 2630 | 92.2 | 2630 | 86.3 | 214 |
| **all** | 10627 | 95.4 | 10626 | 93.0 | 432 |

### length bucket (tokens)

| length bucket (tokens) | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| 1024 | 905 | 95.7 | 905 | 95.7 | 9 |
| 128 | 851 | 93.4 | 851 | 90.2 | 45 |
| 2048 | 900 | 96.3 | 900 | 94.6 | 29 |
| 256 | 910 | 95.8 | 910 | 95.5 | 25 |
| 32 | 770 | 93.4 | 770 | 87.8 | 58 |
| 4096 | 899 | 93.8 | 899 | 92.0 | 32 |
| 512 | 884 | 95.1 | 884 | 93.3 | 28 |
| 64 | 822 | 94.4 | 822 | 91.5 | 37 |
| 8 | 806 | 93.5 | 806 | 91.1 | 44 |
| 8192 | 841 | 95.7 | 841 | 93.9 | 22 |
| ? | 2039 | 98.3 | 2038 | 94.4 | 103 |
| **all** | 10627 | 95.4 | 10626 | 93.0 | 432 |

### hard case

| hard case | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| (none) | 2663 | 97.4 | 2663 | 96.7 | 39 |
| contradiction | 219 | 97.7 | 219 | 96.3 | 4 |
| distractor | 351 | 94.6 | 351 | 94.0 | 10 |
| double_negation | 271 | 93.0 | 271 | 93.7 | 8 |
| evidence_end | 4 | 100.0 | 4 | 100.0 | 0 |
| evidence_middle | 4 | 100.0 | 4 | 100.0 | 0 |
| exception | 386 | 90.9 | 386 | 92.7 | 8 |
| hypothetical | 363 | 94.8 | 363 | 93.9 | 11 |
| injection | 431 | 96.5 | 430 | 90.5 | 28 |
| lexical_overlap | 292 | 93.8 | 292 | 91.8 | 11 |
| long_state | 623 | 94.9 | 623 | 94.4 | 12 |
| missing_evidence | 205 | 96.6 | 205 | 94.1 | 5 |
| multi_positive | 346 | 93.4 | 346 | 89.6 | 28 |
| multi_turn | 198 | 94.9 | 198 | 92.4 | 10 |
| negation | 445 | 95.7 | 445 | 93.7 | 16 |
| nota | 160 | 94.4 | 160 | 90.6 | 9 |
| numeric_reasoning | 1032 | 95.9 | 1032 | 89.0 | 89 |
| paraphrase | 300 | 95.0 | 300 | 92.0 | 12 |
| role_reversal | 656 | 95.3 | 656 | 93.4 | 21 |
| sarcasm | 788 | 93.1 | 788 | 91.9 | 25 |
| temporal_reasoning | 700 | 94.7 | 700 | 85.6 | 81 |
| zero_positive | 190 | 96.8 | 190 | 96.3 | 5 |
| **all** | 10627 | 95.4 | 10626 | 93.0 | 432 |
