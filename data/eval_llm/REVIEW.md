# eval_llm: frozen test set

`data/eval_llm.jsonl` sha256 `6cfc3e1646ead76f85b59f7ccef0ca442a9a66c92c4025bfe3411ebe9ce8d811` — 946 questions / 317 states, every row split=test. **Frozen: never train, select prompts, fit thresholds or temperatures on it.** Authors: anthropic/claude-opus-5.5, moonshotai/kimi-k3, z-ai/glm-5.3. Judges (blind, both must agree with the author): astra, claude-sonnet-5. Jev is reported, never used to keep or drop. LLM-verified; human spot-check list in review/SPOTCHECK.md. Rows are expanded (one question per line) so ids are the raw `<source_id>-q<i>` and join `review/answers_*.jsonl`.

States dropped for 8-gram overlap ≥ 0.3 with training/eval files: 0 []

## Agreement (before the keep rule)

| family | judged | author = astra % | author = claude-sonnet-5 % | kept (unanimous) | dropped | unanswered |
|---|---|---|---|---|---|---|
| tllm_guardrail_hard | 76 | 93.4 | 96.1 | 60 | 7 | 0 |
| tllm_guardrail_simple | 72 | 97.2 | 100.0 | 67 | 2 | 0 |
| tllm_guardrail_very_hard | 61 | 90.2 | 95.1 | 43 | 8 | 0 |
| tllm_jailbreak_hard | 72 | 93.1 | 97.2 | 59 | 5 | 3 |
| tllm_jailbreak_simple | 80 | 97.5 | 96.2 | 70 | 3 | 0 |
| tllm_jailbreak_very_hard | 67 | 98.5 | 97.0 | 60 | 2 | 3 |
| tllm_judge_hard | 109 | 94.5 | 95.4 | 86 | 9 | 0 |
| tllm_judge_simple | 83 | 97.6 | 97.6 | 72 | 4 | 0 |
| tllm_judge_very_hard | 86 | 93.0 | 91.9 | 64 | 11 | 0 |
| tllm_score_hard | 79 | 94.9 | 98.7 | 62 | 5 | 0 |
| tllm_score_simple | 86 | 89.5 | 97.7 | 62 | 11 | 0 |
| tllm_score_very_hard | 100 | 94.0 | 95.0 | 76 | 9 | 0 |
| tllm_verify_hard | 64 | 92.2 | 95.3 | 50 | 6 | 0 |
| tllm_verify_simple | 83 | 94.0 | 94.0 | 60 | 8 | 0 |
| tllm_verify_very_hard | 95 | 96.8 | 83.2 | 55 | 17 | 0 |
| **all** | 1213 | 94.5 | 95.1 | 946 | 107 | 6 |

--strict: 160 more questions dropped because another question of their text was dropped.

## Composition of the kept set, with Jev accuracy on it

### tier (family)

| tier (family) | n | Jev acc % |
|---|---|---|
| tllm_guardrail_hard | 60 | 86.7 |
| tllm_guardrail_simple | 67 | 97.0 |
| tllm_guardrail_very_hard | 43 | 95.3 |
| tllm_jailbreak_hard | 59 | 98.3 |
| tllm_jailbreak_simple | 70 | 98.6 |
| tllm_jailbreak_very_hard | 60 | 85.0 |
| tllm_judge_hard | 86 | 95.3 |
| tllm_judge_simple | 72 | 97.2 |
| tllm_judge_very_hard | 64 | 90.6 |
| tllm_score_hard | 62 | 93.5 |
| tllm_score_simple | 62 | 98.4 |
| tllm_score_very_hard | 76 | 88.2 |
| tllm_verify_hard | 50 | 80.0 |
| tllm_verify_simple | 60 | 98.3 |
| tllm_verify_very_hard | 55 | 80.0 |

### author

| author | n | Jev acc % |
|---|---|---|
| anthropic/claude-opus-5.5 | 318 | 92.5 |
| moonshotai/kimi-k3 | 319 | 92.8 |
| z-ai/glm-5.3 | 309 | 92.2 |

### type

| type | n | Jev acc % |
|---|---|---|
| binary | 488 | 95.1 |
| multiclass | 276 | 95.3 |
| multilabel | 182 | 81.3 |

### length bucket (tokens)

| length bucket (tokens) | n | Jev acc % |
|---|---|---|
| 1024 | 102 | 97.1 |
| 128 | 92 | 91.3 |
| 2048 | 108 | 93.5 |
| 256 | 115 | 97.4 |
| 32 | 94 | 85.1 |
| 4096 | 78 | 93.6 |
| 512 | 115 | 93.0 |
| 64 | 94 | 88.3 |
| 8 | 104 | 89.4 |
| 8192 | 44 | 97.7 |

### hard case (all tags)

| hard case (all tags) | n | Jev acc % |
|---|---|---|
| (none) | 265 | 97.7 |
| answer_trace_mismatch | 45 | 86.7 |
| benign_lookalike | 88 | 86.4 |
| confident_wrong | 39 | 82.1 |
| contradiction | 22 | 95.5 |
| distractor | 117 | 89.7 |
| double_negation | 3 | 100.0 |
| evidence_end | 11 | 100.0 |
| evidence_middle | 20 | 85.0 |
| evidence_start | 2 | 50.0 |
| exception | 20 | 100.0 |
| fake_authority | 1 | 100.0 |
| flawed_step | 44 | 68.2 |
| format_near_miss | 46 | 87.0 |
| gradual_escalation | 1 | 100.0 |
| hypothetical | 7 | 100.0 |
| indirect_injection | 25 | 96.0 |
| injection | 22 | 100.0 |
| judge_injection | 112 | 91.1 |
| length_bias | 7 | 100.0 |
| lexical_overlap | 103 | 93.2 |
| long_state | 74 | 93.2 |
| missing_evidence | 35 | 94.3 |
| multi_positive | 124 | 81.5 |
| multi_turn | 44 | 88.6 |
| negation | 62 | 95.2 |
| nota | 55 | 90.9 |
| numeric_reasoning | 109 | 81.7 |
| obfuscation | 1 | 0.0 |
| over_refusal | 50 | 88.0 |
| paraphrase | 73 | 90.4 |
| partial_compliance | 31 | 77.4 |
| role_reversal | 6 | 66.7 |
| sarcasm | 8 | 100.0 |
| speaker_confusion | 58 | 84.5 |
| subtle_violation | 16 | 100.0 |
| sycophancy | 13 | 100.0 |
| temporal_reasoning | 20 | 100.0 |
| tool_misuse | 6 | 100.0 |
| unsupported_claim | 96 | 89.6 |
| zero_positive | 55 | 87.3 |
| zero_positive_partial | 1 | 100.0 |

Multilabel positives: {0: 25, 1: 23, 2: 41, 3: 56, 4: 30, 5: 7}. Multiclass questions offering a none candidate: 162, none correct in 38 (23.5%).

