# Evaluation report

- model `plumb-4b` @ `-` (external open model via /v1/systemone), adapter/checkpoint `None`, prompt `jev-request` (-)
- data data/eval_llm.jsonl; splits ['test']; n=946; calibration `None`
- cuda / -; 2026-09-30T18:57:13+0000; wall 163.9s

## Overall

question accuracy 84.1%

![reliability](reliability.svg)

**binary**: n 488, positives 245, accuracy 0.885, precision 0.883, recall 0.890, f1 0.886, auroc 0.942, brier 0.092, log_loss 0.306, ece 0.021

**multiclass**: n 276, accuracy 0.906, macro_f1 0.846, log_loss 0.286, brier 0.134, ece_top_label 0.036

**multilabel**: n 182, labels 864, exact_match 0.626, micro_f1 0.896, macro_f1 0.814, label_auroc 0.968, brier 0.075, log_loss 0.249, ece 0.053

## By family

| family | n | question acc % | details |
|---|---|---|---|
| tllm_guardrail_hard | 60 | 88.3 | bin acc 93.8 F1 93.3 AUROC 1.000 ECE 0.190; mc acc 94.1 mF1 91.7 ECE 0.089; ml EM 63.6 µF1 88.4 ECE 0.124 |
| tllm_guardrail_simple | 67 | 94.0 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.031; mc acc 94.7 mF1 89.5 ECE 0.046; ml EM 78.6 µF1 95.5 ECE 0.037 |
| tllm_guardrail_very_hard | 43 | 86.0 | bin acc 95.0 F1 95.7 AUROC 0.979 ECE 0.121; mc acc 92.9 mF1 88.9 ECE 0.052; ml EM 55.6 µF1 88.0 ECE 0.089 |
| tllm_jailbreak_hard | 59 | 74.6 | bin acc 74.1 F1 74.1 AUROC 0.825 ECE 0.210; mc acc 85.0 mF1 72.9 ECE 0.164; ml EM 58.3 µF1 87.3 ECE 0.123 |
| tllm_jailbreak_simple | 70 | 94.3 | bin acc 97.3 F1 97.6 AUROC 0.997 ECE 0.061; mc acc 95.5 mF1 87.5 ECE 0.065; ml EM 81.8 µF1 97.1 ECE 0.063 |
| tllm_jailbreak_very_hard | 60 | 78.3 | bin acc 84.4 F1 81.5 AUROC 0.939 ECE 0.105; mc acc 83.3 mF1 78.4 ECE 0.137; ml EM 50.0 µF1 89.7 ECE 0.097 |
| tllm_judge_hard | 86 | 89.5 | bin acc 97.5 F1 96.8 AUROC 0.979 ECE 0.161; mc acc 92.0 mF1 82.6 ECE 0.053; ml EM 71.4 µF1 85.2 ECE 0.121 |
| tllm_judge_simple | 72 | 90.3 | bin acc 94.7 F1 95.8 AUROC 0.994 ECE 0.076; mc acc 95.0 mF1 88.2 ECE 0.079; ml EM 71.4 µF1 95.1 ECE 0.100 |
| tllm_judge_very_hard | 64 | 87.5 | bin acc 93.8 F1 94.4 AUROC 0.972 ECE 0.121; mc acc 90.5 mF1 88.5 ECE 0.147; ml EM 63.6 µF1 92.8 ECE 0.107 |
| tllm_score_hard | 62 | 77.4 | bin acc 85.3 F1 84.8 AUROC 0.965 ECE 0.137; mc acc 93.8 mF1 90.5 ECE 0.120; ml EM 33.3 µF1 80.6 ECE 0.163 |
| tllm_score_simple | 62 | 91.9 | bin acc 91.2 F1 93.6 AUROC 0.908 ECE 0.087; mc acc 100.0 mF1 100.0 ECE 0.097; ml EM 83.3 µF1 95.8 ECE 0.070 |
| tllm_score_very_hard | 76 | 76.3 | bin acc 89.5 F1 83.3 AUROC 0.985 ECE 0.110; mc acc 81.8 mF1 68.0 ECE 0.111; ml EM 37.5 µF1 80.0 ECE 0.114 |
| tllm_verify_hard | 50 | 64.0 | bin acc 65.4 F1 64.0 AUROC 0.618 ECE 0.254; mc acc 81.2 mF1 66.7 ECE 0.088; ml EM 25.0 µF1 79.1 ECE 0.185 |
| tllm_verify_simple | 60 | 90.0 | bin acc 87.9 F1 90.0 AUROC 0.980 ECE 0.139; mc acc 100.0 mF1 100.0 ECE 0.070; ml EM 83.3 µF1 94.1 ECE 0.065 |
| tllm_verify_very_hard | 55 | 70.9 | bin acc 67.7 F1 54.5 AUROC 0.718 ECE 0.204; mc acc 80.0 mF1 68.6 ECE 0.137; ml EM 66.7 µF1 86.7 ECE 0.181 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 265 | 93.6 |
| answer_trace_mismatch | 45 | 80.0 |
| benign_lookalike | 88 | 79.5 |
| confident_wrong | 39 | 69.2 |
| contradiction | 22 | 90.9 |
| distractor | 117 | 77.8 |
| double_negation | 3 | 100.0 |
| evidence_end | 11 | 90.9 |
| evidence_middle | 20 | 65.0 |
| evidence_start | 2 | 50.0 |
| exception | 20 | 95.0 |
| fake_authority | 1 | 100.0 |
| flawed_step | 44 | 61.4 |
| format_near_miss | 46 | 67.4 |
| gradual_escalation | 1 | 100.0 |
| hypothetical | 7 | 100.0 |
| indirect_injection | 25 | 88.0 |
| injection | 22 | 100.0 |
| judge_injection | 112 | 83.0 |
| length_bias | 7 | 100.0 |
| lexical_overlap | 103 | 85.4 |
| long_state | 74 | 75.7 |
| missing_evidence | 35 | 94.3 |
| multi_positive | 124 | 62.9 |
| multi_turn | 44 | 81.8 |
| negation | 62 | 87.1 |
| nota | 55 | 76.4 |
| numeric_reasoning | 109 | 72.5 |
| obfuscation | 1 | 0.0 |
| over_refusal | 50 | 88.0 |
| paraphrase | 73 | 83.6 |
| partial_compliance | 31 | 67.7 |
| role_reversal | 6 | 66.7 |
| sarcasm | 8 | 100.0 |
| speaker_confusion | 58 | 86.2 |
| subtle_violation | 16 | 93.8 |
| sycophancy | 13 | 84.6 |
| temporal_reasoning | 20 | 75.0 |
| tool_misuse | 6 | 16.7 |
| unsupported_claim | 96 | 79.2 |
| zero_positive | 55 | 85.5 |
| zero_positive_partial | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 308 | 82.5 |
| 00128-00511 | 284 | 84.9 |
| 00512-02047 | 222 | 89.2 |
| 02048-08191 | 125 | 79.2 |
| 08192+ | 7 | 57.1 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 488 | 88.5 |
| 03 | 82 | 87.8 |
| 04 | 239 | 81.6 |
| 05 | 98 | 73.5 |
| 06 | 33 | 72.7 |
| 07 | 3 | 0.0 |
| 08 | 3 | 33.3 |

