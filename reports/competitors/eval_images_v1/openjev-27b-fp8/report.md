# Evaluation report

- model `openjev-27b-fp8` @ `-` (external open model via /v1/systemone), adapter/checkpoint `None`, prompt `jev-request` (-)
- data data/eval_images_v1.jsonl; splits ['test']; n=2002; calibration `None`
- cuda / -; 2026-09-30T20:55:58+0000; wall 223.3s

## Overall

question accuracy 76.6%

![reliability](reliability.svg)

**binary**: n 951, positives 508, accuracy 0.831, precision 0.868, recall 0.805, f1 0.836, auroc 0.932, brier 0.110, log_loss 0.339, ece 0.066

**multiclass**: n 1051, accuracy 0.707, macro_f1 0.887, log_loss 0.720, brier 0.379, ece_top_label 0.072

## By family

| family | n | question acc % | details |
|---|---|---|---|
| img_beans | 204 | 71.1 | bin acc 75.5 F1 78.3 AUROC 0.841 ECE 0.100; mc acc 66.7 mF1 67.5 ECE 0.087 |
| img_eurosat | 200 | 62.5 | bin acc 75.0 F1 71.3 AUROC 0.844 ECE 0.150; mc acc 50.0 mF1 45.2 ECE 0.157 |
| img_fashion | 200 | 76.0 | bin acc 82.0 F1 79.5 AUROC 0.948 ECE 0.123; mc acc 70.0 mF1 69.1 ECE 0.079 |
| img_hurricane | 100 | 55.0 | mc acc 55.0 mF1 54.2 ECE 0.245 |
| img_indoor | 268 | 95.9 | bin acc 96.3 F1 96.2 AUROC 0.995 ECE 0.056; mc acc 95.5 mF1 95.3 ECE 0.035 |
| img_painting | 204 | 69.6 | bin acc 80.4 F1 78.7 AUROC 0.916 ECE 0.138; mc acc 58.8 mF1 57.5 ECE 0.124 |
| img_pets | 222 | 96.4 | bin acc 96.4 F1 97.3 AUROC 0.980 ECE 0.114; mc acc 96.4 mF1 96.1 ECE 0.042 |
| img_rice | 200 | 45.0 | bin acc 54.0 F1 45.2 AUROC 0.631 ECE 0.094; mc acc 36.0 mF1 22.1 ECE 0.104 |
| img_snacks | 200 | 92.0 | bin acc 95.0 F1 95.7 AUROC 0.996 ECE 0.091; mc acc 89.0 mF1 89.0 ECE 0.038 |
| img_trash | 204 | 82.8 | bin acc 87.3 F1 88.9 AUROC 0.965 ECE 0.063; mc acc 78.4 mF1 73.4 ECE 0.142 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 2002 | 76.6 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 2002 | 76.6 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 951 | 83.1 |
| 02 | 100 | 55.0 |
| 03 | 102 | 66.7 |
| 05 | 100 | 36.0 |
| 06 | 102 | 78.4 |
| 10 | 200 | 60.0 |
| 12 | 447 | 85.9 |

## Paraphrase groups

0 groups; same prediction —%; all correct —%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 29.3 |
| 0.4 | 92.0 | 25.5 |
| 0.5 | 82.8 | 20.6 |
| 0.6 | 72.9 | 16.7 |
| 0.7 | 65.2 | 13.3 |
| 0.8 | 57.8 | 10.9 |
| 0.9 | 45.6 | 5.4 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 267 | 0.031 | 0.015 |
| [0.1,0.2) | 44 | 0.146 | 0.205 |
| [0.2,0.3) | 40 | 0.249 | 0.425 |
| [0.3,0.4) | 65 | 0.349 | 0.400 |
| [0.4,0.5) | 64 | 0.433 | 0.672 |
| [0.5,0.6) | 75 | 0.554 | 0.680 |
| [0.6,0.7) | 51 | 0.658 | 0.647 |
| [0.7,0.8) | 77 | 0.752 | 0.870 |
| [0.8,0.9) | 94 | 0.852 | 0.926 |
| [0.9,1.0] | 174 | 0.955 | 0.983 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.1,0.2) | 2 | 0.172 | 0.000 |
| [0.2,0.3) | 15 | 0.267 | 0.267 |
| [0.3,0.4) | 67 | 0.349 | 0.284 |
| [0.4,0.5) | 97 | 0.454 | 0.299 |
| [0.5,0.6) | 104 | 0.547 | 0.510 |
| [0.6,0.7) | 81 | 0.643 | 0.543 |
| [0.7,0.8) | 78 | 0.757 | 0.679 |
| [0.8,0.9) | 128 | 0.854 | 0.688 |
| [0.9,1.0] | 479 | 0.980 | 0.946 |


Answered 2002/2002; errors 0; accuracy counting failures as wrong 76.6%.
Paired vs ours (images_v1/images_v1_images): ours only right 335, openjev-27b-fp8 only right 58, p = 1.8e-48
