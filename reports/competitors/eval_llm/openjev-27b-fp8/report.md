# Evaluation report

- model `openjev-27b-fp8` @ `-` (external open model via /v1/systemone), adapter/checkpoint `None`, prompt `jev-request` (-)
- data data/eval_llm.jsonl; splits ['test']; n=946; calibration `None`
- cuda / -; 2026-09-30T20:52:11+0000; wall 329.1s

## Overall

question accuracy 92.6%

![reliability](reliability.svg)

**binary**: n 488, positives 245, accuracy 0.930, precision 0.907, recall 0.959, f1 0.933, auroc 0.985, brier 0.052, log_loss 0.180, ece 0.047

**multiclass**: n 276, accuracy 0.957, macro_f1 0.930, log_loss 0.160, brier 0.073, ece_top_label 0.028

**multilabel**: n 182, labels 864, exact_match 0.868, micro_f1 0.967, macro_f1 0.935, label_auroc 0.995, brier 0.027, log_loss 0.110, ece 0.036

## By family

| family | n | question acc % | details |
|---|---|---|---|
| tllm_guardrail_hard | 60 | 88.3 | bin acc 84.4 F1 84.8 AUROC 0.976 ECE 0.171; mc acc 100.0 mF1 100.0 ECE 0.022; ml EM 81.8 µF1 93.0 ECE 0.094 |
| tllm_guardrail_simple | 67 | 98.5 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.032; mc acc 100.0 mF1 100.0 ECE 0.011; ml EM 92.9 µF1 98.5 ECE 0.043 |
| tllm_guardrail_very_hard | 43 | 100.0 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.039; mc acc 100.0 mF1 100.0 ECE 0.019; ml EM 100.0 µF1 100.0 ECE 0.039 |
| tllm_jailbreak_hard | 59 | 98.3 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.054; mc acc 95.0 mF1 93.3 ECE 0.082; ml EM 100.0 µF1 100.0 ECE 0.080 |
| tllm_jailbreak_simple | 70 | 98.6 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.052; mc acc 100.0 mF1 100.0 ECE 0.013; ml EM 90.9 µF1 98.6 ECE 0.026 |
| tllm_jailbreak_very_hard | 60 | 81.7 | bin acc 84.4 F1 83.9 AUROC 0.992 ECE 0.146; mc acc 94.4 mF1 91.7 ECE 0.071; ml EM 50.0 µF1 91.2 ECE 0.093 |
| tllm_judge_hard | 86 | 95.3 | bin acc 95.0 F1 93.8 AUROC 0.992 ECE 0.098; mc acc 100.0 mF1 100.0 ECE 0.013; ml EM 90.5 µF1 96.3 ECE 0.049 |
| tllm_judge_simple | 72 | 95.8 | bin acc 94.7 F1 95.8 AUROC 0.964 ECE 0.030; mc acc 95.0 mF1 88.2 ECE 0.043; ml EM 100.0 µF1 100.0 ECE 0.048 |
| tllm_judge_very_hard | 64 | 93.8 | bin acc 96.9 F1 97.3 AUROC 0.992 ECE 0.092; mc acc 90.5 mF1 87.5 ECE 0.070; ml EM 90.9 µF1 98.6 ECE 0.056 |
| tllm_score_hard | 62 | 96.8 | bin acc 97.1 F1 96.8 AUROC 1.000 ECE 0.056; mc acc 100.0 mF1 100.0 ECE 0.018; ml EM 91.7 µF1 98.1 ECE 0.096 |
| tllm_score_simple | 62 | 98.4 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.042; mc acc 100.0 mF1 100.0 ECE 0.022; ml EM 91.7 µF1 98.5 ECE 0.034 |
| tllm_score_very_hard | 76 | 88.2 | bin acc 92.1 F1 87.0 AUROC 0.987 ECE 0.084; mc acc 90.9 mF1 82.6 ECE 0.094; ml EM 75.0 µF1 89.9 ECE 0.071 |
| tllm_verify_hard | 50 | 78.0 | bin acc 73.1 F1 69.6 AUROC 0.897 ECE 0.178; mc acc 93.8 mF1 87.5 ECE 0.106; ml EM 62.5 µF1 91.4 ECE 0.118 |
| tllm_verify_simple | 60 | 96.7 | bin acc 97.0 F1 97.6 AUROC 1.000 ECE 0.070; mc acc 100.0 mF1 100.0 ECE 0.020; ml EM 91.7 µF1 98.5 ECE 0.052 |
| tllm_verify_very_hard | 55 | 76.4 | bin acc 77.4 F1 72.0 AUROC 0.823 ECE 0.154; mc acc 73.3 mF1 59.3 ECE 0.155; ml EM 77.8 µF1 88.9 ECE 0.103 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 265 | 97.7 |
| answer_trace_mismatch | 45 | 86.7 |
| benign_lookalike | 88 | 85.2 |
| confident_wrong | 39 | 84.6 |
| contradiction | 22 | 100.0 |
| distractor | 117 | 90.6 |
| double_negation | 3 | 100.0 |
| evidence_end | 11 | 90.9 |
| evidence_middle | 20 | 90.0 |
| evidence_start | 2 | 100.0 |
| exception | 20 | 100.0 |
| fake_authority | 1 | 100.0 |
| flawed_step | 44 | 72.7 |
| format_near_miss | 46 | 93.5 |
| gradual_escalation | 1 | 100.0 |
| hypothetical | 7 | 100.0 |
| indirect_injection | 25 | 96.0 |
| injection | 22 | 95.5 |
| judge_injection | 112 | 92.0 |
| length_bias | 7 | 100.0 |
| lexical_overlap | 103 | 90.3 |
| long_state | 74 | 87.8 |
| missing_evidence | 35 | 94.3 |
| multi_positive | 124 | 87.1 |
| multi_turn | 44 | 84.1 |
| negation | 62 | 98.4 |
| nota | 55 | 90.9 |
| numeric_reasoning | 109 | 84.4 |
| obfuscation | 1 | 100.0 |
| over_refusal | 50 | 92.0 |
| paraphrase | 73 | 91.8 |
| partial_compliance | 31 | 77.4 |
| role_reversal | 6 | 66.7 |
| sarcasm | 8 | 100.0 |
| speaker_confusion | 58 | 86.2 |
| subtle_violation | 16 | 100.0 |
| sycophancy | 13 | 100.0 |
| temporal_reasoning | 20 | 85.0 |
| tool_misuse | 6 | 66.7 |
| unsupported_claim | 96 | 88.5 |
| zero_positive | 55 | 92.7 |
| zero_positive_partial | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 308 | 89.0 |
| 00128-00511 | 284 | 94.4 |
| 00512-02047 | 222 | 94.1 |
| 02048-08191 | 125 | 94.4 |
| 08192+ | 7 | 100.0 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 488 | 93.0 |
| 03 | 82 | 91.5 |
| 04 | 239 | 94.1 |
| 05 | 98 | 87.8 |
| 06 | 33 | 93.9 |
| 07 | 3 | 100.0 |
| 08 | 3 | 66.7 |

