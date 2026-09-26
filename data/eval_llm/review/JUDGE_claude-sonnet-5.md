# Blind judge review (round 2)

Author = the model in `provenance`; judge = GPT-6 Astra (reasoning low) via batch; Jev = `~typesafe/jev-latest` decisions API. A question is kept by build_hardcases.py only if author = judge.

### family

| family | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| tllm_guardrail_hard | 76 | 96.1 | 0 | — | 0 |
| tllm_guardrail_simple | 72 | 100.0 | 0 | — | 0 |
| tllm_guardrail_very_hard | 61 | 95.1 | 0 | — | 0 |
| tllm_jailbreak_hard | 72 | 97.2 | 0 | — | 0 |
| tllm_jailbreak_simple | 80 | 96.2 | 0 | — | 0 |
| tllm_jailbreak_very_hard | 67 | 97.0 | 0 | — | 0 |
| tllm_judge_hard | 109 | 95.4 | 0 | — | 0 |
| tllm_judge_simple | 83 | 97.6 | 0 | — | 0 |
| tllm_judge_very_hard | 86 | 91.9 | 0 | — | 0 |
| tllm_score_hard | 79 | 98.7 | 0 | — | 0 |
| tllm_score_simple | 86 | 97.7 | 0 | — | 0 |
| tllm_score_very_hard | 100 | 95.0 | 0 | — | 0 |
| tllm_verify_hard | 64 | 95.3 | 0 | — | 0 |
| tllm_verify_simple | 83 | 94.0 | 0 | — | 0 |
| tllm_verify_very_hard | 95 | 83.2 | 0 | — | 0 |
| **all** | 1213 | 95.1 | 0 | — | 0 |

### author

| author | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| openrouter/anthropic/claude-opus-5.5 | 377 | 95.8 | 0 | — | 0 |
| openrouter/moonshotai/kimi-k3 | 415 | 96.1 | 0 | — | 0 |
| openrouter/z-ai/glm-5.3 | 421 | 93.6 | 0 | — | 0 |
| **all** | 1213 | 95.1 | 0 | — | 0 |

### type

| type | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| binary | 612 | 97.4 | 0 | — | 0 |
| multiclass | 351 | 96.0 | 0 | — | 0 |
| multilabel | 250 | 88.4 | 0 | — | 0 |
| **all** | 1213 | 95.1 | 0 | — | 0 |

### length bucket (tokens)

| length bucket (tokens) | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| 1024 | 126 | 94.4 | 0 | — | 0 |
| 128 | 115 | 93.9 | 0 | — | 0 |
| 2048 | 137 | 97.1 | 0 | — | 0 |
| 256 | 137 | 99.3 | 0 | — | 0 |
| 32 | 112 | 97.3 | 0 | — | 0 |
| 4096 | 139 | 90.6 | 0 | — | 0 |
| 512 | 141 | 92.2 | 0 | — | 0 |
| 64 | 111 | 97.3 | 0 | — | 0 |
| 8 | 121 | 97.5 | 0 | — | 0 |
| 8192 | 74 | 90.5 | 0 | — | 0 |
| **all** | 1213 | 95.1 | 0 | — | 0 |

### hard case

| hard case | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| (none) | 319 | 96.9 | 0 | — | 0 |
| answer_trace_mismatch | 48 | 91.7 | 0 | — | 0 |
| benign_lookalike | 28 | 96.4 | 0 | — | 0 |
| confident_wrong | 27 | 96.3 | 0 | — | 0 |
| contradiction | 2 | 100.0 | 0 | — | 0 |
| distractor | 20 | 85.0 | 0 | — | 0 |
| double_negation | 1 | 100.0 | 0 | — | 0 |
| flawed_step | 52 | 78.8 | 0 | — | 0 |
| format_near_miss | 32 | 93.8 | 0 | — | 0 |
| indirect_injection | 4 | 100.0 | 0 | — | 0 |
| injection | 3 | 100.0 | 0 | — | 0 |
| judge_injection | 82 | 95.1 | 0 | — | 0 |
| length_bias | 10 | 70.0 | 0 | — | 0 |
| lexical_overlap | 16 | 100.0 | 0 | — | 0 |
| long_state | 71 | 97.2 | 0 | — | 0 |
| missing_evidence | 38 | 92.1 | 0 | — | 0 |
| multi_positive | 71 | 93.0 | 0 | — | 0 |
| multi_turn | 3 | 100.0 | 0 | — | 0 |
| negation | 42 | 95.2 | 0 | — | 0 |
| nota | 24 | 100.0 | 0 | — | 0 |
| numeric_reasoning | 30 | 96.7 | 0 | — | 0 |
| over_refusal | 34 | 100.0 | 0 | — | 0 |
| paraphrase | 23 | 95.7 | 0 | — | 0 |
| partial_compliance | 17 | 94.1 | 0 | — | 0 |
| role_reversal | 3 | 100.0 | 0 | — | 0 |
| speaker_confusion | 43 | 97.7 | 0 | — | 0 |
| subtle_violation | 20 | 95.0 | 0 | — | 0 |
| sycophancy | 9 | 88.9 | 0 | — | 0 |
| temporal_reasoning | 3 | 100.0 | 0 | — | 0 |
| tool_misuse | 8 | 87.5 | 0 | — | 0 |
| unsupported_claim | 99 | 100.0 | 0 | — | 0 |
| zero_positive | 31 | 96.8 | 0 | — | 0 |
| **all** | 1213 | 95.1 | 0 | — | 0 |
