# Evaluation report

- model `jpt-4b` @ `-` (external open model via /v1/systemone), adapter/checkpoint `None`, prompt `jev-request` (-)
- data data/eval_images_v1.jsonl; splits ['test']; n=2002; calibration `None`
- cuda / -; 2026-09-30T19:32:50+0000; wall 74.9s

## Overall

question accuracy 76.2%

![reliability](reliability.svg)

**binary**: n 951, positives 508, accuracy 0.823, precision 0.911, recall 0.742, f1 0.818, auroc 0.934, brier 0.124, log_loss 0.380, ece 0.108

**multiclass**: n 1051, accuracy 0.706, macro_f1 0.893, log_loss 0.722, brier 0.364, ece_top_label 0.025

## By family

| family | n | question acc % | details |
|---|---|---|---|
| img_beans | 204 | 75.0 | bin acc 81.4 F1 83.5 AUROC 0.878 ECE 0.094; mc acc 68.6 mF1 68.9 ECE 0.095 |
| img_eurosat | 200 | 56.5 | bin acc 71.0 F1 63.3 AUROC 0.877 ECE 0.195; mc acc 42.0 mF1 35.7 ECE 0.162 |
| img_fashion | 200 | 78.5 | bin acc 86.0 F1 84.8 AUROC 0.944 ECE 0.133; mc acc 71.0 mF1 70.3 ECE 0.112 |
| img_hurricane | 100 | 62.0 | mc acc 62.0 mF1 61.2 ECE 0.108 |
| img_indoor | 268 | 96.6 | bin acc 95.5 F1 95.4 AUROC 0.997 ECE 0.058; mc acc 97.8 mF1 97.7 ECE 0.052 |
| img_painting | 204 | 68.6 | bin acc 79.4 F1 77.9 AUROC 0.912 ECE 0.153; mc acc 57.8 mF1 56.9 ECE 0.070 |
| img_pets | 222 | 92.8 | bin acc 89.2 F1 91.4 AUROC 0.982 ECE 0.120; mc acc 96.4 mF1 96.3 ECE 0.094 |
| img_rice | 200 | 38.0 | bin acc 49.0 F1 0.0 AUROC 0.556 ECE 0.276; mc acc 27.0 mF1 24.6 ECE 0.078 |
| img_snacks | 200 | 93.0 | bin acc 93.0 F1 93.8 AUROC 0.997 ECE 0.096; mc acc 93.0 mF1 93.0 ECE 0.054 |
| img_trash | 204 | 84.8 | bin acc 91.2 F1 91.6 AUROC 0.972 ECE 0.055; mc acc 78.4 mF1 73.7 ECE 0.126 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 2002 | 76.2 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 2002 | 76.2 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 951 | 82.3 |
| 02 | 100 | 62.0 |
| 03 | 102 | 68.6 |
| 05 | 100 | 27.0 |
| 06 | 102 | 78.4 |
| 10 | 200 | 56.5 |
| 12 | 447 | 87.2 |

## Paraphrase groups

0 groups; same prediction —%; all correct —%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 29.4 |
| 0.4 | 78.8 | 18.0 |
| 0.5 | 72.1 | 16.0 |
| 0.6 | 61.7 | 11.4 |
| 0.7 | 52.7 | 7.9 |
| 0.8 | 45.5 | 5.4 |
| 0.9 | 35.8 | 3.2 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 318 | 0.016 | 0.044 |
| [0.1,0.2) | 90 | 0.147 | 0.444 |
| [0.2,0.3) | 52 | 0.242 | 0.519 |
| [0.3,0.4) | 45 | 0.347 | 0.667 |
| [0.4,0.5) | 32 | 0.437 | 0.625 |
| [0.5,0.6) | 37 | 0.556 | 0.676 |
| [0.6,0.7) | 58 | 0.669 | 0.862 |
| [0.7,0.8) | 54 | 0.758 | 0.852 |
| [0.8,0.9) | 73 | 0.852 | 0.932 |
| [0.9,1.0] | 192 | 0.950 | 0.979 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.1,0.2) | 23 | 0.163 | 0.087 |
| [0.2,0.3) | 141 | 0.250 | 0.241 |
| [0.3,0.4) | 59 | 0.347 | 0.458 |
| [0.4,0.5) | 70 | 0.456 | 0.600 |
| [0.5,0.6) | 110 | 0.547 | 0.573 |
| [0.6,0.7) | 94 | 0.656 | 0.681 |
| [0.7,0.8) | 76 | 0.754 | 0.763 |
| [0.8,0.9) | 102 | 0.859 | 0.863 |
| [0.9,1.0] | 376 | 0.969 | 0.968 |


Answered 2002/2002; errors 0; accuracy counting failures as wrong 76.2%.
Paired vs ours (images_v1/images_v1_images): ours only right 325, jpt-4b only right 40, p = 1.3e-56