## Paraphrase groups

29 groups; same prediction 86.2%; all correct 79.3%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 4.3 |
| 0.4 | 99.6 | 4.0 |
| 0.5 | 99.3 | 3.6 |
| 0.6 | 99.3 | 3.6 |
| 0.7 | 97.8 | 3.3 |
| 0.8 | 94.9 | 2.7 |
| 0.9 | 89.9 | 2.8 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 175 | 0.030 | 0.000 |
| [0.1,0.2) | 30 | 0.137 | 0.167 |
| [0.2,0.3) | 17 | 0.235 | 0.235 |
| [0.3,0.4) | 4 | 0.372 | 0.250 |
| [0.4,0.5) | 3 | 0.427 | 0.000 |
| [0.5,0.6) | 7 | 0.554 | 0.143 |
| [0.6,0.7) | 3 | 0.649 | 0.667 |
| [0.7,0.8) | 12 | 0.756 | 0.667 |
| [0.8,0.9) | 26 | 0.866 | 0.654 |
| [0.9,1.0] | 211 | 0.956 | 0.981 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.3,0.4) | 1 | 0.399 | 0.000 |
| [0.4,0.5) | 1 | 0.496 | 0.000 |
| [0.6,0.7) | 4 | 0.641 | 0.750 |
| [0.7,0.8) | 8 | 0.750 | 0.750 |
| [0.8,0.9) | 14 | 0.861 | 1.000 |
| [0.9,1.0] | 248 | 0.989 | 0.972 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 349 | 0.028 | 0.003 |
| [0.1,0.2) | 40 | 0.139 | 0.050 |
| [0.2,0.3) | 17 | 0.246 | 0.118 |
| [0.3,0.4) | 9 | 0.325 | 0.000 |
| [0.4,0.5) | 10 | 0.458 | 0.400 |
| [0.5,0.6) | 7 | 0.546 | 0.429 |
| [0.6,0.7) | 7 | 0.647 | 0.286 |
| [0.7,0.8) | 13 | 0.763 | 0.846 |
| [0.8,0.9) | 37 | 0.861 | 0.946 |
| [0.9,1.0] | 375 | 0.968 | 0.981 |


Answered 946/946; errors 0; accuracy counting failures as wrong 92.6%.
Paired vs ours (images_v1/eval_llm): ours only right 34, openjev-27b-fp8 only right 35, p = 1
