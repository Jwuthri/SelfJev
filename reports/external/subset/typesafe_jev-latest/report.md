# Evaluation report

- model `~typesafe/jev-latest` @ `-`, adapter `None`, prompt `~typesafe/jev-latest` (-)
- data reports/external/subset/subset.jsonl; splits ['test']; n=501; calibration `None`
- - / -; 2026-09-23T01:54:54-0700; wall 0.0s

## Overall

question accuracy 85.6%

![reliability](reliability.svg)

**binary**: n 174, positives 84, accuracy 0.920, precision 0.898, recall 0.940, f1 0.919, auroc 0.978, brier 0.056, log_loss 0.198, ece 0.056

**multiclass**: n 253, accuracy 0.854, macro_f1 0.828, log_loss 1.652, brier 0.236, ece_top_label 0.096

**multilabel**: n 74, labels 409, exact_match 0.716, micro_f1 0.876, macro_f1 0.900, label_auroc 0.974, brier 0.054, log_loss 0.193, ece 0.052

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
| heldout_boolq | 30 | 80.0 | bin acc 80.0 F1 84.2 AUROC 0.921 ECE 0.110 |
| heldout_emotion_multiclass | 30 | 66.7 | mc acc 66.7 mF1 51.7 ECE 0.244 |
| heldout_intent_clinc | 30 | 86.7 | mc acc 86.7 mF1 83.9 ECE 0.093 |
| heldout_question_type_trec | 30 | 100.0 | mc acc 100.0 mF1 100.0 ECE 0.012 |
| heldout_sentiment_sst2 | 30 | 100.0 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.144 |
| heldout_topic_dbpedia | 30 | 100.0 | mc acc 100.0 mF1 100.0 ECE 0.002 |
| hf_emotions_multilabel | 30 | 33.3 | ml EM 33.3 µF1 61.5 ECE 0.088 |
| hf_intent_banking77 | 30 | 93.3 | mc acc 93.3 mF1 85.7 ECE 0.052 |
| hf_nli | 30 | 86.7 | bin acc 86.7 F1 85.7 AUROC 1.000 ECE 0.139 |
| hf_sentiment_tweets | 30 | 60.0 | mc acc 60.0 mF1 61.0 ECE 0.304 |
| hf_topic_agnews | 30 | 83.3 | mc acc 83.3 mF1 82.0 ECE 0.177 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 335 | 82.7 |
| contradiction | 20 | 100.0 |
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
| missing_evidence | 18 | 77.8 |
| multi_positive | 35 | 91.4 |
| multi_turn | 9 | 100.0 |
| negation | 30 | 100.0 |
| new_label_names | 3 | 100.0 |
| nota | 2 | 100.0 |
| numeric_reasoning | 16 | 93.8 |
| paraphrase | 22 | 100.0 |
| role_reversal | 15 | 100.0 |
| sarcasm | 12 | 100.0 |
| temporal_reasoning | 29 | 79.3 |
| zero_positive | 6 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 372 | 83.3 |
| 00128-00511 | 79 | 93.7 |
| 00512-02047 | 50 | 90.0 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 174 | 92.0 |
| 03 | 40 | 70.0 |
| 04 | 63 | 87.3 |
| 05 | 22 | 90.9 |
| 06 | 138 | 78.3 |
| 07 | 5 | 100.0 |
| 08 | 59 | 89.8 |

## Paraphrase groups

11 groups; same prediction 81.8%; all correct 100.0%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 14.6 |
| 0.4 | 100.0 | 14.6 |
| 0.5 | 99.6 | 14.3 |
| 0.6 | 96.8 | 12.7 |
| 0.7 | 92.5 | 11.5 |
| 0.8 | 90.1 | 10.5 |
| 0.9 | 85.8 | 8.3 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 60 | 0.050 | 0.017 |
| [0.1,0.2) | 16 | 0.129 | 0.062 |
| [0.2,0.3) | 3 | 0.237 | 0.000 |
| [0.3,0.4) | 4 | 0.340 | 0.500 |
| [0.4,0.5) | 3 | 0.453 | 0.333 |
| [0.5,0.6) | 6 | 0.562 | 0.500 |
| [0.6,0.7) | 4 | 0.660 | 0.750 |
| [0.7,0.8) | 7 | 0.734 | 0.429 |
| [0.8,0.9) | 6 | 0.850 | 1.000 |
| [0.9,1.0] | 65 | 0.967 | 0.985 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.4,0.5) | 1 | 0.460 | 0.000 |
| [0.5,0.6) | 7 | 0.546 | 0.286 |
| [0.6,0.7) | 11 | 0.638 | 0.636 |
| [0.7,0.8) | 6 | 0.735 | 0.500 |
| [0.8,0.9) | 11 | 0.836 | 0.455 |
| [0.9,1.0] | 217 | 0.993 | 0.917 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 209 | 0.044 | 0.010 |
| [0.1,0.2) | 43 | 0.125 | 0.047 |
| [0.2,0.3) | 17 | 0.236 | 0.176 |
| [0.3,0.4) | 8 | 0.330 | 0.375 |
| [0.4,0.5) | 1 | 0.410 | 0.000 |
| [0.5,0.6) | 6 | 0.537 | 0.500 |
| [0.6,0.7) | 10 | 0.643 | 0.300 |
| [0.7,0.8) | 8 | 0.742 | 0.500 |
| [0.8,0.9) | 7 | 0.856 | 0.429 |
| [0.9,1.0] | 100 | 0.971 | 0.970 |
