# Evaluation report

- model `ours-LoRA` @ `-`, adapter `None`, prompt `ours-LoRA` (-)
- data reports/external/full/subset.jsonl; splits ['test']; n=3471; calibration `None`
- - / -; 2026-09-23T09:40:46-0700; wall 0.0s

## Overall

question accuracy 73.5%

![reliability](reliability.svg)

**binary**: n 984, positives 475, accuracy 0.778, precision 0.820, recall 0.693, f1 0.751, auroc 0.863, brier 0.155, log_loss 0.480, ece 0.066

**multiclass**: n 2143, accuracy 0.783, macro_f1 0.823, log_loss 0.601, brier 0.301, ece_top_label 0.027

**multilabel**: n 344, labels 2029, exact_match 0.311, micro_f1 0.629, macro_f1 0.545, label_auroc 0.882, brier 0.113, log_loss 0.359, ece 0.052

## By family

| family | n | question acc % | details |
|---|---|---|---|
| eval_adversarial | 27 | 63.0 | bin acc 66.7 F1 66.7 AUROC 0.796 ECE 0.276; mc acc 85.7 mF1 77.8 ECE 0.127; ml EM 20.0 µF1 72.7 ECE 0.256 |
| eval_agent_output | 26 | 46.2 | bin acc 57.1 F1 57.1 AUROC 0.592 ECE 0.355; mc acc 57.1 mF1 38.1 ECE 0.438; ml EM 0.0 µF1 66.7 ECE 0.239 |
| eval_evidence | 17 | 82.4 | bin acc 93.3 F1 90.9 AUROC 0.980 ECE 0.147; ml EM 0.0 µF1 40.0 ECE 0.464 |
| eval_multilabel | 32 | 34.4 | bin acc 57.1 F1 57.1 AUROC 0.750 ECE 0.345; mc acc 0.0 mF1 0.0 ECE 0.496; ml EM 29.2 µF1 75.9 ECE 0.138 |
| eval_policy | 22 | 40.9 | bin acc 46.2 F1 46.2 AUROC 0.429 ECE 0.500; mc acc 40.0 mF1 23.8 ECE 0.521; ml EM 25.0 µF1 66.7 ECE 0.386 |
| eval_routing | 25 | 76.0 | bin acc 80.0 F1 75.0 AUROC 0.917 ECE 0.189; mc acc 76.9 mF1 66.7 ECE 0.162; ml EM 50.0 µF1 80.0 ECE 0.114 |
| eval_urgency_sentiment | 22 | 54.5 | bin acc 80.0 F1 80.0 AUROC 0.917 ECE 0.205; mc acc 40.0 mF1 23.0 ECE 0.250; ml EM 0.0 µF1 83.3 ECE 0.160 |
| heldout_boolq | 300 | 70.3 | bin acc 70.3 F1 73.7 AUROC 0.768 ECE 0.103 |
| heldout_emotion_multiclass | 300 | 56.0 | mc acc 56.0 mF1 47.3 ECE 0.063 |
| heldout_intent_clinc | 300 | 89.3 | mc acc 89.3 mF1 90.8 ECE 0.034 |
| heldout_question_type_trec | 300 | 68.0 | mc acc 68.0 mF1 68.1 ECE 0.066 |
| heldout_sentiment_sst2 | 300 | 76.7 | bin acc 76.7 F1 69.8 AUROC 0.935 ECE 0.189 |
| heldout_topic_dbpedia | 300 | 91.7 | mc acc 91.7 mF1 91.5 ECE 0.040 |
| hf_emotions_multilabel | 300 | 32.3 | ml EM 32.3 µF1 60.1 ECE 0.041 |
| hf_intent_banking77 | 300 | 92.7 | mc acc 92.7 mF1 90.3 ECE 0.027 |
| hf_nli | 300 | 89.0 | bin acc 89.0 F1 85.5 AUROC 0.946 ECE 0.040 |
| hf_sentiment_tweets | 300 | 66.7 | mc acc 66.7 mF1 66.6 ECE 0.058 |
| hf_topic_agnews | 300 | 86.7 | mc acc 86.7 mF1 86.8 ECE 0.063 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 3042 | 74.2 |
| contradiction | 107 | 90.7 |
| distractor | 33 | 45.5 |
| double_negation | 6 | 33.3 |
| evidence_end | 13 | 46.2 |
| evidence_middle | 11 | 54.5 |
| evidence_start | 9 | 77.8 |
| exception | 7 | 0.0 |
| hypothetical | 7 | 57.1 |
| injection | 10 | 50.0 |
| lexical_overlap | 20 | 55.0 |
| long_state | 50 | 46.0 |
| missing_evidence | 104 | 81.7 |
| multi_positive | 81 | 18.5 |
| multi_turn | 9 | 77.8 |
| negation | 30 | 56.7 |
| new_label_names | 3 | 100.0 |
| nota | 46 | 89.1 |
| numeric_reasoning | 16 | 37.5 |
| paraphrase | 22 | 50.0 |
| role_reversal | 15 | 46.7 |
| sarcasm | 12 | 33.3 |
| temporal_reasoning | 29 | 37.9 |
| zero_positive | 6 | 33.3 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 3211 | 74.6 |
| 00128-00511 | 208 | 63.5 |
| 00512-02047 | 52 | 48.1 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 984 | 77.8 |
| 03 | 310 | 66.8 |
| 04 | 333 | 83.2 |
| 05 | 22 | 31.8 |
| 06 | 1218 | 61.3 |
| 07 | 49 | 87.8 |
| 08 | 555 | 91.0 |

