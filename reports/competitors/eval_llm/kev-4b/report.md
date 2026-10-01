# Evaluation report

- model `kev-4b` @ `-` (external open model via /v1/systemone), adapter/checkpoint `None`, prompt `jev-request` (-)
- data data/eval_llm.jsonl; splits ['test']; n=946; calibration `None`
- cuda / -; 2026-09-30T17:58:40+0000; wall 34.3s

## Overall

question accuracy 74.7%

![reliability](reliability.svg)

**binary**: n 488, positives 245, accuracy 0.803, precision 0.754, recall 0.902, f1 0.822, auroc 0.901, brier 0.135, log_loss 0.419, ece 0.075

**multiclass**: n 276, accuracy 0.848, macro_f1 0.771, log_loss 0.514, brier 0.261, ece_top_label 0.141

**multilabel**: n 182, labels 864, exact_match 0.445, micro_f1 0.807, macro_f1 0.687, label_auroc 0.910, brier 0.132, log_loss 0.412, ece 0.095

## By family

| family | n | question acc % | details |
|---|---|---|---|
| tllm_guardrail_hard | 60 | 66.7 | bin acc 75.0 F1 77.8 AUROC 0.921 ECE 0.261; mc acc 82.4 mF1 69.4 ECE 0.239; ml EM 18.2 µF1 79.2 ECE 0.210 |
| tllm_guardrail_simple | 67 | 91.0 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.165; mc acc 94.7 mF1 93.3 ECE 0.214; ml EM 64.3 µF1 90.9 ECE 0.126 |
| tllm_guardrail_very_hard | 43 | 93.0 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.189; mc acc 92.9 mF1 83.3 ECE 0.215; ml EM 77.8 µF1 94.1 ECE 0.201 |
| tllm_jailbreak_hard | 59 | 62.7 | bin acc 63.0 F1 61.5 AUROC 0.756 ECE 0.168; mc acc 70.0 mF1 59.8 ECE 0.190; ml EM 50.0 µF1 81.4 ECE 0.156 |
| tllm_jailbreak_simple | 70 | 85.7 | bin acc 94.6 F1 95.0 AUROC 0.994 ECE 0.142; mc acc 86.4 mF1 70.4 ECE 0.198; ml EM 54.5 µF1 93.2 ECE 0.147 |
| tllm_jailbreak_very_hard | 60 | 76.7 | bin acc 81.2 F1 80.0 AUROC 0.883 ECE 0.184; mc acc 83.3 mF1 82.3 ECE 0.157; ml EM 50.0 µF1 87.7 ECE 0.152 |
| tllm_judge_hard | 86 | 72.1 | bin acc 75.0 F1 70.6 AUROC 0.856 ECE 0.151; mc acc 88.0 mF1 79.8 ECE 0.115; ml EM 47.6 µF1 72.7 ECE 0.210 |
| tllm_judge_simple | 72 | 86.1 | bin acc 92.1 F1 93.9 AUROC 0.968 ECE 0.103; mc acc 95.0 mF1 88.2 ECE 0.127; ml EM 57.1 µF1 89.4 ECE 0.117 |
| tllm_judge_very_hard | 64 | 73.4 | bin acc 87.5 F1 89.5 AUROC 0.933 ECE 0.172; mc acc 76.2 mF1 64.4 ECE 0.333; ml EM 27.3 µF1 83.1 ECE 0.223 |
| tllm_score_hard | 62 | 74.2 | bin acc 79.4 F1 82.1 AUROC 0.955 ECE 0.210; mc acc 93.8 mF1 85.7 ECE 0.220; ml EM 33.3 µF1 61.3 ECE 0.190 |
| tllm_score_simple | 62 | 79.0 | bin acc 85.3 F1 90.2 AUROC 0.887 ECE 0.090; mc acc 93.8 mF1 88.2 ECE 0.162; ml EM 41.7 µF1 86.2 ECE 0.114 |
| tllm_score_very_hard | 76 | 69.7 | bin acc 78.9 F1 71.4 AUROC 0.882 ECE 0.209; mc acc 77.3 mF1 63.2 ECE 0.124; ml EM 37.5 µF1 75.9 ECE 0.131 |
| tllm_verify_hard | 50 | 52.0 | bin acc 42.3 F1 54.5 AUROC 0.679 ECE 0.378; mc acc 87.5 mF1 81.2 ECE 0.230; ml EM 12.5 µF1 28.6 ECE 0.192 |
| tllm_verify_simple | 60 | 85.0 | bin acc 84.8 F1 88.4 AUROC 0.893 ECE 0.176; mc acc 100.0 mF1 100.0 ECE 0.248; ml EM 66.7 µF1 89.9 ECE 0.127 |
| tllm_verify_very_hard | 55 | 49.1 | bin acc 58.1 F1 55.2 AUROC 0.697 ECE 0.250; mc acc 53.3 mF1 39.6 ECE 0.070; ml EM 11.1 µF1 55.6 ECE 0.162 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 265 | 87.9 |
| answer_trace_mismatch | 45 | 55.6 |
| benign_lookalike | 88 | 79.5 |
| confident_wrong | 39 | 56.4 |
| contradiction | 22 | 81.8 |
| distractor | 117 | 71.8 |
| double_negation | 3 | 66.7 |
| evidence_end | 11 | 100.0 |
| evidence_middle | 20 | 60.0 |
| evidence_start | 2 | 0.0 |
| exception | 20 | 90.0 |
| fake_authority | 1 | 100.0 |
| flawed_step | 44 | 45.5 |
| format_near_miss | 46 | 67.4 |
| gradual_escalation | 1 | 0.0 |
| hypothetical | 7 | 85.7 |
| indirect_injection | 25 | 72.0 |
| injection | 22 | 68.2 |
| judge_injection | 112 | 74.1 |
| length_bias | 7 | 100.0 |
| lexical_overlap | 103 | 74.8 |
| long_state | 74 | 70.3 |
| missing_evidence | 35 | 80.0 |
| multi_positive | 124 | 46.8 |
| multi_turn | 44 | 65.9 |
| negation | 62 | 83.9 |
| nota | 55 | 76.4 |
| numeric_reasoning | 109 | 63.3 |
| obfuscation | 1 | 100.0 |
| over_refusal | 50 | 74.0 |
| paraphrase | 73 | 82.2 |
| partial_compliance | 31 | 67.7 |
| role_reversal | 6 | 83.3 |
| sarcasm | 8 | 50.0 |
| speaker_confusion | 58 | 72.4 |
| subtle_violation | 16 | 62.5 |
| sycophancy | 13 | 53.8 |
| temporal_reasoning | 20 | 65.0 |
| tool_misuse | 6 | 33.3 |
| unsupported_claim | 96 | 71.9 |
| zero_positive | 55 | 58.2 |
| zero_positive_partial | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 308 | 70.1 |
| 00128-00511 | 284 | 79.2 |
| 00512-02047 | 222 | 77.5 |
| 02048-08191 | 125 | 73.6 |
| 08192+ | 7 | 28.6 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 488 | 80.3 |
| 03 | 82 | 81.7 |
| 04 | 239 | 70.7 |
| 05 | 98 | 58.2 |
| 06 | 33 | 60.6 |
| 07 | 3 | 66.7 |
| 08 | 3 | 0.0 |

