# Evaluation report

- model `/home/ubuntu/ckpt/selfjev-4b-vision-4bit` @ `851bf6e806` (shared-prefix tree, forward only: text once per request, each question once, then each candidate), adapter/checkpoint `None`, prompt `challenger-state-first-v1` (6c9d8459ac44)
- data data/compact_challenge_v1.jsonl; splits ['test']; n=720; calibration `None`
- cuda / bfloat16; 2026-10-01T08:09:34+0000; wall 31.9s

## Overall

question accuracy 100.0%

![reliability](reliability.svg)

**binary**: n 360, positives 122, accuracy 1.000, precision 1.000, recall 1.000, f1 1.000, auroc 1.000, brier 0.002, log_loss 0.037, ece 0.036

**multiclass**: n 240, accuracy 1.000, macro_f1 1.000, log_loss 0.020, brier 0.002, ece_top_label 0.019

**multilabel**: n 120, labels 360, exact_match 1.000, micro_f1 1.000, macro_f1 1.000, label_auroc 1.000, brier 0.000, log_loss 0.015, ece 0.014

## By family

| family | n | question acc % | details |
|---|---|---|---|
| compact_fresh_rules | 720 | 100.0 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.036; mc acc 100.0 mF1 100.0 ECE 0.019; ml EM 100.0 µF1 100.0 ECE 0.014 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 240 | 100.0 |
| conditional_policy | 120 | 100.0 |
| missing_evidence | 120 | 100.0 |
| negation | 120 | 100.0 |
| none_of_the_above | 120 | 100.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 720 | 100.0 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 360 | 100.0 |
| 03 | 360 | 100.0 |

## Paraphrase groups

0 groups; same prediction —%; all correct —%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 0.0 |
| 0.4 | 100.0 | 0.0 |
| 0.5 | 100.0 | 0.0 |
| 0.6 | 100.0 | 0.0 |
| 0.7 | 100.0 | 0.0 |
| 0.8 | 100.0 | 0.0 |
| 0.9 | 96.7 | 0.0 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 238 | 0.032 | 0.000 |
| [0.6,0.7) | 1 | 0.672 | 1.000 |
| [0.8,0.9) | 7 | 0.846 | 1.000 |
| [0.9,1.0] | 114 | 0.966 | 1.000 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.8,0.9) | 8 | 0.893 | 1.000 |
| [0.9,1.0] | 232 | 0.984 | 1.000 |

## Reliability: multilabel

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 203 | 0.012 | 0.000 |
| [0.9,1.0] | 157 | 0.982 | 1.000 |
