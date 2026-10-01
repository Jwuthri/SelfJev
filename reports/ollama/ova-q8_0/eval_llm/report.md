# Evaluation report

- model `selfjev-q8_0` @ `307babdfc8` (one request per candidate on Ollama (prefix cache shares the state), readout logprob(yes) - logprob(no)), adapter/checkpoint `merged into the GGUF`, prompt `challenger-state-first-v1` (6c9d8459ac44)
- data data/ova/eval_llm.jsonl; splits ['test']; n=946; calibration `None`
- ollama / Q8_0; 2026-10-01T08:00:32+0000; wall 620.0s

## Overall

question accuracy 92.7%

![reliability](reliability.svg)

**binary**: n 488, positives 245, accuracy 0.936, precision 0.921, recall 0.955, f1 0.938, auroc 0.984, brier 0.048, log_loss 0.172, ece 0.039

**multiclass**: n 276, accuracy 0.953, macro_f1 0.925, log_loss 0.146, brier 0.077, ece_top_label 0.029

**multilabel**: n 182, labels 864, exact_match 0.863, micro_f1 0.961, macro_f1 0.925, label_auroc 0.991, brier 0.032, log_loss 0.124, ece 0.025

## By family

| family | n | question acc % | details |
|---|---|---|---|
| tllm_guardrail_hard | 60 | 90.0 | bin acc 93.8 F1 93.3 AUROC 1.000 ECE 0.132; mc acc 94.1 mF1 87.5 ECE 0.065; ml EM 72.7 µF1 92.3 ECE 0.068 |
| tllm_guardrail_simple | 67 | 98.5 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.026; mc acc 100.0 mF1 100.0 ECE 0.024; ml EM 92.9 µF1 98.5 ECE 0.047 |
| tllm_guardrail_very_hard | 43 | 97.7 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.093; mc acc 92.9 mF1 83.3 ECE 0.064; ml EM 100.0 µF1 100.0 ECE 0.050 |
| tllm_jailbreak_hard | 59 | 100.0 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.060; mc acc 100.0 mF1 100.0 ECE 0.057; ml EM 100.0 µF1 100.0 ECE 0.048 |
| tllm_jailbreak_simple | 70 | 98.6 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.035; mc acc 100.0 mF1 100.0 ECE 0.054; ml EM 90.9 µF1 98.6 ECE 0.033 |
| tllm_jailbreak_very_hard | 60 | 86.7 | bin acc 87.5 F1 85.7 AUROC 0.972 ECE 0.107; mc acc 94.4 mF1 91.7 ECE 0.062; ml EM 70.0 µF1 94.5 ECE 0.057 |
| tllm_judge_hard | 86 | 96.5 | bin acc 95.0 F1 93.3 AUROC 0.968 ECE 0.089; mc acc 100.0 mF1 100.0 ECE 0.011; ml EM 95.2 µF1 96.2 ECE 0.024 |
| tllm_judge_simple | 72 | 97.2 | bin acc 97.4 F1 97.9 AUROC 0.997 ECE 0.066; mc acc 100.0 mF1 100.0 ECE 0.033; ml EM 92.9 µF1 98.8 ECE 0.036 |
| tllm_judge_very_hard | 64 | 92.2 | bin acc 96.9 F1 97.3 AUROC 0.996 ECE 0.073; mc acc 95.2 mF1 96.7 ECE 0.028; ml EM 72.7 µF1 95.8 ECE 0.062 |
| tllm_score_hard | 62 | 95.2 | bin acc 97.1 F1 97.0 AUROC 1.000 ECE 0.110; mc acc 93.8 mF1 85.7 ECE 0.082; ml EM 91.7 µF1 98.0 ECE 0.091 |
| tllm_score_simple | 62 | 96.8 | bin acc 94.1 F1 95.8 AUROC 0.992 ECE 0.068; mc acc 100.0 mF1 100.0 ECE 0.046; ml EM 100.0 µF1 100.0 ECE 0.040 |
| tllm_score_very_hard | 76 | 81.6 | bin acc 84.2 F1 75.0 AUROC 0.970 ECE 0.135; mc acc 86.4 mF1 75.0 ECE 0.099; ml EM 68.8 µF1 87.5 ECE 0.057 |
| tllm_verify_hard | 50 | 78.0 | bin acc 80.8 F1 80.0 AUROC 0.891 ECE 0.187; mc acc 81.2 mF1 70.6 ECE 0.135; ml EM 62.5 µF1 78.6 ECE 0.148 |
| tllm_verify_simple | 60 | 98.3 | bin acc 97.0 F1 97.6 AUROC 1.000 ECE 0.066; mc acc 100.0 mF1 100.0 ECE 0.005; ml EM 100.0 µF1 100.0 ECE 0.040 |
| tllm_verify_very_hard | 55 | 80.0 | bin acc 80.6 F1 75.0 AUROC 0.859 ECE 0.171; mc acc 86.7 mF1 82.2 ECE 0.172; ml EM 66.7 µF1 84.6 ECE 0.057 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 265 | 97.7 |
| answer_trace_mismatch | 45 | 86.7 |
| benign_lookalike | 88 | 87.5 |
| confident_wrong | 39 | 76.9 |
| contradiction | 22 | 95.5 |
| distractor | 117 | 89.7 |
| double_negation | 3 | 100.0 |
| evidence_end | 11 | 90.9 |
| evidence_middle | 20 | 75.0 |
| evidence_start | 2 | 50.0 |
| exception | 20 | 95.0 |
| fake_authority | 1 | 100.0 |
| flawed_step | 44 | 63.6 |
| format_near_miss | 46 | 87.0 |
| gradual_escalation | 1 | 100.0 |
| hypothetical | 7 | 100.0 |
| indirect_injection | 25 | 96.0 |
| injection | 22 | 100.0 |
| judge_injection | 112 | 91.1 |
| length_bias | 7 | 100.0 |
| lexical_overlap | 103 | 93.2 |
| long_state | 74 | 93.2 |
| missing_evidence | 35 | 97.1 |
| multi_positive | 124 | 85.5 |
| multi_turn | 44 | 86.4 |
| negation | 62 | 95.2 |
| nota | 55 | 89.1 |
| numeric_reasoning | 109 | 78.9 |
| obfuscation | 1 | 0.0 |
| over_refusal | 50 | 92.0 |
| paraphrase | 73 | 93.2 |
| partial_compliance | 31 | 71.0 |
| role_reversal | 6 | 66.7 |
| sarcasm | 8 | 87.5 |
| speaker_confusion | 58 | 93.1 |
| subtle_violation | 16 | 93.8 |
| sycophancy | 13 | 92.3 |
| temporal_reasoning | 20 | 95.0 |
| tool_misuse | 6 | 100.0 |
| unsupported_claim | 96 | 89.6 |
| zero_positive | 55 | 94.5 |
| zero_positive_partial | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 308 | 89.9 |
| 00128-00511 | 284 | 96.5 |
| 00512-02047 | 222 | 94.1 |
| 02048-08191 | 125 | 88.8 |
| 08192+ | 7 | 85.7 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 488 | 93.6 |
| 03 | 82 | 95.1 |
| 04 | 239 | 94.1 |
| 05 | 98 | 85.7 |
| 06 | 33 | 87.9 |
| 07 | 3 | 66.7 |
| 08 | 3 | 66.7 |

