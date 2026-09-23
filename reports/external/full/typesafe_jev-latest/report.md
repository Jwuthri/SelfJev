# Evaluation report

- model `~typesafe/jev-latest` @ `-`, adapter `None`, prompt `~typesafe/jev-latest` (-)
- data reports/external/full/subset.jsonl; splits ['test']; n=3471; calibration `None`
- - / -; 2026-09-23T09:40:46-0700; wall 0.0s

## Overall

question accuracy 82.7%

![reliability](reliability.svg)

**binary**: n 984, positives 475, accuracy 0.935, precision 0.942, recall 0.922, f1 0.932, auroc 0.981, brier 0.051, log_loss 0.191, ece 0.045

**multiclass**: n 2143, accuracy 0.846, macro_f1 0.916, log_loss 2.134, brier 0.258, ece_top_label 0.099

**multilabel**: n 344, labels 2029, exact_match 0.401, micro_f1 0.663, macro_f1 0.883, label_auroc 0.890, brier 0.112, log_loss 0.359, ece 0.066

## By family

| family | n | question acc % | details |
|---|---|---|---|
| eval_adversarial | 27 | 100.0 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.048; mc acc 100.0 mF1 100.0 ECE 0.027; ml EM 100.0 µF1 100.0 ECE 0.036 |
| eval_agent_output | 26 | 92.3 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.045; mc acc 85.7 mF1 76.0 ECE 0.089; ml EM 80.0 µF1 94.1 ECE 0.094 |
| eval_evidence | 17 | 100.0 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.047; ml EM 100.0 µF1 100.0 ECE 0.048 |
| eval_multilabel | 32 | 100.0 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.084; mc acc 100.0 mF1 100.0 ECE 0.000; ml EM 100.0 µF1 100.0 ECE 0.040 |
| eval_policy | 22 | 72.7 | bin acc 76.9 F1 76.9 AUROC 0.857 ECE 0.316; mc acc 40.0 mF1 25.0 ECE 0.458; ml EM 100.0 µF1 100.0 ECE 0.139 |
| eval_routing | 25 | 100.0 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.042; mc acc 100.0 mF1 100.0 ECE 0.000; ml EM 100.0 µF1 100.0 ECE 0.093 |
| eval_urgency_sentiment | 22 | 95.5 | bin acc 90.0 F1 90.9 AUROC 1.000 ECE 0.095; mc acc 100.0 mF1 100.0 ECE 0.004; ml EM 100.0 µF1 100.0 ECE 0.029 |
| heldout_boolq | 300 | 90.7 | bin acc 90.7 F1 91.9 AUROC 0.965 ECE 0.038 |
| heldout_emotion_multiclass | 300 | 57.7 | mc acc 57.7 mF1 47.2 ECE 0.301 |
| heldout_intent_clinc | 300 | 94.3 | mc acc 94.3 mF1 95.4 ECE 0.026 |
| heldout_question_type_trec | 300 | 94.0 | mc acc 94.0 mF1 91.5 ECE 0.035 |
| heldout_sentiment_sst2 | 300 | 96.7 | bin acc 96.7 F1 96.6 AUROC 0.994 ECE 0.097 |
| heldout_topic_dbpedia | 300 | 98.0 | mc acc 98.0 mF1 97.8 ECE 0.012 |
| hf_emotions_multilabel | 300 | 31.7 | ml EM 31.7 µF1 58.8 ECE 0.071 |
| hf_intent_banking77 | 300 | 95.7 | mc acc 95.7 mF1 95.0 ECE 0.023 |
| hf_nli | 300 | 92.7 | bin acc 92.7 F1 90.4 AUROC 0.985 ECE 0.072 |
| hf_sentiment_tweets | 300 | 64.3 | mc acc 64.3 mF1 64.6 ECE 0.242 |
| hf_topic_agnews | 300 | 87.3 | mc acc 87.3 mF1 87.0 ECE 0.106 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 3042 | 82.2 |
| contradiction | 107 | 100.0 |
| distractor | 33 | 93.9 |
| double_negation | 6 | 83.3 |
| evidence_end | 13 | 84.6 |
| evidence_middle | 11 | 81.8 |
| evidence_start | 9 | 100.0 |
| exception | 7 | 71.4 |
| hypothetical | 7 | 100.0 |
| injection | 10 | 100.0 |
| lexical_overlap | 20 | 100.0 |
| long_state | 50 | 90.0 |
| missing_evidence | 104 | 84.6 |
| multi_positive | 81 | 56.8 |
| multi_turn | 9 | 100.0 |
| negation | 30 | 100.0 |
| new_label_names | 3 | 100.0 |
| nota | 46 | 100.0 |
| numeric_reasoning | 16 | 93.8 |
| paraphrase | 22 | 100.0 |
| role_reversal | 15 | 100.0 |
| sarcasm | 12 | 100.0 |
| temporal_reasoning | 29 | 79.3 |
| zero_positive | 6 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 3211 | 82.0 |
| 00128-00511 | 208 | 92.3 |
| 00512-02047 | 52 | 90.4 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 984 | 93.5 |
| 03 | 310 | 65.5 |
| 04 | 333 | 87.7 |
| 05 | 22 | 90.9 |
| 06 | 1218 | 70.8 |
| 07 | 49 | 100.0 |
| 08 | 555 | 94.6 |

## Paraphrase groups

11 groups; same prediction 81.8%; all correct 100.0%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 15.4 |
| 0.4 | 99.8 | 15.2 |
| 0.5 | 99.2 | 15.0 |
| 0.6 | 96.5 | 14.2 |
| 0.7 | 92.2 | 12.6 |
| 0.8 | 88.2 | 11.2 |
| 0.9 | 83.6 | 9.8 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 336 | 0.046 | 0.015 |
| [0.1,0.2) | 95 | 0.137 | 0.063 |
| [0.2,0.3) | 41 | 0.247 | 0.244 |
| [0.3,0.4) | 27 | 0.346 | 0.222 |
| [0.4,0.5) | 20 | 0.443 | 0.500 |
| [0.5,0.6) | 18 | 0.553 | 0.556 |
| [0.6,0.7) | 20 | 0.653 | 0.750 |
| [0.7,0.8) | 47 | 0.739 | 0.766 |
| [0.8,0.9) | 64 | 0.845 | 0.984 |
| [0.9,1.0] | 316 | 0.961 | 0.994 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.3,0.4) | 5 | 0.364 | 0.200 |
| [0.4,0.5) | 12 | 0.459 | 0.417 |
| [0.5,0.6) | 57 | 0.548 | 0.544 |
| [0.6,0.7) | 93 | 0.649 | 0.516 |
| [0.7,0.8) | 86 | 0.744 | 0.570 |
| [0.8,0.9) | 98 | 0.847 | 0.633 |
| [0.9,1.0] | 1792 | 0.993 | 0.902 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 989 | 0.045 | 0.034 |
| [0.1,0.2) | 277 | 0.137 | 0.123 |
| [0.2,0.3) | 130 | 0.240 | 0.154 |
| [0.3,0.4) | 83 | 0.345 | 0.253 |
| [0.4,0.5) | 58 | 0.444 | 0.379 |
| [0.5,0.6) | 61 | 0.542 | 0.311 |
| [0.6,0.7) | 55 | 0.645 | 0.491 |
| [0.7,0.8) | 61 | 0.752 | 0.475 |
| [0.8,0.9) | 92 | 0.846 | 0.489 |
| [0.9,1.0] | 223 | 0.959 | 0.848 |
