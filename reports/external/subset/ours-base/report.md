# Evaluation report

- model `ours-base` @ `-`, adapter `None`, prompt `ours-base` (-)
- data reports/external/subset/subset.jsonl; splits ['test']; n=501; calibration `None`
- - / -; 2026-09-23T01:54:54-0700; wall 0.0s

## Overall

question accuracy 56.3%

![reliability](reliability.svg)

**binary**: n 174, positives 84, accuracy 0.546, precision 0.521, recall 0.726, f1 0.607, auroc 0.601, brier 0.412, log_loss 1.929, ece 0.411

**multiclass**: n 253, accuracy 0.723, macro_f1 0.620, log_loss 0.830, brier 0.411, ece_top_label 0.079

**multilabel**: n 74, labels 409, exact_match 0.054, micro_f1 0.517, macro_f1 0.384, label_auroc 0.713, brier 0.273, log_loss 1.177, ece 0.264

## By family

| family | n | question acc % | details |
|---|---|---|---|
| eval_adversarial | 27 | 74.1 | bin acc 73.3 F1 75.0 AUROC 0.741 ECE 0.351; mc acc 100.0 mF1 100.0 ECE 0.255; ml EM 40.0 µF1 75.0 ECE 0.251 |
| eval_agent_output | 26 | 30.8 | bin acc 42.9 F1 33.3 AUROC 0.510 ECE 0.454; mc acc 14.3 mF1 11.1 ECE 0.493; ml EM 20.0 µF1 57.1 ECE 0.286 |
| eval_evidence | 17 | 41.2 | bin acc 46.7 F1 55.6 AUROC 0.820 ECE 0.526; ml EM 0.0 µF1 54.5 ECE 0.467 |
| eval_multilabel | 32 | 12.5 | bin acc 57.1 F1 66.7 AUROC 0.750 ECE 0.486; mc acc 0.0 mF1 0.0 ECE 0.434; ml EM 0.0 µF1 55.1 ECE 0.358 |
| eval_policy | 22 | 31.8 | bin acc 46.2 F1 63.2 AUROC 0.548 ECE 0.536; mc acc 20.0 mF1 12.5 ECE 0.241; ml EM 0.0 µF1 69.6 ECE 0.465 |
| eval_routing | 25 | 48.0 | bin acc 60.0 F1 66.7 AUROC 0.875 ECE 0.382; mc acc 38.5 mF1 23.1 ECE 0.284; ml EM 50.0 µF1 50.0 ECE 0.209 |
| eval_urgency_sentiment | 22 | 40.9 | bin acc 60.0 F1 66.7 AUROC 0.417 ECE 0.421; mc acc 30.0 mF1 21.2 ECE 0.334; ml EM 0.0 µF1 66.7 ECE 0.477 |
| heldout_boolq | 30 | 66.7 | bin acc 66.7 F1 79.2 AUROC 0.651 ECE 0.364 |
| heldout_emotion_multiclass | 30 | 70.0 | mc acc 70.0 mF1 55.4 ECE 0.256 |
| heldout_intent_clinc | 30 | 96.7 | mc acc 96.7 mF1 95.4 ECE 0.086 |
| heldout_question_type_trec | 30 | 73.3 | mc acc 73.3 mF1 71.5 ECE 0.184 |
| heldout_sentiment_sst2 | 30 | 46.7 | bin acc 46.7 F1 0.0 AUROC 0.603 ECE 0.497 |
| heldout_topic_dbpedia | 30 | 90.0 | mc acc 90.0 mF1 72.1 ECE 0.077 |
| hf_emotions_multilabel | 30 | 0.0 | ml EM 0.0 µF1 0.0 ECE 0.179 |
| hf_intent_banking77 | 30 | 86.7 | mc acc 86.7 mF1 75.9 ECE 0.174 |
| hf_nli | 30 | 50.0 | bin acc 50.0 F1 61.5 AUROC 0.819 ECE 0.458 |
| hf_sentiment_tweets | 30 | 63.3 | mc acc 63.3 mF1 63.4 ECE 0.169 |
| hf_topic_agnews | 30 | 73.3 | mc acc 73.3 mF1 67.7 ECE 0.200 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 335 | 67.2 |
| contradiction | 20 | 10.0 |
| distractor | 33 | 21.2 |
| double_negation | 6 | 33.3 |
| evidence_end | 13 | 38.5 |
| evidence_middle | 11 | 45.5 |
| evidence_start | 9 | 55.6 |
| exception | 7 | 0.0 |
| hypothetical | 7 | 57.1 |
| injection | 10 | 60.0 |
| lexical_overlap | 20 | 40.0 |
| long_state | 50 | 36.0 |
| missing_evidence | 18 | 22.2 |
| multi_positive | 35 | 2.9 |
| multi_turn | 9 | 33.3 |
| negation | 30 | 33.3 |
| new_label_names | 3 | 0.0 |
| nota | 2 | 50.0 |
| numeric_reasoning | 16 | 37.5 |
| paraphrase | 22 | 18.2 |
| role_reversal | 15 | 40.0 |
| sarcasm | 12 | 8.3 |
| temporal_reasoning | 29 | 31.0 |
| zero_positive | 6 | 33.3 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 372 | 63.2 |
| 00128-00511 | 79 | 36.7 |
| 00512-02047 | 50 | 36.0 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 174 | 54.6 |
| 03 | 40 | 65.0 |
| 04 | 63 | 52.4 |
| 05 | 22 | 9.1 |
| 06 | 138 | 51.4 |
| 07 | 5 | 20.0 |
| 08 | 59 | 91.5 |

