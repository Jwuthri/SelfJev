# Evaluation report

- model `mica-4b` @ `-` (external open model via /v1/systemone), adapter/checkpoint `None`, prompt `jev-request` (-)
- data data/eval_llm.jsonl; splits ['test']; n=939; calibration `None`
- cuda / -; 2026-09-30T18:42:10+0000; wall 69.4s

## Overall

question accuracy 84.8%

![reliability](reliability.svg)

**binary**: n 486, positives 244, accuracy 0.893, precision 0.884, recall 0.906, f1 0.895, auroc 0.958, brier 0.082, log_loss 0.267, ece 0.043

**multiclass**: n 274, accuracy 0.927, macro_f1 0.866, log_loss 0.210, brier 0.108, ece_top_label 0.043

**multilabel**: n 179, labels 845, exact_match 0.603, micro_f1 0.871, macro_f1 0.783, label_auroc 0.949, brier 0.093, log_loss 0.305, ece 0.048

## By family

| family | n | question acc % | details |
|---|---|---|---|
| tllm_guardrail_hard | 60 | 83.3 | bin acc 75.0 F1 73.3 AUROC 0.905 ECE 0.129; mc acc 100.0 mF1 100.0 ECE 0.104; ml EM 81.8 µF1 94.7 ECE 0.097 |
| tllm_guardrail_simple | 67 | 94.0 | bin acc 97.1 F1 97.3 AUROC 1.000 ECE 0.069; mc acc 100.0 mF1 100.0 ECE 0.025; ml EM 78.6 µF1 95.5 ECE 0.070 |
| tllm_guardrail_very_hard | 43 | 90.7 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.047; mc acc 92.9 mF1 83.3 ECE 0.103; ml EM 66.7 µF1 92.0 ECE 0.066 |
| tllm_jailbreak_hard | 59 | 83.1 | bin acc 77.8 F1 78.6 AUROC 0.883 ECE 0.211; mc acc 100.0 mF1 100.0 ECE 0.103; ml EM 66.7 µF1 92.9 ECE 0.096 |
| tllm_jailbreak_simple | 70 | 92.9 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.055; mc acc 95.5 mF1 87.5 ECE 0.049; ml EM 63.6 µF1 91.7 ECE 0.105 |
| tllm_jailbreak_very_hard | 60 | 80.0 | bin acc 81.2 F1 80.0 AUROC 0.923 ECE 0.129; mc acc 88.9 mF1 80.4 ECE 0.084; ml EM 60.0 µF1 92.6 ECE 0.087 |
| tllm_judge_hard | 86 | 83.7 | bin acc 95.0 F1 93.3 AUROC 0.992 ECE 0.075; mc acc 92.0 mF1 82.6 ECE 0.066; ml EM 52.4 µF1 71.6 ECE 0.145 |
| tllm_judge_simple | 72 | 93.1 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.066; mc acc 90.0 mF1 77.8 ECE 0.108; ml EM 78.6 µF1 95.3 ECE 0.069 |
| tllm_judge_very_hard | 61 | 86.9 | bin acc 96.8 F1 97.1 AUROC 0.992 ECE 0.066; mc acc 90.0 mF1 75.4 ECE 0.109; ml EM 50.0 µF1 86.2 ECE 0.119 |
| tllm_score_hard | 62 | 87.1 | bin acc 94.1 F1 93.8 AUROC 0.986 ECE 0.090; mc acc 100.0 mF1 100.0 ECE 0.060; ml EM 50.0 µF1 88.9 ECE 0.100 |
| tllm_score_simple | 62 | 87.1 | bin acc 88.2 F1 91.3 AUROC 0.958 ECE 0.157; mc acc 100.0 mF1 100.0 ECE 0.096; ml EM 66.7 µF1 90.4 ECE 0.078 |
| tllm_score_very_hard | 72 | 73.6 | bin acc 81.1 F1 74.1 AUROC 0.951 ECE 0.147; mc acc 90.5 mF1 81.8 ECE 0.090; ml EM 28.6 µF1 67.6 ECE 0.191 |
| tllm_verify_hard | 50 | 76.0 | bin acc 80.8 F1 78.3 AUROC 0.897 ECE 0.247; mc acc 81.2 mF1 70.6 ECE 0.200; ml EM 50.0 µF1 75.0 ECE 0.128 |
| tllm_verify_simple | 60 | 91.7 | bin acc 93.9 F1 95.2 AUROC 0.948 ECE 0.094; mc acc 100.0 mF1 100.0 ECE 0.031; ml EM 75.0 µF1 90.6 ECE 0.075 |
| tllm_verify_very_hard | 55 | 65.5 | bin acc 74.2 F1 66.7 AUROC 0.756 ECE 0.203; mc acc 66.7 mF1 58.3 ECE 0.150; ml EM 33.3 µF1 73.3 ECE 0.134 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 265 | 93.2 |
| answer_trace_mismatch | 45 | 68.9 |
| benign_lookalike | 85 | 85.9 |
| confident_wrong | 35 | 68.6 |
| contradiction | 22 | 81.8 |
| distractor | 114 | 82.5 |
| double_negation | 3 | 66.7 |
| evidence_end | 11 | 100.0 |
| evidence_middle | 18 | 61.1 |
| evidence_start | 2 | 0.0 |
| exception | 20 | 95.0 |
| fake_authority | 1 | 100.0 |
| flawed_step | 44 | 61.4 |
| format_near_miss | 46 | 76.1 |
| gradual_escalation | 1 | 100.0 |
| hypothetical | 7 | 85.7 |
| indirect_injection | 25 | 88.0 |
| injection | 22 | 86.4 |
| judge_injection | 107 | 83.2 |
| length_bias | 7 | 100.0 |
| lexical_overlap | 103 | 86.4 |
| long_state | 70 | 81.4 |
| missing_evidence | 35 | 85.7 |
| multi_positive | 120 | 59.2 |
| multi_turn | 44 | 75.0 |
| negation | 62 | 88.7 |
| nota | 54 | 83.3 |
| numeric_reasoning | 107 | 73.8 |
| obfuscation | 1 | 0.0 |
| over_refusal | 50 | 86.0 |
| paraphrase | 73 | 89.0 |
| partial_compliance | 31 | 71.0 |
| role_reversal | 6 | 83.3 |
| sarcasm | 8 | 87.5 |
| speaker_confusion | 58 | 84.5 |
| subtle_violation | 16 | 75.0 |
| sycophancy | 10 | 90.0 |
| temporal_reasoning | 19 | 78.9 |
| tool_misuse | 6 | 50.0 |
| unsupported_claim | 96 | 81.2 |
| zero_positive | 52 | 88.5 |
| zero_positive_partial | 1 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 308 | 84.7 |
| 00128-00511 | 284 | 86.6 |
| 00512-02047 | 222 | 85.6 |
| 02048-08191 | 125 | 79.2 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 486 | 89.3 |
| 03 | 82 | 95.1 |
| 04 | 238 | 84.5 |
| 05 | 98 | 66.3 |
| 06 | 30 | 56.7 |
| 07 | 2 | 0.0 |
| 08 | 3 | 33.3 |

