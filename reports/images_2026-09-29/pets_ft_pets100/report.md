# Evaluation report

- model `Qwen/Qwen3.5-4B` @ `851bf6e806` (shared-prefix tree, forward only: text once per request, each question once, then each candidate), adapter/checkpoint `runs/pets_ft/adapter`, prompt `challenger-state-first-v1` (6c9d8459ac44)
- data data/ova/eval_pets100.jsonl; splits ['test']; n=100; calibration `None`
- cuda / bfloat16; 2026-09-30T03:21:24+0000; wall 16.4s

## Overall

question accuracy 90.0%

![reliability](reliability.svg)

**binary**: n 21, positives 10, accuracy 1.000, precision 1.000, recall 1.000, f1 1.000, auroc 1.000, brier 0.000, log_loss 0.004, ece 0.004

**multiclass**: n 79, accuracy 0.873, macro_f1 0.724, log_loss 0.438, brier 0.216, ece_top_label 0.085

## By family

| family | n | question acc % | details |
|---|---|---|---|
| pets_breed37 | 18 | 83.3 | mc acc 83.3 mF1 68.6 ECE 0.132 |
| pets_cat_breed | 61 | 88.5 | mc acc 88.5 mF1 88.4 ECE 0.124 |
| pets_is_cat | 21 | 100.0 | bin acc 100.0 F1 100.0 AUROC 1.000 ECE 0.004 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 100 | 90.0 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 100 | 90.0 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 21 | 100.0 |
| 12 | 61 | 88.5 |
| 37 | 18 | 83.3 |

## Paraphrase groups

0 groups; same prediction —%; all correct —%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 12.7 |
| 0.4 | 97.5 | 11.7 |
| 0.5 | 96.2 | 11.8 |
| 0.6 | 92.4 | 11.0 |
| 0.7 | 88.6 | 8.6 |
| 0.8 | 82.3 | 7.7 |
| 0.9 | 79.7 | 7.9 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 11 | 0.006 | 0.000 |
| [0.9,1.0] | 10 | 0.998 | 1.000 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.3,0.4) | 2 | 0.386 | 0.500 |
| [0.4,0.5) | 1 | 0.406 | 1.000 |
| [0.5,0.6) | 3 | 0.542 | 0.667 |
| [0.6,0.7) | 3 | 0.672 | 0.333 |
| [0.7,0.8) | 5 | 0.739 | 0.800 |
| [0.8,0.9) | 2 | 0.832 | 1.000 |
| [0.9,1.0] | 63 | 0.982 | 0.921 |
