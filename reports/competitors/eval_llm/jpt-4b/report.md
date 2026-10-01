# Evaluation report

- model `jpt-4b` @ `-` (external open model via /v1/systemone), adapter/checkpoint `None`, prompt `jev-request` (-)
- data data/eval_llm.jsonl; splits ['test']; n=946; calibration `None`
- cuda / -; 2026-09-30T19:31:32+0000; wall 40.0s

## Overall

question accuracy 85.0%

![reliability](reliability.svg)

**binary**: n 488, positives 245, accuracy 0.895, precision 0.873, recall 0.927, f1 0.899, auroc 0.951, brier 0.081, log_loss 0.282, ece 0.027

**multiclass**: n 276, accuracy 0.899, macro_f1 0.830, log_loss 0.332, brier 0.169, ece_top_label 0.035

**multilabel**: n 182, labels 864, exact_match 0.654, micro_f1 0.899, macro_f1 0.822, label_auroc 0.963, brier 0.076, log_loss 0.259, ece 0.040

## By family

| family | n | question acc % | details |
|---|---|---|---|
| tllm_guardrail_hard | 60 | 75.0 | bin acc 75.0 F1 77.8 AUROC 0.956 ECE 0.225; mc acc 94.1 mF1 87.5 ECE 0.135; ml EM 45.5 µF1 79.1 ECE 0.173 |
| tllm_guardrail_simple | 67 | 95.5 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.029; mc acc 94.7 mF1 93.3 ECE 0.075; ml EM 85.7 µF1 97.0 ECE 0.049 |
| tllm_guardrail_very_hard | 43 | 93.0 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.078; mc acc 92.9 mF1 83.3 ECE 0.128; ml EM 77.8 µF1 93.9 ECE 0.078 |
| tllm_jailbreak_hard | 59 | 78.0 | bin acc 81.5 F1 81.5 AUROC 0.883 ECE 0.183; mc acc 90.0 mF1 86.2 ECE 0.142; ml EM 50.0 µF1 84.6 ECE 0.100 |
| tllm_jailbreak_simple | 70 | 94.3 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.056; mc acc 90.9 mF1 76.5 ECE 0.066; ml EM 81.8 µF1 97.1 ECE 0.033 |
| tllm_jailbreak_very_hard | 60 | 81.7 | bin acc 84.4 F1 82.8 AUROC 0.960 ECE 0.131; mc acc 88.9 mF1 82.4 ECE 0.078; ml EM 60.0 µF1 92.6 ECE 0.080 |
| tllm_judge_hard | 86 | 91.9 | bin acc 90.0 F1 85.7 AUROC 0.976 ECE 0.085; mc acc 100.0 mF1 100.0 ECE 0.089; ml EM 85.7 µF1 90.6 ECE 0.059 |
| tllm_judge_simple | 72 | 90.3 | bin acc 94.7 F1 95.8 AUROC 0.980 ECE 0.054; mc acc 90.0 mF1 81.2 ECE 0.049; ml EM 78.6 µF1 96.4 ECE 0.048 |
| tllm_judge_very_hard | 64 | 87.5 | bin acc 93.8 F1 94.4 AUROC 0.948 ECE 0.112; mc acc 95.2 mF1 91.6 ECE 0.110; ml EM 54.5 µF1 89.9 ECE 0.130 |
| tllm_score_hard | 62 | 82.3 | bin acc 88.2 F1 87.5 AUROC 0.969 ECE 0.147; mc acc 100.0 mF1 100.0 ECE 0.129; ml EM 41.7 µF1 80.7 ECE 0.138 |
| tllm_score_simple | 62 | 93.5 | bin acc 97.1 F1 98.0 AUROC 0.912 ECE 0.034; mc acc 93.8 mF1 88.2 ECE 0.113; ml EM 83.3 µF1 97.1 ECE 0.055 |
| tllm_score_very_hard | 76 | 80.3 | bin acc 89.5 F1 84.6 AUROC 0.973 ECE 0.079; mc acc 77.3 mF1 63.2 ECE 0.144; ml EM 62.5 µF1 87.1 ECE 0.074 |
| tllm_verify_hard | 50 | 66.0 | bin acc 73.1 F1 72.0 AUROC 0.724 ECE 0.244; mc acc 75.0 mF1 64.7 ECE 0.254; ml EM 25.0 µF1 69.0 ECE 0.158 |
| tllm_verify_simple | 60 | 90.0 | bin acc 90.9 F1 92.7 AUROC 0.980 ECE 0.134; mc acc 100.0 mF1 100.0 ECE 0.057; ml EM 75.0 µF1 90.6 ECE 0.105 |
| tllm_verify_very_hard | 55 | 67.3 | bin acc 80.6 F1 76.9 AUROC 0.829 ECE 0.185; mc acc 60.0 mF1 47.4 ECE 0.262; ml EM 33.3 µF1 74.1 ECE 0.106 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 265 | 93.6 |
| answer_trace_mismatch | 45 | 75.6 |
| benign_lookalike | 88 | 80.7 |
| confident_wrong | 39 | 71.8 |
| contradiction | 22 | 95.5 |
| distractor | 117 | 83.8 |
| double_negation | 3 | 66.7 |
| evidence_end | 11 | 90.9 |
| evidence_middle | 20 | 70.0 |
| evidence_start | 2 | 50.0 |
| exception | 20 | 90.0 |
| fake_authority | 1 | 100.0 |
| flawed_step | 44 | 54.5 |
| format_near_miss | 46 | 82.6 |
| gradual_escalation | 1 | 100.0 |
| hypothetical | 7 | 100.0 |
| indirect_injection | 25 | 88.0 |
| injection | 22 | 95.5 |
| judge_injection | 112 | 81.2 |
| length_bias | 7 | 100.0 |
| lexical_overlap | 103 | 84.5 |
| long_state | 74 | 82.4 |
| missing_evidence | 35 | 88.6 |
| multi_positive | 124 | 64.5 |
| multi_turn | 44 | 84.1 |
| negation | 62 | 91.9 |
| nota | 55 | 80.0 |
| numeric_reasoning | 109 | 75.2 |
| obfuscation | 1 | 0.0 |
| over_refusal | 50 | 88.0 |
| paraphrase | 73 | 89.0 |
| partial_compliance | 31 | 71.0 |
| role_reversal | 6 | 83.3 |
| sarcasm | 8 | 62.5 |
| speaker_confusion | 58 | 75.9 |
| subtle_violation | 16 | 81.2 |
| sycophancy | 13 | 84.6 |
| temporal_reasoning | 20 | 80.0 |
| tool_misuse | 6 | 33.3 |
| unsupported_claim | 96 | 83.3 |
| zero_positive | 55 | 90.9 |
| zero_positive_partial | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 308 | 79.9 |
| 00128-00511 | 284 | 88.7 |
| 00512-02047 | 222 | 89.2 |
| 02048-08191 | 125 | 82.4 |
| 08192+ | 7 | 71.4 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 488 | 89.5 |
| 03 | 82 | 90.2 |
| 04 | 239 | 82.4 |
| 05 | 98 | 69.4 |
| 06 | 33 | 75.8 |
| 07 | 3 | 33.3 |
| 08 | 3 | 66.7 |

