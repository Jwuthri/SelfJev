# Evaluation report

- model `selfjev-4b-vision-api` @ `-` (external open model via /v1/systemone), adapter/checkpoint `None`, prompt `jev-request` (-)
- data data/eval_llm.jsonl; splits ['test']; n=946; calibration `None`
- cuda / -; 2026-09-30T17:29:14+0000; wall 88.6s

## Overall

question accuracy 90.7%

![reliability](reliability.svg)

**binary**: n 488, positives 245, accuracy 0.939, precision 0.912, recall 0.971, f1 0.941, auroc 0.981, brier 0.055, log_loss 0.194, ece 0.053

**multiclass**: n 276, accuracy 0.953, macro_f1 0.925, log_loss 0.154, brier 0.079, ece_top_label 0.020

**multilabel**: n 182, labels 864, exact_match 0.753, micro_f1 0.921, macro_f1 0.853, label_auroc 0.980, brier 0.059, log_loss 0.191, ece 0.031

## By family

| family | n | question acc % | details |
|---|---|---|---|
| tllm_guardrail_hard | 60 | 90.0 | bin acc 93.8 F1 93.3 AUROC 1.000 ECE 0.115; mc acc 94.1 mF1 87.5 ECE 0.061; ml EM 72.7 µF1 90.0 ECE 0.100 |
| tllm_guardrail_simple | 67 | 97.0 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.012; mc acc 100.0 mF1 100.0 ECE 0.022; ml EM 85.7 µF1 97.0 ECE 0.050 |
| tllm_guardrail_very_hard | 43 | 95.3 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.047; mc acc 92.9 mF1 83.3 ECE 0.034; ml EM 88.9 µF1 98.0 ECE 0.050 |
| tllm_jailbreak_hard | 59 | 98.3 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.065; mc acc 100.0 mF1 100.0 ECE 0.060; ml EM 91.7 µF1 98.2 ECE 0.078 |
| tllm_jailbreak_simple | 70 | 97.1 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.015; mc acc 100.0 mF1 100.0 ECE 0.039; ml EM 81.8 µF1 97.1 ECE 0.042 |
| tllm_jailbreak_very_hard | 60 | 85.0 | bin acc 87.5 F1 86.7 AUROC 0.955 ECE 0.129; mc acc 94.4 mF1 91.7 ECE 0.073; ml EM 60.0 µF1 92.9 ECE 0.099 |
| tllm_judge_hard | 86 | 93.0 | bin acc 92.5 F1 90.3 AUROC 0.965 ECE 0.090; mc acc 100.0 mF1 100.0 ECE 0.014; ml EM 85.7 µF1 92.6 ECE 0.056 |
| tllm_judge_simple | 72 | 95.8 | bin acc 97.4 F1 97.9 AUROC 0.997 ECE 0.050; mc acc 100.0 mF1 100.0 ECE 0.025; ml EM 85.7 µF1 97.7 ECE 0.043 |
| tllm_judge_very_hard | 64 | 92.2 | bin acc 96.9 F1 97.3 AUROC 0.996 ECE 0.076; mc acc 95.2 mF1 96.7 ECE 0.028; ml EM 72.7 µF1 95.8 ECE 0.063 |
| tllm_score_hard | 62 | 88.7 | bin acc 97.1 F1 97.0 AUROC 1.000 ECE 0.066; mc acc 100.0 mF1 100.0 ECE 0.060; ml EM 50.0 µF1 71.4 ECE 0.191 |
| tllm_score_simple | 62 | 98.4 | bin acc 97.1 F1 98.0 AUROC 0.992 ECE 0.072; mc acc 100.0 mF1 100.0 ECE 0.046; ml EM 100.0 µF1 100.0 ECE 0.038 |
| tllm_score_very_hard | 76 | 78.9 | bin acc 81.6 F1 72.0 AUROC 0.963 ECE 0.145; mc acc 86.4 mF1 75.0 ECE 0.117; ml EM 62.5 µF1 85.3 ECE 0.082 |
| tllm_verify_hard | 50 | 76.0 | bin acc 84.6 F1 83.3 AUROC 0.891 ECE 0.212; mc acc 81.2 mF1 70.6 ECE 0.200; ml EM 37.5 µF1 82.4 ECE 0.090 |
| tllm_verify_simple | 60 | 95.0 | bin acc 97.0 F1 97.6 AUROC 0.996 ECE 0.048; mc acc 100.0 mF1 100.0 ECE 0.004; ml EM 83.3 µF1 92.3 ECE 0.069 |
| tllm_verify_very_hard | 55 | 76.4 | bin acc 83.9 F1 81.5 AUROC 0.868 ECE 0.172; mc acc 80.0 mF1 70.8 ECE 0.150; ml EM 44.4 µF1 72.7 ECE 0.159 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 265 | 96.6 |
| answer_trace_mismatch | 45 | 86.7 |
| benign_lookalike | 88 | 85.2 |
| confident_wrong | 39 | 76.9 |
| contradiction | 22 | 95.5 |
| distractor | 117 | 86.3 |
| double_negation | 3 | 100.0 |
| evidence_end | 11 | 90.9 |
| evidence_middle | 20 | 75.0 |
| evidence_start | 2 | 0.0 |
| exception | 20 | 95.0 |
| fake_authority | 1 | 100.0 |
| flawed_step | 44 | 63.6 |
| format_near_miss | 46 | 82.6 |
| gradual_escalation | 1 | 100.0 |
| hypothetical | 7 | 100.0 |
| indirect_injection | 25 | 96.0 |
| injection | 22 | 95.5 |
| judge_injection | 112 | 91.1 |
| length_bias | 7 | 100.0 |
| lexical_overlap | 103 | 90.3 |
| long_state | 74 | 89.2 |
| missing_evidence | 35 | 94.3 |
| multi_positive | 124 | 78.2 |
| multi_turn | 44 | 81.8 |
| negation | 62 | 91.9 |
| nota | 55 | 87.3 |
| numeric_reasoning | 109 | 78.0 |
| obfuscation | 1 | 100.0 |
| over_refusal | 50 | 92.0 |
| paraphrase | 73 | 91.8 |
| partial_compliance | 31 | 71.0 |
| role_reversal | 6 | 83.3 |
| sarcasm | 8 | 87.5 |
| speaker_confusion | 58 | 91.4 |
| subtle_violation | 16 | 93.8 |
| sycophancy | 13 | 92.3 |
| temporal_reasoning | 20 | 85.0 |
| tool_misuse | 6 | 66.7 |
| unsupported_claim | 96 | 84.4 |
| zero_positive | 55 | 90.9 |
| zero_positive_partial | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 308 | 88.0 |
| 00128-00511 | 284 | 94.0 |
| 00512-02047 | 222 | 92.3 |
| 02048-08191 | 125 | 87.2 |
| 08192+ | 7 | 85.7 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 488 | 93.9 |
| 03 | 82 | 95.1 |
| 04 | 239 | 89.1 |
| 05 | 98 | 80.6 |
| 06 | 33 | 78.8 |
| 07 | 3 | 66.7 |
| 08 | 3 | 66.7 |

