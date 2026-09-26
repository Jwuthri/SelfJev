# Blind judge review (round 2)

Author = the model in `provenance`; judge = GPT-6 Astra (reasoning low) via batch; Jev = `~typesafe/jev-latest` decisions API. A question is kept by build_hardcases.py only if author = judge.

### family

| family | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| tllm_guardrail_hard | 76 | 93.4 | 76 | 86.8 | 8 |
| tllm_guardrail_simple | 72 | 97.2 | 72 | 97.2 | 2 |
| tllm_guardrail_very_hard | 61 | 90.2 | 61 | 93.4 | 3 |
| tllm_jailbreak_hard | 75 | 93.3 | 75 | 94.7 | 1 |
| tllm_jailbreak_simple | 80 | 97.5 | 80 | 97.5 | 1 |
| tllm_jailbreak_very_hard | 70 | 98.6 | 70 | 85.7 | 9 |
| tllm_judge_hard | 109 | 94.5 | 109 | 92.7 | 5 |
| tllm_judge_simple | 83 | 97.6 | 83 | 96.4 | 3 |
| tllm_judge_very_hard | 86 | 93.0 | 86 | 89.5 | 7 |
| tllm_score_hard | 79 | 94.9 | 79 | 94.9 | 4 |
| tllm_score_simple | 86 | 89.5 | 86 | 95.3 | 2 |
| tllm_score_very_hard | 100 | 94.0 | 100 | 85.0 | 12 |
| tllm_verify_hard | 64 | 92.2 | 64 | 76.6 | 12 |
| tllm_verify_simple | 83 | 94.0 | 83 | 95.2 | 2 |
| tllm_verify_very_hard | 95 | 96.8 | 95 | 76.8 | 21 |
| **all** | 1219 | 94.5 | 1219 | 90.5 | 92 |

### author

| author | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| openrouter/anthropic/claude-opus-5.5 | 377 | 98.1 | 377 | 91.2 | 31 |
| openrouter/moonshotai/kimi-k3 | 418 | 92.1 | 418 | 91.9 | 27 |
| openrouter/z-ai/glm-5.3 | 424 | 93.6 | 424 | 88.4 | 34 |
| **all** | 1219 | 94.5 | 1219 | 90.5 | 92 |

### type

| type | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| binary | 614 | 97.1 | 614 | 94.3 | 30 |
| multiclass | 353 | 94.3 | 353 | 93.8 | 17 |
| multilabel | 252 | 88.5 | 252 | 76.6 | 45 |
| **all** | 1219 | 94.5 | 1219 | 90.5 | 92 |

### length bucket (tokens)

| length bucket (tokens) | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| 1024 | 126 | 94.4 | 126 | 92.1 | 7 |
| 128 | 115 | 97.4 | 115 | 91.3 | 10 |
| 2048 | 137 | 94.2 | 137 | 92.0 | 8 |
| 256 | 137 | 94.9 | 137 | 95.6 | 4 |
| 32 | 112 | 93.8 | 112 | 83.0 | 15 |
| 4096 | 139 | 87.8 | 139 | 89.9 | 7 |
| 512 | 144 | 96.5 | 144 | 88.9 | 14 |
| 64 | 114 | 95.6 | 114 | 88.6 | 13 |
| 8 | 121 | 96.7 | 121 | 89.3 | 12 |
| 8192 | 74 | 94.6 | 74 | 94.6 | 2 |
| **all** | 1219 | 94.5 | 1219 | 90.5 | 92 |

### hard case

| hard case | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| (none) | 319 | 95.9 | 319 | 96.6 | 9 |
| answer_trace_mismatch | 48 | 93.8 | 48 | 85.4 | 6 |
| benign_lookalike | 28 | 100.0 | 28 | 78.6 | 6 |
| confident_wrong | 27 | 96.3 | 27 | 81.5 | 4 |
| contradiction | 2 | 100.0 | 2 | 100.0 | 0 |
| distractor | 20 | 85.0 | 20 | 70.0 | 3 |
| double_negation | 1 | 100.0 | 1 | 100.0 | 0 |
| flawed_step | 52 | 92.3 | 52 | 57.7 | 19 |
| format_near_miss | 32 | 96.9 | 32 | 81.2 | 5 |
| indirect_injection | 4 | 100.0 | 4 | 100.0 | 0 |
| injection | 3 | 100.0 | 3 | 100.0 | 0 |
| judge_injection | 85 | 94.1 | 85 | 91.8 | 6 |
| length_bias | 10 | 100.0 | 10 | 90.0 | 1 |
| lexical_overlap | 16 | 100.0 | 16 | 100.0 | 0 |
| long_state | 74 | 90.5 | 74 | 93.2 | 2 |
| missing_evidence | 38 | 97.4 | 38 | 97.4 | 1 |
| multi_positive | 71 | 88.7 | 71 | 91.5 | 3 |
| multi_turn | 3 | 100.0 | 3 | 66.7 | 1 |
| negation | 42 | 100.0 | 42 | 92.9 | 3 |
| nota | 24 | 91.7 | 24 | 95.8 | 0 |
| numeric_reasoning | 30 | 90.0 | 30 | 100.0 | 0 |
| over_refusal | 34 | 97.1 | 34 | 85.3 | 5 |
| paraphrase | 23 | 87.0 | 23 | 91.3 | 0 |
| partial_compliance | 17 | 100.0 | 17 | 94.1 | 1 |
| role_reversal | 3 | 66.7 | 3 | 100.0 | 0 |
| speaker_confusion | 43 | 100.0 | 43 | 81.4 | 8 |
| subtle_violation | 20 | 80.0 | 20 | 95.0 | 0 |
| sycophancy | 9 | 88.9 | 9 | 100.0 | 0 |
| temporal_reasoning | 3 | 100.0 | 3 | 100.0 | 0 |
| tool_misuse | 8 | 100.0 | 8 | 100.0 | 0 |
| unsupported_claim | 99 | 97.0 | 99 | 92.9 | 7 |
| zero_positive | 31 | 90.3 | 31 | 87.1 | 2 |
| **all** | 1219 | 94.5 | 1219 | 90.5 | 92 |