## Paraphrase groups

29 groups; same prediction 82.8%; all correct 75.9%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 10.1 |
| 0.4 | 100.0 | 10.1 |
| 0.5 | 96.4 | 8.6 |
| 0.6 | 92.8 | 8.2 |
| 0.7 | 88.4 | 6.6 |
| 0.8 | 81.2 | 5.4 |
| 0.9 | 60.9 | 1.8 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 178 | 0.026 | 0.039 |
| [0.1,0.2) | 21 | 0.146 | 0.143 |
| [0.2,0.3) | 8 | 0.253 | 0.250 |
| [0.3,0.4) | 10 | 0.351 | 0.400 |
| [0.4,0.5) | 11 | 0.440 | 0.182 |
| [0.5,0.6) | 9 | 0.550 | 0.556 |
| [0.6,0.7) | 15 | 0.666 | 0.467 |
| [0.7,0.8) | 16 | 0.766 | 0.688 |
| [0.8,0.9) | 42 | 0.869 | 0.833 |
| [0.9,1.0] | 178 | 0.958 | 0.949 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.4,0.5) | 10 | 0.451 | 0.500 |
| [0.5,0.6) | 10 | 0.545 | 0.800 |
| [0.6,0.7) | 12 | 0.652 | 0.583 |
| [0.7,0.8) | 20 | 0.746 | 0.800 |
| [0.8,0.9) | 56 | 0.859 | 0.839 |
| [0.9,1.0] | 168 | 0.961 | 0.982 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 356 | 0.017 | 0.042 |
| [0.1,0.2) | 44 | 0.142 | 0.364 |
| [0.2,0.3) | 22 | 0.237 | 0.364 |
| [0.3,0.4) | 14 | 0.335 | 0.429 |
| [0.4,0.5) | 8 | 0.436 | 0.250 |
| [0.5,0.6) | 12 | 0.545 | 0.500 |
| [0.6,0.7) | 17 | 0.662 | 0.588 |
| [0.7,0.8) | 23 | 0.756 | 0.609 |
| [0.8,0.9) | 50 | 0.859 | 0.820 |
| [0.9,1.0] | 318 | 0.966 | 0.975 |


Answered 946/946; errors 0; accuracy counting failures as wrong 85.0%.
Paired vs ours (images_v1/eval_llm): ours only right 92, jpt-4b only right 21, p = 8.7e-12