## Paraphrase groups

29 groups; same prediction 86.2%; all correct 79.3%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 15.2 |
| 0.4 | 93.1 | 13.2 |
| 0.5 | 79.3 | 7.3 |
| 0.6 | 65.6 | 5.0 |
| 0.7 | 55.1 | 3.9 |
| 0.8 | 40.6 | 0.0 |
| 0.9 | 21.0 | 0.0 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 55 | 0.060 | 0.018 |
| [0.1,0.2) | 38 | 0.152 | 0.026 |
| [0.2,0.3) | 38 | 0.252 | 0.079 |
| [0.3,0.4) | 32 | 0.349 | 0.281 |
| [0.4,0.5) | 32 | 0.446 | 0.312 |
| [0.5,0.6) | 44 | 0.546 | 0.455 |
| [0.6,0.7) | 32 | 0.649 | 0.469 |
| [0.7,0.8) | 47 | 0.750 | 0.745 |
| [0.8,0.9) | 72 | 0.854 | 0.792 |
| [0.9,1.0] | 98 | 0.940 | 0.959 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.3,0.4) | 19 | 0.361 | 0.579 |
| [0.4,0.5) | 38 | 0.448 | 0.526 |
| [0.5,0.6) | 38 | 0.558 | 0.816 |
| [0.6,0.7) | 29 | 0.649 | 0.897 |
| [0.7,0.8) | 40 | 0.758 | 0.850 |
| [0.8,0.9) | 54 | 0.855 | 1.000 |
| [0.9,1.0] | 58 | 0.941 | 1.000 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 40 | 0.060 | 0.000 |
| [0.1,0.2) | 79 | 0.152 | 0.025 |
| [0.2,0.3) | 87 | 0.247 | 0.046 |
| [0.3,0.4) | 90 | 0.354 | 0.133 |
| [0.4,0.5) | 87 | 0.455 | 0.494 |
| [0.5,0.6) | 93 | 0.550 | 0.452 |
| [0.6,0.7) | 89 | 0.651 | 0.607 |
| [0.7,0.8) | 61 | 0.749 | 0.689 |
| [0.8,0.9) | 88 | 0.853 | 0.909 |
| [0.9,1.0] | 150 | 0.945 | 0.993 |


Answered 946/946; errors 0; accuracy counting failures as wrong 74.7%.
Paired vs ours (images_v1/eval_llm): ours only right 187, kev-4b only right 19, p = 6.9e-36