## Paraphrase groups

11 groups; same prediction 45.5%; all correct 36.4%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 21.7 |
| 0.4 | 96.4 | 20.2 |
| 0.5 | 90.6 | 17.9 |
| 0.6 | 79.7 | 13.0 |
| 0.7 | 68.8 | 9.4 |
| 0.8 | 58.1 | 5.5 |
| 0.9 | 45.4 | 3.6 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 222 | 0.045 | 0.090 |
| [0.1,0.2) | 145 | 0.148 | 0.152 |
| [0.2,0.3) | 94 | 0.249 | 0.415 |
| [0.3,0.4) | 56 | 0.346 | 0.464 |
| [0.4,0.5) | 66 | 0.445 | 0.591 |
| [0.5,0.6) | 48 | 0.555 | 0.729 |
| [0.6,0.7) | 61 | 0.654 | 0.721 |
| [0.7,0.8) | 54 | 0.749 | 0.685 |
| [0.8,0.9) | 84 | 0.852 | 0.857 |
| [0.9,1.0] | 154 | 0.953 | 0.916 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.2,0.3) | 10 | 0.274 | 0.400 |
| [0.3,0.4) | 67 | 0.350 | 0.403 |
| [0.4,0.5) | 124 | 0.461 | 0.427 |
| [0.5,0.6) | 235 | 0.553 | 0.468 |
| [0.6,0.7) | 232 | 0.648 | 0.638 |
| [0.7,0.8) | 229 | 0.750 | 0.694 |
| [0.8,0.9) | 273 | 0.854 | 0.879 |
| [0.9,1.0] | 973 | 0.972 | 0.964 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 907 | 0.032 | 0.025 |
| [0.1,0.2) | 265 | 0.141 | 0.068 |
| [0.2,0.3) | 165 | 0.248 | 0.188 |
| [0.3,0.4) | 112 | 0.348 | 0.277 |
| [0.4,0.5) | 110 | 0.455 | 0.464 |
| [0.5,0.6) | 138 | 0.548 | 0.500 |
| [0.6,0.7) | 78 | 0.652 | 0.487 |
| [0.7,0.8) | 70 | 0.751 | 0.586 |
| [0.8,0.9) | 65 | 0.851 | 0.677 |
| [0.9,1.0] | 119 | 0.948 | 0.790 |
