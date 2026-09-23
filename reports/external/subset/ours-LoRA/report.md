# Evaluation report

- model `ours-LoRA` @ `-`, adapter `None`, prompt `ours-LoRA` (-)
- data reports/external/subset/subset.jsonl; splits ['test']; n=501; calibration `None`
- - / -; 2026-09-23T01:54:54-0700; wall 0.0s

## Overall

question accuracy 69.9%

![reliability](reliability.svg)

**binary**: n 174, positives 84, accuracy 0.730, precision 0.718, recall 0.726, f1 0.722, auroc 0.816, brier 0.179, log_loss 0.549, ece 0.125

**multiclass**: n 253, accuracy 0.787, macro_f1 0.698, log_loss 0.628, brier 0.315, ece_top_label 0.035

**multilabel**: n 74, labels 409, exact_match 0.324, micro_f1 0.714, macro_f1 0.552, label_auroc 0.888, brier 0.137, log_loss 0.444, ece 0.099

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
| heldout_boolq | 30 | 56.7 | bin acc 56.7 F1 66.7 AUROC 0.713 ECE 0.238 |
| heldout_emotion_multiclass | 30 | 73.3 | mc acc 73.3 mF1 61.3 ECE 0.116 |
| heldout_intent_clinc | 30 | 93.3 | mc acc 93.3 mF1 91.4 ECE 0.114 |
| heldout_question_type_trec | 30 | 80.0 | mc acc 80.0 mF1 82.1 ECE 0.202 |
| heldout_sentiment_sst2 | 30 | 83.3 | bin acc 83.3 F1 81.5 AUROC 0.996 ECE 0.259 |
| heldout_topic_dbpedia | 30 | 93.3 | mc acc 93.3 mF1 93.1 ECE 0.070 |
| hf_emotions_multilabel | 30 | 46.7 | ml EM 46.7 µF1 67.7 ECE 0.064 |
| hf_intent_banking77 | 30 | 86.7 | mc acc 86.7 mF1 73.3 ECE 0.106 |
| hf_nli | 30 | 90.0 | bin acc 90.0 F1 88.0 AUROC 0.958 ECE 0.145 |
| hf_sentiment_tweets | 30 | 73.3 | mc acc 73.3 mF1 75.6 ECE 0.109 |
| hf_topic_agnews | 30 | 76.7 | mc acc 76.7 mF1 77.2 ECE 0.172 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 335 | 77.6 |
| contradiction | 20 | 70.0 |
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
| missing_evidence | 18 | 77.8 |
| multi_positive | 35 | 11.4 |
| multi_turn | 9 | 77.8 |
| negation | 30 | 56.7 |
| new_label_names | 3 | 100.0 |
| nota | 2 | 50.0 |
| numeric_reasoning | 16 | 37.5 |
| paraphrase | 22 | 50.0 |
| role_reversal | 15 | 46.7 |
| sarcasm | 12 | 33.3 |
| temporal_reasoning | 29 | 37.9 |
| zero_positive | 6 | 33.3 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 372 | 77.2 |
| 00128-00511 | 79 | 50.6 |
| 00512-02047 | 50 | 46.0 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 174 | 73.0 |
| 03 | 40 | 72.5 |
| 04 | 63 | 63.5 |
| 05 | 22 | 31.8 |
| 06 | 138 | 65.9 |
| 07 | 5 | 60.0 |
| 08 | 59 | 89.8 |

## Paraphrase groups

11 groups; same prediction 45.5%; all correct 36.4%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 21.3 |
| 0.4 | 96.0 | 19.3 |
| 0.5 | 87.7 | 16.2 |
| 0.6 | 75.9 | 12.0 |
| 0.7 | 70.0 | 10.7 |
| 0.8 | 57.7 | 7.5 |
| 0.9 | 41.1 | 6.7 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 34 | 0.054 | 0.118 |
| [0.1,0.2) | 14 | 0.149 | 0.000 |
| [0.2,0.3) | 17 | 0.252 | 0.294 |
| [0.3,0.4) | 9 | 0.348 | 0.333 |
| [0.4,0.5) | 15 | 0.437 | 0.733 |
| [0.5,0.6) | 12 | 0.553 | 0.750 |
| [0.6,0.7) | 13 | 0.661 | 0.615 |
| [0.7,0.8) | 11 | 0.735 | 0.364 |
| [0.8,0.9) | 15 | 0.848 | 0.733 |
| [0.9,1.0] | 34 | 0.955 | 0.853 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.3,0.4) | 10 | 0.356 | 0.300 |
| [0.4,0.5) | 21 | 0.466 | 0.476 |
| [0.5,0.6) | 30 | 0.552 | 0.567 |
| [0.6,0.7) | 15 | 0.648 | 0.733 |
| [0.7,0.8) | 31 | 0.753 | 0.742 |
| [0.8,0.9) | 42 | 0.847 | 0.905 |
| [0.9,1.0] | 104 | 0.968 | 0.933 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 133 | 0.037 | 0.015 |
| [0.1,0.2) | 49 | 0.144 | 0.061 |
| [0.2,0.3) | 37 | 0.250 | 0.162 |
| [0.3,0.4) | 27 | 0.347 | 0.222 |
| [0.4,0.5) | 17 | 0.454 | 0.471 |
| [0.5,0.6) | 19 | 0.546 | 0.474 |
| [0.6,0.7) | 11 | 0.649 | 0.455 |
| [0.7,0.8) | 19 | 0.754 | 0.526 |
| [0.8,0.9) | 27 | 0.852 | 0.704 |
| [0.9,1.0] | 70 | 0.956 | 0.743 |