## Paraphrase groups

29 groups; same prediction 89.7%; all correct 86.2%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 4.7 |
| 0.4 | 100.0 | 4.7 |
| 0.5 | 97.8 | 3.3 |
| 0.6 | 95.3 | 3.0 |
| 0.7 | 93.5 | 2.7 |
| 0.8 | 90.6 | 2.4 |
| 0.9 | 86.2 | 1.3 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 175 | 0.020 | 0.011 |
| [0.1,0.2) | 17 | 0.139 | 0.000 |
| [0.2,0.3) | 12 | 0.265 | 0.083 |
| [0.3,0.4) | 8 | 0.350 | 0.000 |
| [0.4,0.5) | 15 | 0.448 | 0.267 |
| [0.5,0.6) | 5 | 0.539 | 1.000 |
| [0.6,0.7) | 8 | 0.660 | 0.500 |
| [0.7,0.8) | 13 | 0.749 | 0.538 |
| [0.8,0.9) | 16 | 0.873 | 0.750 |
| [0.9,1.0] | 219 | 0.985 | 0.959 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.4,0.5) | 6 | 0.449 | 0.333 |
| [0.5,0.6) | 7 | 0.570 | 0.857 |
| [0.6,0.7) | 5 | 0.670 | 0.800 |
| [0.7,0.8) | 8 | 0.763 | 0.875 |
| [0.8,0.9) | 12 | 0.854 | 0.750 |
| [0.9,1.0] | 238 | 0.987 | 0.987 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 315 | 0.021 | 0.019 |
| [0.1,0.2) | 39 | 0.146 | 0.128 |
| [0.2,0.3) | 31 | 0.242 | 0.258 |
| [0.3,0.4) | 17 | 0.351 | 0.235 |
| [0.4,0.5) | 19 | 0.449 | 0.211 |
| [0.5,0.6) | 14 | 0.542 | 0.286 |
| [0.6,0.7) | 13 | 0.647 | 0.538 |
| [0.7,0.8) | 17 | 0.744 | 0.588 |
| [0.8,0.9) | 25 | 0.856 | 0.560 |
| [0.9,1.0] | 374 | 0.987 | 0.979 |


Answered 946/946; errors 0; accuracy counting failures as wrong 90.7%.
Paired vs ours (images_v1/eval_llm): ours only right 31, selfjev-4b-vision-api only right 14, p = 0.016