## Paraphrase groups

29 groups; same prediction 79.3%; all correct 75.9%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 9.4 |
| 0.4 | 99.6 | 9.1 |
| 0.5 | 96.7 | 7.9 |
| 0.6 | 92.8 | 5.9 |
| 0.7 | 87.0 | 3.8 |
| 0.8 | 83.0 | 3.1 |
| 0.9 | 60.5 | 1.2 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 136 | 0.037 | 0.037 |
| [0.1,0.2) | 49 | 0.147 | 0.143 |
| [0.2,0.3) | 28 | 0.243 | 0.250 |
| [0.3,0.4) | 14 | 0.341 | 0.286 |
| [0.4,0.5) | 14 | 0.443 | 0.286 |
| [0.5,0.6) | 11 | 0.526 | 0.636 |
| [0.6,0.7) | 16 | 0.658 | 0.688 |
| [0.7,0.8) | 21 | 0.758 | 0.619 |
| [0.8,0.9) | 44 | 0.858 | 0.886 |
| [0.9,1.0] | 155 | 0.962 | 0.955 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.3,0.4) | 1 | 0.386 | 0.000 |
| [0.4,0.5) | 8 | 0.463 | 0.500 |
| [0.5,0.6) | 11 | 0.549 | 0.455 |
| [0.6,0.7) | 16 | 0.660 | 0.625 |
| [0.7,0.8) | 11 | 0.758 | 0.818 |
| [0.8,0.9) | 62 | 0.864 | 0.919 |
| [0.9,1.0] | 167 | 0.967 | 0.988 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 230 | 0.038 | 0.000 |
| [0.1,0.2) | 77 | 0.140 | 0.013 |
| [0.2,0.3) | 26 | 0.238 | 0.115 |
| [0.3,0.4) | 26 | 0.340 | 0.308 |
| [0.4,0.5) | 29 | 0.443 | 0.379 |
| [0.5,0.6) | 26 | 0.540 | 0.308 |
| [0.6,0.7) | 27 | 0.653 | 0.593 |
| [0.7,0.8) | 41 | 0.756 | 0.610 |
| [0.8,0.9) | 72 | 0.853 | 0.778 |
| [0.9,1.0] | 310 | 0.961 | 0.968 |


Answered 946/946; errors 0; accuracy counting failures as wrong 84.1%.
Paired vs ours (images_v1/eval_llm): ours only right 97, plumb-4b only right 18, p = 2.8e-14
