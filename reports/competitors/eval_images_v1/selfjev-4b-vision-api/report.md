# Evaluation report

- model `selfjev-4b-vision-api` @ `-` (external open model via /v1/systemone), adapter/checkpoint `None`, prompt `jev-request` (-)
- data data/eval_images_v1.jsonl; splits ['test']; n=2002; calibration `None`
- cuda / -; 2026-09-30T17:31:39+0000; wall 142.7s

## Overall

question accuracy 90.6%

![reliability](reliability.svg)

**binary**: n 951, positives 508, accuracy 0.938, precision 0.963, recall 0.919, f1 0.941, auroc 0.985, brier 0.048, log_loss 0.177, ece 0.034

**multiclass**: n 1051, accuracy 0.876, macro_f1 0.938, log_loss 0.335, brier 0.179, ece_top_label 0.036

## By family

| family | n | question acc % | details |
|---|---|---|---|
| img_beans | 204 | 98.0 | bin acc 98.0 F1 98.1 AUROC 0.999 ECE 0.033; mc acc 98.0 mF1 98.0 ECE 0.042 |
| img_eurosat | 200 | 92.5 | bin acc 94.0 F1 94.1 AUROC 0.983 ECE 0.049; mc acc 91.0 mF1 90.9 ECE 0.071 |
| img_fashion | 200 | 86.5 | bin acc 94.0 F1 93.9 AUROC 0.981 ECE 0.048; mc acc 79.0 mF1 78.7 ECE 0.070 |
| img_hurricane | 100 | 61.0 | mc acc 61.0 mF1 60.3 ECE 0.253 |
| img_indoor | 268 | 96.3 | bin acc 95.5 F1 95.4 AUROC 0.996 ECE 0.043; mc acc 97.0 mF1 96.9 ECE 0.028 |
| img_painting | 204 | 72.5 | bin acc 80.4 F1 78.3 AUROC 0.927 ECE 0.173; mc acc 64.7 mF1 63.5 ECE 0.116 |
| img_pets | 222 | 97.7 | bin acc 98.2 F1 98.6 AUROC 0.998 ECE 0.025; mc acc 97.3 mF1 97.2 ECE 0.025 |
| img_rice | 200 | 92.5 | bin acc 91.0 F1 91.1 AUROC 0.968 ECE 0.057; mc acc 94.0 mF1 94.0 ECE 0.053 |
| img_snacks | 200 | 95.0 | bin acc 94.0 F1 94.7 AUROC 0.995 ECE 0.073; mc acc 96.0 mF1 96.0 ECE 0.046 |
| img_trash | 204 | 96.1 | bin acc 98.0 F1 98.1 AUROC 0.999 ECE 0.044; mc acc 94.1 mF1 94.1 ECE 0.040 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 2002 | 90.6 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 2002 | 90.6 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 951 | 93.8 |
| 02 | 100 | 61.0 |
| 03 | 102 | 98.0 |
| 05 | 100 | 94.0 |
| 06 | 102 | 94.1 |
| 10 | 200 | 85.0 |
| 12 | 447 | 89.5 |

## Paraphrase groups

0 groups; same prediction —%; all correct —%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 12.4 |
| 0.4 | 98.6 | 11.6 |
| 0.5 | 96.9 | 10.7 |
| 0.6 | 91.5 | 8.4 |
| 0.7 | 86.6 | 6.7 |
| 0.8 | 79.5 | 5.7 |
| 0.9 | 71.8 | 3.3 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 416 | 0.008 | 0.038 |
| [0.1,0.2) | 18 | 0.144 | 0.278 |
| [0.2,0.3) | 13 | 0.264 | 0.692 |
| [0.3,0.4) | 8 | 0.354 | 0.625 |
| [0.4,0.5) | 11 | 0.460 | 0.545 |
| [0.5,0.6) | 8 | 0.564 | 0.750 |
| [0.6,0.7) | 12 | 0.646 | 0.917 |
| [0.7,0.8) | 14 | 0.747 | 0.714 |
| [0.8,0.9) | 34 | 0.854 | 0.912 |
| [0.9,1.0] | 417 | 0.985 | 0.981 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.2,0.3) | 3 | 0.254 | 0.333 |
| [0.3,0.4) | 12 | 0.369 | 0.333 |
| [0.4,0.5) | 18 | 0.457 | 0.389 |
| [0.5,0.6) | 56 | 0.554 | 0.500 |
| [0.6,0.7) | 52 | 0.653 | 0.615 |
| [0.7,0.8) | 74 | 0.754 | 0.824 |
| [0.8,0.9) | 81 | 0.848 | 0.716 |
| [0.9,1.0] | 755 | 0.987 | 0.967 |


Answered 2002/2002; errors 0; accuracy counting failures as wrong 90.6%.
Paired vs ours (images_v1/images_v1_images): ours only right 15, selfjev-4b-vision-api only right 18, p = 0.73
