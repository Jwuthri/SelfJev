# Evaluation report

- model `imajev-4b` @ `-` (external open model via /v1/systemone), adapter/checkpoint `None`, prompt `jev-request` (-)
- data data/eval_images_v1.jsonl; splits ['test']; n=2002; calibration `None`
- cuda / -; 2026-09-30T19:22:38+0000; wall 108.8s

## Overall

question accuracy 75.9%

![reliability](reliability.svg)

**binary**: n 951, positives 508, accuracy 0.838, precision 0.861, recall 0.831, f1 0.846, auroc 0.929, brier 0.108, log_loss 0.341, ece 0.044

**multiclass**: n 1051, accuracy 0.688, macro_f1 0.881, log_loss 0.834, brier 0.411, ece_top_label 0.051

## By family

| family | n | question acc % | details |
|---|---|---|---|
| img_beans | 204 | 73.0 | bin acc 75.5 F1 79.3 AUROC 0.873 ECE 0.119; mc acc 70.6 mF1 70.8 ECE 0.080 |
| img_eurosat | 200 | 61.0 | bin acc 79.0 F1 76.9 AUROC 0.862 ECE 0.100; mc acc 43.0 mF1 39.1 ECE 0.152 |
| img_fashion | 200 | 74.0 | bin acc 89.0 F1 88.9 AUROC 0.952 ECE 0.086; mc acc 59.0 mF1 54.1 ECE 0.174 |
| img_hurricane | 100 | 67.0 | mc acc 67.0 mF1 66.2 ECE 0.135 |
| img_indoor | 268 | 97.4 | bin acc 97.8 F1 97.7 AUROC 0.997 ECE 0.075; mc acc 97.0 mF1 96.9 ECE 0.052 |
| img_painting | 204 | 69.1 | bin acc 82.4 F1 82.0 AUROC 0.918 ECE 0.096; mc acc 55.9 mF1 52.5 ECE 0.166 |
| img_pets | 222 | 91.9 | bin acc 91.0 F1 93.2 AUROC 0.965 ECE 0.075; mc acc 92.8 mF1 91.8 ECE 0.042 |
| img_rice | 200 | 37.0 | bin acc 50.0 F1 35.9 AUROC 0.566 ECE 0.156; mc acc 24.0 mF1 14.1 ECE 0.149 |
| img_snacks | 200 | 94.5 | bin acc 95.0 F1 95.7 AUROC 0.995 ECE 0.088; mc acc 94.0 mF1 93.8 ECE 0.062 |
| img_trash | 204 | 80.9 | bin acc 89.2 F1 90.3 AUROC 0.950 ECE 0.069; mc acc 72.5 mF1 67.0 ECE 0.150 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 2002 | 75.9 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 2002 | 75.9 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 951 | 83.8 |
| 02 | 100 | 67.0 |
| 03 | 102 | 70.6 |
| 05 | 100 | 24.0 |
| 06 | 102 | 72.5 |
| 10 | 200 | 51.0 |
| 12 | 447 | 85.9 |

## Paraphrase groups

0 groups; same prediction —%; all correct —%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 31.2 |
| 0.4 | 88.4 | 25.0 |
| 0.5 | 80.6 | 21.3 |
| 0.6 | 69.6 | 17.2 |
| 0.7 | 59.5 | 13.3 |
| 0.8 | 49.9 | 10.1 |
| 0.9 | 37.0 | 5.1 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 221 | 0.052 | 0.009 |
| [0.1,0.2) | 62 | 0.141 | 0.161 |
| [0.2,0.3) | 60 | 0.260 | 0.233 |
| [0.3,0.4) | 50 | 0.344 | 0.480 |
| [0.4,0.5) | 68 | 0.448 | 0.529 |
| [0.5,0.6) | 42 | 0.548 | 0.667 |
| [0.6,0.7) | 47 | 0.654 | 0.574 |
| [0.7,0.8) | 50 | 0.753 | 0.720 |
| [0.8,0.9) | 108 | 0.856 | 0.898 |
| [0.9,1.0] | 243 | 0.952 | 0.963 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.1,0.2) | 2 | 0.188 | 0.000 |
| [0.2,0.3) | 31 | 0.264 | 0.226 |
| [0.3,0.4) | 89 | 0.345 | 0.213 |
| [0.4,0.5) | 82 | 0.450 | 0.366 |
| [0.5,0.6) | 115 | 0.551 | 0.530 |
| [0.6,0.7) | 107 | 0.651 | 0.598 |
| [0.7,0.8) | 101 | 0.752 | 0.703 |
| [0.8,0.9) | 135 | 0.855 | 0.756 |
| [0.9,1.0] | 389 | 0.967 | 0.949 |


Answered 2002/2002; errors 0; accuracy counting failures as wrong 75.9%.
Paired vs ours (images_v1/images_v1_images): ours only right 341, imajev-4b only right 51, p = 9e-54
