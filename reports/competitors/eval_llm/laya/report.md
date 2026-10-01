# Evaluation report

- model `laya` @ `-` (external open model via /v1/systemone), adapter/checkpoint `None`, prompt `jev-request` (-)
- data data/eval_llm.jsonl; splits ['test']; n=946; calibration `None`
- cuda / -; 2026-09-30T17:33:21+0000; wall 10.9s

## Overall

question accuracy 46.4%

![reliability](reliability.svg)

**binary**: n 488, positives 245, accuracy 0.574, precision 0.558, recall 0.722, f1 0.630, auroc 0.611, brier 0.264, log_loss 0.890, ece 0.147

**multiclass**: n 276, accuracy 0.475, macro_f1 0.307, log_loss 1.257, brier 0.663, ece_top_label 0.090

**multilabel**: n 182, labels 864, exact_match 0.154, micro_f1 0.613, macro_f1 0.450, label_auroc 0.675, brier 0.235, log_loss 0.755, ece 0.092

## By family

| family | n | question acc % | details |
|---|---|---|---|
| tllm_guardrail_hard | 60 | 43.3 | bin acc 50.0 F1 60.0 AUROC 0.492 ECE 0.378; mc acc 47.1 mF1 35.0 ECE 0.237; ml EM 18.2 µF1 60.9 ECE 0.210 |
| tllm_guardrail_simple | 67 | 49.3 | bin acc 61.8 F1 64.9 AUROC 0.646 ECE 0.180; mc acc 47.4 mF1 34.4 ECE 0.332; ml EM 21.4 µF1 52.6 ECE 0.155 |
| tllm_guardrail_very_hard | 43 | 53.5 | bin acc 65.0 F1 72.0 AUROC 0.802 ECE 0.244; mc acc 64.3 mF1 42.2 ECE 0.295; ml EM 11.1 µF1 62.2 ECE 0.124 |
| tllm_jailbreak_hard | 59 | 50.8 | bin acc 55.6 F1 62.5 AUROC 0.550 ECE 0.293; mc acc 60.0 mF1 40.1 ECE 0.117; ml EM 25.0 µF1 62.7 ECE 0.162 |
| tllm_jailbreak_simple | 70 | 52.9 | bin acc 67.6 F1 76.0 AUROC 0.871 ECE 0.226; mc acc 50.0 mF1 29.0 ECE 0.146; ml EM 9.1 µF1 72.7 ECE 0.207 |
| tllm_jailbreak_very_hard | 60 | 41.7 | bin acc 50.0 F1 52.9 AUROC 0.640 ECE 0.338; mc acc 38.9 mF1 29.2 ECE 0.268; ml EM 20.0 µF1 69.2 ECE 0.145 |
| tllm_judge_hard | 86 | 52.3 | bin acc 72.5 F1 66.7 AUROC 0.756 ECE 0.124; mc acc 36.0 mF1 16.7 ECE 0.176; ml EM 33.3 µF1 58.0 ECE 0.208 |
| tllm_judge_simple | 72 | 62.5 | bin acc 73.7 F1 78.3 AUROC 0.791 ECE 0.147; mc acc 75.0 mF1 68.5 ECE 0.183; ml EM 14.3 µF1 71.1 ECE 0.175 |
| tllm_judge_very_hard | 64 | 39.1 | bin acc 40.6 F1 42.4 AUROC 0.472 ECE 0.251; mc acc 57.1 mF1 38.6 ECE 0.136; ml EM 0.0 µF1 47.5 ECE 0.179 |
| tllm_score_hard | 62 | 45.2 | bin acc 55.9 F1 57.1 AUROC 0.465 ECE 0.327; mc acc 50.0 mF1 38.5 ECE 0.156; ml EM 8.3 µF1 47.8 ECE 0.204 |
| tllm_score_simple | 62 | 51.6 | bin acc 58.8 F1 72.0 AUROC 0.454 ECE 0.281; mc acc 62.5 mF1 47.6 ECE 0.218; ml EM 16.7 µF1 75.4 ECE 0.129 |
| tllm_score_very_hard | 76 | 35.5 | bin acc 47.4 F1 44.4 AUROC 0.684 ECE 0.252; mc acc 40.9 mF1 25.0 ECE 0.133; ml EM 0.0 µF1 38.9 ECE 0.211 |
| tllm_verify_hard | 50 | 34.0 | bin acc 42.3 F1 54.5 AUROC 0.388 ECE 0.333; mc acc 37.5 mF1 22.7 ECE 0.387; ml EM 0.0 µF1 63.4 ECE 0.132 |
| tllm_verify_simple | 60 | 40.0 | bin acc 60.6 F1 73.5 AUROC 0.516 ECE 0.182; mc acc 6.7 mF1 4.3 ECE 0.447; ml EM 25.0 µF1 77.6 ECE 0.164 |
| tllm_verify_very_hard | 55 | 40.0 | bin acc 51.6 F1 48.3 AUROC 0.530 ECE 0.266; mc acc 33.3 mF1 19.6 ECE 0.135; ml EM 11.1 µF1 45.7 ECE 0.286 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 265 | 55.8 |
| answer_trace_mismatch | 45 | 37.8 |
| benign_lookalike | 88 | 54.5 |
| confident_wrong | 39 | 35.9 |
| contradiction | 22 | 50.0 |
| distractor | 117 | 46.2 |
| double_negation | 3 | 33.3 |
| evidence_end | 11 | 72.7 |
| evidence_middle | 20 | 20.0 |
| evidence_start | 2 | 50.0 |
| exception | 20 | 45.0 |
| fake_authority | 1 | 100.0 |
| flawed_step | 44 | 43.2 |
| format_near_miss | 46 | 26.1 |
| gradual_escalation | 1 | 100.0 |
| hypothetical | 7 | 71.4 |
| indirect_injection | 25 | 36.0 |
| injection | 22 | 36.4 |
| judge_injection | 112 | 45.5 |
| length_bias | 7 | 0.0 |
| lexical_overlap | 103 | 43.7 |
| long_state | 74 | 39.2 |
| missing_evidence | 35 | 45.7 |
| multi_positive | 124 | 12.9 |
| multi_turn | 44 | 38.6 |
| negation | 62 | 41.9 |
| nota | 55 | 69.1 |
| numeric_reasoning | 109 | 40.4 |
| obfuscation | 1 | 0.0 |
| over_refusal | 50 | 44.0 |
| paraphrase | 73 | 57.5 |
| partial_compliance | 31 | 35.5 |
| role_reversal | 6 | 50.0 |
| sarcasm | 8 | 37.5 |
| speaker_confusion | 58 | 44.8 |
| subtle_violation | 16 | 18.8 |
| sycophancy | 13 | 30.8 |
| temporal_reasoning | 20 | 45.0 |
| tool_misuse | 6 | 16.7 |
| unsupported_claim | 96 | 34.4 |
| zero_positive | 55 | 49.1 |
| zero_positive_partial | 1 | 0.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 308 | 55.5 |
| 00128-00511 | 284 | 49.6 |
| 00512-02047 | 222 | 40.5 |
| 02048-08191 | 125 | 28.8 |
| 08192+ | 7 | 14.3 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 488 | 57.4 |
| 03 | 82 | 51.2 |
| 04 | 239 | 40.6 |
| 05 | 98 | 19.4 |
| 06 | 33 | 3.0 |
| 07 | 3 | 0.0 |
| 08 | 3 | 0.0 |

