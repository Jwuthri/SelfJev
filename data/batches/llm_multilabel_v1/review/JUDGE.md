# Blind judge review (round 2)

Author = the model in `provenance`; judge = GPT-6 Astra (reasoning low) via batch; Jev = `~typesafe/jev-latest` decisions API. A question is kept by build_hardcases.py only if author = judge.

### family

| family | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| llmml_guardrail_hard | 590 | 90.7 | 0 | — | 0 |
| llmml_guardrail_simple | 644 | 94.7 | 0 | — | 0 |
| llmml_guardrail_very_hard | 568 | 88.2 | 0 | — | 0 |
| llmml_jailbreak_hard | 542 | 91.7 | 0 | — | 0 |
| llmml_jailbreak_simple | 636 | 92.3 | 0 | — | 0 |
| llmml_jailbreak_very_hard | 541 | 88.9 | 0 | — | 0 |
| llmml_judge_hard | 636 | 88.1 | 0 | — | 0 |
| llmml_judge_simple | 669 | 92.8 | 0 | — | 0 |
| llmml_judge_very_hard | 665 | 87.1 | 0 | — | 0 |
| llmml_score_hard | 666 | 89.0 | 0 | — | 0 |
| llmml_score_simple | 661 | 91.4 | 0 | — | 0 |
| llmml_score_very_hard | 631 | 84.6 | 0 | — | 0 |
| llmml_verify_hard | 612 | 86.3 | 0 | — | 0 |
| llmml_verify_simple | 618 | 91.6 | 0 | — | 0 |
| llmml_verify_very_hard | 607 | 87.6 | 0 | — | 0 |
| **all** | 9286 | 89.7 | 0 | — | 0 |

### author

| author | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| google-batch/gemini-3.8-flash | 4652 | 92.0 | 0 | — | 0 |
| openrouter/google/gemini-3.8-flash | 1726 | 91.9 | 0 | — | 0 |
| openrouter/openai/gpt-6-luna | 2460 | 83.5 | 0 | — | 0 |
| openrouter/x-ai/grok-4.7 | 448 | 91.1 | 0 | — | 0 |
| **all** | 9286 | 89.7 | 0 | — | 0 |

### type

| type | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| multilabel | 9286 | 89.7 | 0 | — | 0 |
| **all** | 9286 | 89.7 | 0 | — | 0 |

### length bucket (tokens)

| length bucket (tokens) | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| 1024 | 839 | 90.2 | 0 | — | 0 |
| 128 | 903 | 88.6 | 0 | — | 0 |
| 2048 | 838 | 94.2 | 0 | — | 0 |
| 256 | 925 | 90.4 | 0 | — | 0 |
| 32 | 949 | 89.7 | 0 | — | 0 |
| 4096 | 962 | 92.0 | 0 | — | 0 |
| 512 | 874 | 90.4 | 0 | — | 0 |
| 64 | 928 | 89.3 | 0 | — | 0 |
| 8 | 948 | 85.0 | 0 | — | 0 |
| 8192 | 1120 | 87.9 | 0 | — | 0 |
| **all** | 9286 | 89.7 | 0 | — | 0 |

### hard case

| hard case | judged | author = judge % | jev | author = jev % | judge right, jev wrong |
|---|---|---|---|---|---|
| (none) | 2264 | 92.1 | 0 | — | 0 |
| answer_trace_mismatch | 103 | 86.4 | 0 | — | 0 |
| benign_lookalike | 195 | 91.3 | 0 | — | 0 |
| confident_wrong | 405 | 86.9 | 0 | — | 0 |
| contradiction | 13 | 84.6 | 0 | — | 0 |
| crescendo | 34 | 91.2 | 0 | — | 0 |
| distractor | 399 | 87.5 | 0 | — | 0 |
| evidence_middle | 2 | 100.0 | 0 | — | 0 |
| exception | 71 | 83.1 | 0 | — | 0 |
| flawed_step | 232 | 81.5 | 0 | — | 0 |
| format_near_miss | 266 | 85.3 | 0 | — | 0 |
| hypothetical | 17 | 94.1 | 0 | — | 0 |
| implicit_positive | 18 | 88.9 | 0 | — | 0 |
| indirect_injection | 197 | 92.9 | 0 | — | 0 |
| judge_injection | 332 | 93.1 | 0 | — | 0 |
| length_bias | 231 | 85.7 | 0 | — | 0 |
| lexical_overlap | 239 | 88.7 | 0 | — | 0 |
| long_state | 385 | 88.8 | 0 | — | 0 |
| missing_evidence | 283 | 87.6 | 0 | — | 0 |
| multi_positive | 495 | 90.9 | 0 | — | 0 |
| multi_turn | 205 | 86.3 | 0 | — | 0 |
| negation | 279 | 96.1 | 0 | — | 0 |
| nota | 174 | 93.7 | 0 | — | 0 |
| numeric_reasoning | 323 | 90.4 | 0 | — | 0 |
| obfuscation | 215 | 84.7 | 0 | — | 0 |
| over_refusal | 70 | 91.4 | 0 | — | 0 |
| paraphrase | 195 | 85.6 | 0 | — | 0 |
| partial_compliance | 110 | 90.9 | 0 | — | 0 |
| role_reversal | 323 | 87.6 | 0 | — | 0 |
| simple | 14 | 85.7 | 0 | — | 0 |
| speaker_confusion | 214 | 91.1 | 0 | — | 0 |
| subtle_violation | 72 | 94.4 | 0 | — | 0 |
| sycophancy | 122 | 86.9 | 0 | — | 0 |
| temporal_reasoning | 141 | 87.2 | 0 | — | 0 |
| tool_misuse | 91 | 86.8 | 0 | — | 0 |
| unsupported_claim | 194 | 88.7 | 0 | — | 0 |
| zero_positive | 363 | 90.9 | 0 | — | 0 |
| **all** | 9286 | 89.7 | 0 | — | 0 |