## Paraphrase groups

29 groups; same prediction 86.2%; all correct 79.3%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 7.3 |
| 0.4 | 99.3 | 6.6 |
| 0.5 | 96.7 | 6.0 |
| 0.6 | 93.8 | 4.7 |
| 0.7 | 88.7 | 2.1 |
| 0.8 | 83.2 | 0.4 |
| 0.9 | 76.3 | 0.0 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 182 | 0.023 | 0.044 |
| [0.1,0.2) | 22 | 0.150 | 0.182 |
| [0.2,0.3) | 11 | 0.271 | 0.273 |
| [0.3,0.4) | 8 | 0.360 | 0.625 |
| [0.4,0.5) | 13 | 0.451 | 0.231 |
| [0.5,0.6) | 18 | 0.546 | 0.500 |
| [0.6,0.7) | 23 | 0.652 | 0.870 |
| [0.7,0.8) | 19 | 0.757 | 0.632 |
| [0.8,0.9) | 29 | 0.854 | 0.793 |
| [0.9,1.0] | 161 | 0.967 | 0.975 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.3,0.4) | 2 | 0.400 | 0.000 |
| [0.4,0.5) | 7 | 0.466 | 0.714 |
| [0.5,0.6) | 8 | 0.534 | 0.500 |
| [0.6,0.7) | 14 | 0.652 | 0.500 |
| [0.7,0.8) | 15 | 0.744 | 0.733 |
| [0.8,0.9) | 19 | 0.851 | 0.947 |
| [0.9,1.0] | 209 | 0.977 | 1.000 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 234 | 0.031 | 0.021 |
| [0.1,0.2) | 60 | 0.149 | 0.050 |
| [0.2,0.3) | 31 | 0.242 | 0.226 |
| [0.3,0.4) | 27 | 0.349 | 0.259 |
| [0.4,0.5) | 32 | 0.450 | 0.406 |
| [0.5,0.6) | 38 | 0.546 | 0.395 |
| [0.6,0.7) | 20 | 0.654 | 0.550 |
| [0.7,0.8) | 39 | 0.752 | 0.615 |
| [0.8,0.9) | 51 | 0.856 | 0.745 |
| [0.9,1.0] | 313 | 0.973 | 0.942 |


Answered 939/946; errors 2; accuracy counting failures as wrong 84.1%.
Paired vs ours (images_v1/eval_llm): ours only right 98, mica-4b only right 19, p = 5.1e-14
