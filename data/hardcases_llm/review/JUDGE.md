# Blind judge review (round 2)

Author = the model in `provenance`; judge = GPT-6 Astra (reasoning low) via batch; Jev = `~typesafe/jev-latest` decisions API. A question is kept by build_hardcases.py only if author = judge.

### family

| family | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| llm_guardrail_hard | 761 | 93.0 | 0 | — | 0 |
| llm_guardrail_simple | 748 | 93.0 | 0 | — | 0 |
| llm_guardrail_very_hard | 751 | 93.6 | 0 | — | 0 |
| llm_jailbreak_hard | 763 | 92.4 | 0 | — | 0 |
| llm_jailbreak_simple | 756 | 93.7 | 0 | — | 0 |
| llm_jailbreak_very_hard | 732 | 91.7 | 0 | — | 0 |
| llm_judge_hard | 751 | 92.3 | 0 | — | 0 |
| llm_judge_simple | 746 | 92.9 | 0 | — | 0 |
| llm_judge_very_hard | 753 | 86.9 | 0 | — | 0 |
| llm_score_hard | 736 | 91.4 | 0 | — | 0 |
| llm_score_simple | 740 | 94.3 | 0 | — | 0 |
| llm_score_very_hard | 775 | 88.0 | 0 | — | 0 |
| llm_verify_hard | 740 | 94.2 | 0 | — | 0 |
| llm_verify_simple | 754 | 95.6 | 0 | — | 0 |
| llm_verify_very_hard | 736 | 91.4 | 0 | — | 0 |
| **all** | 11242 | 92.3 | 0 | — | 0 |

### author

| author | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| openrouter/deepseek/deepseek-v4-flash | 1557 | 73.7 | 0 | — | 0 |
| openrouter/google/gemini-3.8-flash | 3032 | 96.9 | 0 | — | 0 |
| openrouter/openai/gpt-6-luna | 4562 | 93.1 | 0 | — | 0 |
| openrouter/x-ai/grok-4.7 | 2091 | 97.7 | 0 | — | 0 |
| **all** | 11242 | 92.3 | 0 | — | 0 |

### type

| type | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| binary | 4893 | 94.6 | 0 | — | 0 |
| multiclass | 3526 | 94.1 | 0 | — | 0 |
| multilabel | 2823 | 86.0 | 0 | — | 0 |
| **all** | 11242 | 92.3 | 0 | — | 0 |

### length bucket (tokens)

| length bucket (tokens) | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| 1024 | 1123 | 91.6 | 0 | — | 0 |
| 128 | 1116 | 92.7 | 0 | — | 0 |
| 2048 | 1101 | 92.1 | 0 | — | 0 |
| 256 | 1179 | 93.6 | 0 | — | 0 |
| 32 | 1093 | 94.5 | 0 | — | 0 |
| 4096 | 1172 | 91.1 | 0 | — | 0 |
| 512 | 1119 | 92.7 | 0 | — | 0 |
| 64 | 1084 | 92.5 | 0 | — | 0 |
| 8 | 1088 | 91.3 | 0 | — | 0 |
| 8192 | 1167 | 90.8 | 0 | — | 0 |
| **all** | 11242 | 92.3 | 0 | — | 0 |

### hard case

| hard case | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| (none) | 3404 | 93.9 | 0 | — | 0 |
| answer_trace_mismatch | 146 | 91.1 | 0 | — | 0 |
| benign_lookalike | 393 | 93.6 | 0 | — | 0 |
| confident_wrong | 419 | 90.2 | 0 | — | 0 |
| contradiction | 7 | 100.0 | 0 | — | 0 |
| crescendo | 78 | 94.9 | 0 | — | 0 |
| distractor | 192 | 93.2 | 0 | — | 0 |
| double_negation | 1 | 100.0 | 0 | — | 0 |
| evidence_start | 2 | 50.0 | 0 | — | 0 |
| exception | 172 | 94.8 | 0 | — | 0 |
| flawed_step | 273 | 91.2 | 0 | — | 0 |
| format_near_miss | 290 | 85.2 | 0 | — | 0 |
| indirect_injection | 374 | 93.9 | 0 | — | 0 |
| injection | 27 | 66.7 | 0 | — | 0 |
| jailbreak | 7 | 71.4 | 0 | — | 0 |
| judge_injection | 440 | 94.8 | 0 | — | 0 |
| length_bias | 239 | 87.0 | 0 | — | 0 |
| lexical_overlap | 250 | 94.4 | 0 | — | 0 |
| long_state | 625 | 90.7 | 0 | — | 0 |
| missing_evidence | 224 | 92.9 | 0 | — | 0 |
| multi_positive | 498 | 88.6 | 0 | — | 0 |
| multi_turn | 294 | 90.8 | 0 | — | 0 |
| negation | 216 | 92.6 | 0 | — | 0 |
| nota | 261 | 92.0 | 0 | — | 0 |
| numeric_reasoning | 288 | 89.6 | 0 | — | 0 |
| obfuscation | 215 | 93.5 | 0 | — | 0 |
| over_refusal | 207 | 90.3 | 0 | — | 0 |
| paraphrase | 331 | 95.8 | 0 | — | 0 |
| partial_compliance | 97 | 85.6 | 0 | — | 0 |
| role_reversal | 179 | 92.2 | 0 | — | 0 |
| sarcasm | 4 | 75.0 | 0 | — | 0 |
| speaker_confusion | 253 | 92.9 | 0 | — | 0 |
| subtle_violation | 172 | 94.8 | 0 | — | 0 |
| sycophancy | 39 | 84.6 | 0 | — | 0 |
| temporal_reasoning | 71 | 95.8 | 0 | — | 0 |
| tool_misuse | 90 | 93.3 | 0 | — | 0 |
| unsupported_claim | 207 | 94.2 | 0 | — | 0 |
| zero_positive | 257 | 89.5 | 0 | — | 0 |
| **all** | 11242 | 92.3 | 0 | — | 0 |