## Paraphrase groups

29 groups; same prediction 62.1%; all correct 44.8%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 52.5 |
| 0.4 | 72.1 | 48.7 |
| 0.5 | 48.9 | 42.2 |
| 0.6 | 31.5 | 34.5 |
| 0.7 | 19.2 | 30.2 |
| 0.8 | 13.0 | 30.6 |
| 0.9 | 8.7 | 25.0 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 13 | 0.050 | 0.077 |
| [0.1,0.2) | 28 | 0.155 | 0.179 |
| [0.2,0.3) | 41 | 0.258 | 0.415 |
| [0.3,0.4) | 46 | 0.341 | 0.457 |
| [0.4,0.5) | 43 | 0.455 | 0.558 |
| [0.5,0.6) | 63 | 0.548 | 0.540 |
| [0.6,0.7) | 77 | 0.657 | 0.468 |
| [0.7,0.8) | 77 | 0.752 | 0.610 |
| [0.8,0.9) | 70 | 0.842 | 0.586 |
| [0.9,1.0] | 30 | 0.979 | 0.633 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.2,0.3) | 13 | 0.275 | 0.231 |
| [0.3,0.4) | 64 | 0.352 | 0.406 |
| [0.4,0.5) | 64 | 0.450 | 0.375 |
| [0.5,0.6) | 48 | 0.549 | 0.438 |
| [0.6,0.7) | 34 | 0.649 | 0.588 |
| [0.7,0.8) | 17 | 0.742 | 0.706 |
| [0.8,0.9) | 12 | 0.852 | 0.583 |
| [0.9,1.0] | 24 | 0.952 | 0.750 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 35 | 0.070 | 0.029 |
| [0.1,0.2) | 74 | 0.153 | 0.270 |
| [0.2,0.3) | 99 | 0.254 | 0.333 |
| [0.3,0.4) | 100 | 0.351 | 0.480 |
| [0.4,0.5) | 122 | 0.456 | 0.508 |
| [0.5,0.6) | 125 | 0.548 | 0.472 |
| [0.6,0.7) | 107 | 0.657 | 0.617 |
| [0.7,0.8) | 81 | 0.749 | 0.679 |
| [0.8,0.9) | 79 | 0.846 | 0.722 |
| [0.9,1.0] | 42 | 0.951 | 0.643 |


Answered 946/946; errors 0; accuracy counting failures as wrong 46.4%.
Paired vs ours (images_v1/eval_llm): ours only right 457, laya only right 21, p = 6.2e-108