## Paraphrase groups

29 groups; same prediction 96.6%; all correct 89.7%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 4.7 |
| 0.4 | 100.0 | 4.7 |
| 0.5 | 99.3 | 4.0 |
| 0.6 | 96.4 | 3.0 |
| 0.7 | 92.4 | 2.7 |
| 0.8 | 89.1 | 1.6 |
| 0.9 | 85.1 | 1.7 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 181 | 0.040 | 0.006 |
| [0.1,0.2) | 22 | 0.140 | 0.045 |
| [0.2,0.3) | 15 | 0.253 | 0.200 |
| [0.3,0.4) | 8 | 0.345 | 0.375 |
| [0.4,0.5) | 8 | 0.454 | 0.375 |
| [0.5,0.6) | 8 | 0.547 | 0.250 |
| [0.6,0.7) | 8 | 0.664 | 0.875 |
| [0.7,0.8) | 16 | 0.751 | 0.812 |
| [0.8,0.9) | 27 | 0.857 | 0.778 |
| [0.9,1.0] | 195 | 0.970 | 0.979 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.4,0.5) | 2 | 0.446 | 0.000 |
| [0.5,0.6) | 8 | 0.532 | 0.625 |
| [0.6,0.7) | 11 | 0.639 | 0.909 |
| [0.7,0.8) | 9 | 0.769 | 0.667 |
| [0.8,0.9) | 11 | 0.870 | 1.000 |
| [0.9,1.0] | 235 | 0.988 | 0.983 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 390 | 0.036 | 0.023 |
| [0.1,0.2) | 31 | 0.150 | 0.129 |
| [0.2,0.3) | 15 | 0.240 | 0.200 |
| [0.3,0.4) | 9 | 0.361 | 0.556 |
| [0.4,0.5) | 6 | 0.465 | 0.500 |
| [0.5,0.6) | 9 | 0.544 | 0.778 |
| [0.6,0.7) | 7 | 0.664 | 1.000 |
| [0.7,0.8) | 9 | 0.754 | 0.778 |
| [0.8,0.9) | 26 | 0.859 | 0.846 |
| [0.9,1.0] | 362 | 0.974 | 0.997 |