## Paraphrase groups

11 groups; same prediction 72.7%; all correct 18.2%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 27.7 |
| 0.4 | 84.2 | 21.1 |
| 0.5 | 70.4 | 18.0 |
| 0.6 | 60.9 | 16.2 |
| 0.7 | 53.8 | 14.0 |
| 0.8 | 44.3 | 8.9 |
| 0.9 | 34.8 | 3.4 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 44 | 0.021 | 0.432 |
| [0.1,0.2) | 2 | 0.131 | 0.500 |
| [0.2,0.3) | 3 | 0.246 | 0.333 |
| [0.3,0.4) | 2 | 0.352 | 0.000 |
| [0.4,0.5) | 6 | 0.452 | 0.333 |
| [0.5,0.6) | 2 | 0.502 | 0.500 |
| [0.6,0.7) | 6 | 0.668 | 0.167 |
| [0.7,0.8) | 4 | 0.774 | 0.500 |
| [0.8,0.9) | 4 | 0.859 | 1.000 |
| [0.9,1.0] | 101 | 0.983 | 0.525 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.2,0.3) | 5 | 0.269 | 0.200 |
| [0.3,0.4) | 35 | 0.353 | 0.400 |
| [0.4,0.5) | 35 | 0.440 | 0.629 |
| [0.5,0.6) | 24 | 0.545 | 0.708 |
| [0.6,0.7) | 18 | 0.638 | 0.667 |
| [0.7,0.8) | 24 | 0.746 | 0.625 |
| [0.8,0.9) | 24 | 0.843 | 0.708 |
| [0.9,1.0] | 88 | 0.975 | 0.966 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 242 | 0.014 | 0.190 |
| [0.1,0.2) | 8 | 0.125 | 0.250 |
| [0.2,0.3) | 8 | 0.256 | 0.125 |
| [0.3,0.4) | 4 | 0.346 | 0.250 |
| [0.4,0.5) | 4 | 0.429 | 0.500 |
| [0.5,0.6) | 6 | 0.532 | 0.167 |
| [0.6,0.7) | 8 | 0.649 | 0.375 |
| [0.7,0.8) | 6 | 0.752 | 0.667 |
| [0.8,0.9) | 17 | 0.874 | 0.353 |
| [0.9,1.0] | 106 | 0.970 | 0.509 |
