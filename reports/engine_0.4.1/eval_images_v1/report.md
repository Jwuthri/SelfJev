# Evaluation report

- model `Qwen/Qwen3.5-4B` @ `851bf6e806` (shared-prefix tree, forward only: text once per request, each question once, then each candidate), adapter/checkpoint `weights/selfjev_4b_vision`, prompt `challenger-state-first-v1` (6c9d8459ac44)
- data data/ova/eval_images_v1.jsonl; splits ['test']; n=2002; calibration `None`
- cuda / bfloat16; 2026-10-02T23:24:00+0000; wall 108.3s

## Overall

question accuracy 90.5%

![reliability](reliability.svg)

**binary**: n 951, positives 508, accuracy 0.937, precision 0.957, recall 0.923, f1 0.940, auroc 0.986, brier 0.047, log_loss 0.162, ece 0.030

**multiclass**: n 1051, accuracy 0.876, macro_f1 0.931, log_loss 0.333, brier 0.177, ece_top_label 0.030

## By family

| family | n | question acc % | details |
|---|---|---|---|
| img_beans | 204 | 97.5 | bin acc 96.1 F1 96.2 AUROC 0.998 ECE 0.037; mc acc 99.0 mF1 99.0 ECE 0.031 |
| img_eurosat | 200 | 93.5 | bin acc 95.0 F1 95.0 AUROC 0.986 ECE 0.050; mc acc 92.0 mF1 91.9 ECE 0.054 |
| img_fashion | 200 | 89.0 | bin acc 97.0 F1 97.0 AUROC 0.981 ECE 0.042; mc acc 81.0 mF1 81.0 ECE 0.054 |
| img_hurricane | 100 | 61.0 | mc acc 61.0 mF1 60.1 ECE 0.240 |
| img_indoor | 268 | 95.5 | bin acc 95.5 F1 95.4 AUROC 0.997 ECE 0.041; mc acc 95.5 mF1 95.3 ECE 0.029 |
| img_painting | 204 | 70.6 | bin acc 79.4 F1 77.4 AUROC 0.924 ECE 0.150; mc acc 61.8 mF1 58.2 ECE 0.166 |
| img_pets | 222 | 97.3 | bin acc 96.4 F1 97.3 AUROC 0.999 ECE 0.031; mc acc 98.2 mF1 98.1 ECE 0.029 |
| img_rice | 200 | 92.5 | bin acc 91.0 F1 90.9 AUROC 0.972 ECE 0.053; mc acc 94.0 mF1 94.0 ECE 0.032 |
| img_snacks | 200 | 95.5 | bin acc 95.0 F1 95.7 AUROC 0.995 ECE 0.066; mc acc 96.0 mF1 96.0 ECE 0.041 |
| img_trash | 204 | 95.6 | bin acc 97.1 F1 97.1 AUROC 0.999 ECE 0.056; mc acc 94.1 mF1 94.1 ECE 0.017 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 2002 | 90.5 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 2002 | 90.5 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 951 | 93.7 |
| 02 | 100 | 61.0 |
| 03 | 102 | 99.0 |
| 05 | 100 | 94.0 |
| 06 | 102 | 94.1 |
| 10 | 200 | 86.5 |
| 12 | 447 | 88.6 |

## Paraphrase groups

0 groups; same prediction —%; all correct —%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 12.4 |
| 0.4 | 98.8 | 11.7 |
| 0.5 | 96.3 | 10.6 |
| 0.6 | 91.2 | 8.4 |
| 0.7 | 86.5 | 6.8 |
| 0.8 | 81.6 | 5.5 |
| 0.9 | 72.8 | 3.4 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 406 | 0.013 | 0.027 |
| [0.1,0.2) | 22 | 0.141 | 0.273 |
| [0.2,0.3) | 15 | 0.262 | 0.667 |
| [0.3,0.4) | 10 | 0.332 | 0.800 |
| [0.4,0.5) | 8 | 0.438 | 0.500 |
| [0.5,0.6) | 7 | 0.550 | 0.571 |
| [0.6,0.7) | 18 | 0.646 | 0.833 |
| [0.7,0.8) | 22 | 0.753 | 0.818 |
| [0.8,0.9) | 41 | 0.855 | 0.854 |
| [0.9,1.0] | 402 | 0.978 | 0.988 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.2,0.3) | 2 | 0.268 | 0.500 |
| [0.3,0.4) | 11 | 0.382 | 0.273 |
| [0.4,0.5) | 26 | 0.471 | 0.462 |
| [0.5,0.6) | 53 | 0.552 | 0.509 |
| [0.6,0.7) | 50 | 0.650 | 0.620 |
| [0.7,0.8) | 51 | 0.751 | 0.706 |
| [0.8,0.9) | 93 | 0.850 | 0.774 |
| [0.9,1.0] | 765 | 0.987 | 0.966 |
