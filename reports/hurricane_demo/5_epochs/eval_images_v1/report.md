# Evaluation report

- model `Qwen/Qwen3.5-4B` @ `851bf6e806` (shared-prefix tree, forward only: text once per request, each question once, then each candidate), adapter/checkpoint `/home/ubuntu/.selfjev/server/jobs/ftjob_4e4f0ce0d40f4cfbb677/run/adapter`, prompt `challenger-state-first-v1` (6c9d8459ac44)
- data data/ova/eval_images_v1.jsonl; splits ['test']; n=2002; calibration `None`
- cuda / bfloat16; 2026-10-02T23:39:09+0000; wall 107.9s

## Overall

question accuracy 91.3%

![reliability](reliability.svg)

**binary**: n 951, positives 508, accuracy 0.933, precision 0.959, recall 0.913, f1 0.935, auroc 0.986, brier 0.049, log_loss 0.168, ece 0.040

**multiclass**: n 1051, accuracy 0.895, macro_f1 0.932, log_loss 0.288, brier 0.147, ece_top_label 0.030

## By family

| family | n | question acc % | details |
|---|---|---|---|
| img_beans | 204 | 99.0 | bin acc 98.0 F1 98.1 AUROC 0.999 ECE 0.050; mc acc 100.0 mF1 100.0 ECE 0.049 |
| img_eurosat | 200 | 91.5 | bin acc 93.0 F1 93.1 AUROC 0.988 ECE 0.069; mc acc 90.0 mF1 89.5 ECE 0.110 |
| img_fashion | 200 | 87.0 | bin acc 96.0 F1 96.0 AUROC 0.980 ECE 0.063; mc acc 78.0 mF1 77.5 ECE 0.071 |
| img_hurricane | 100 | 86.0 | mc acc 86.0 mF1 85.9 ECE 0.078 |
| img_indoor | 268 | 95.1 | bin acc 95.5 F1 95.4 AUROC 0.996 ECE 0.044; mc acc 94.8 mF1 94.5 ECE 0.031 |
| img_painting | 204 | 70.6 | bin acc 79.4 F1 77.4 AUROC 0.923 ECE 0.150; mc acc 61.8 mF1 56.7 ECE 0.111 |
| img_pets | 222 | 97.3 | bin acc 96.4 F1 97.3 AUROC 0.999 ECE 0.036; mc acc 98.2 mF1 98.1 ECE 0.030 |
| img_rice | 200 | 92.5 | bin acc 90.0 F1 89.8 AUROC 0.974 ECE 0.091; mc acc 95.0 mF1 95.0 ECE 0.039 |
| img_snacks | 200 | 93.5 | bin acc 93.0 F1 93.8 AUROC 0.995 ECE 0.079; mc acc 94.0 mF1 94.0 ECE 0.040 |
| img_trash | 204 | 96.1 | bin acc 97.1 F1 97.1 AUROC 0.999 ECE 0.057; mc acc 95.1 mF1 95.1 ECE 0.035 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 2002 | 91.3 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 2002 | 91.3 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 951 | 93.3 |
| 02 | 100 | 86.0 |
| 03 | 102 | 100.0 |
| 05 | 100 | 95.0 |
| 06 | 102 | 95.1 |
| 10 | 200 | 84.0 |
| 12 | 447 | 87.9 |

## Paraphrase groups

0 groups; same prediction —%; all correct —%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 10.5 |
| 0.4 | 97.5 | 8.6 |
| 0.5 | 94.2 | 7.3 |
| 0.6 | 87.8 | 5.4 |
| 0.7 | 83.2 | 4.1 |
| 0.8 | 77.0 | 2.2 |
| 0.9 | 68.1 | 1.3 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 391 | 0.016 | 0.023 |
| [0.1,0.2) | 34 | 0.143 | 0.235 |
| [0.2,0.3) | 19 | 0.259 | 0.579 |
| [0.3,0.4) | 9 | 0.345 | 0.778 |
| [0.4,0.5) | 14 | 0.449 | 0.643 |
| [0.5,0.6) | 10 | 0.566 | 0.700 |
| [0.6,0.7) | 29 | 0.643 | 0.793 |
| [0.7,0.8) | 28 | 0.755 | 0.786 |
| [0.8,0.9) | 60 | 0.860 | 0.950 |
| [0.9,1.0] | 357 | 0.972 | 0.994 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.2,0.3) | 2 | 0.238 | 0.000 |
| [0.3,0.4) | 24 | 0.365 | 0.167 |
| [0.4,0.5) | 35 | 0.453 | 0.543 |
| [0.5,0.6) | 67 | 0.553 | 0.672 |
| [0.6,0.7) | 49 | 0.654 | 0.714 |
| [0.7,0.8) | 65 | 0.758 | 0.723 |
| [0.8,0.9) | 93 | 0.853 | 0.903 |
| [0.9,1.0] | 716 | 0.980 | 0.987 |
