# Evaluation report

- model `Qwen/Qwen3.5-4B` @ `851bf6e806` (shared-prefix tree, forward only: text once per request, each question once, then each candidate), adapter/checkpoint `/home/ubuntu/.selfjev/server/jobs/ftjob_41120853b4b54553832c/run/adapter`, prompt `challenger-state-first-v1` (6c9d8459ac44)
- data data/ova/eval_images_v1.jsonl; splits ['test']; n=2002; calibration `None`
- cuda / bfloat16; 2026-10-02T23:27:59+0000; wall 108.1s

## Overall

question accuracy 91.2%

![reliability](reliability.svg)

**binary**: n 951, positives 508, accuracy 0.934, precision 0.959, recall 0.915, f1 0.937, auroc 0.986, brier 0.048, log_loss 0.167, ece 0.039

**multiclass**: n 1051, accuracy 0.892, macro_f1 0.927, log_loss 0.300, brier 0.155, ece_top_label 0.033

## By family

| family | n | question acc % | details |
|---|---|---|---|
| img_beans | 204 | 99.0 | bin acc 98.0 F1 98.1 AUROC 0.999 ECE 0.052; mc acc 100.0 mF1 100.0 ECE 0.052 |
| img_eurosat | 200 | 92.5 | bin acc 93.0 F1 93.1 AUROC 0.987 ECE 0.064; mc acc 92.0 mF1 91.8 ECE 0.118 |
| img_fashion | 200 | 88.0 | bin acc 96.0 F1 96.0 AUROC 0.980 ECE 0.067; mc acc 80.0 mF1 79.9 ECE 0.096 |
| img_hurricane | 100 | 79.0 | mc acc 79.0 mF1 78.6 ECE 0.054 |
| img_indoor | 268 | 94.8 | bin acc 95.5 F1 95.4 AUROC 0.997 ECE 0.043; mc acc 94.0 mF1 93.7 ECE 0.026 |
| img_painting | 204 | 70.6 | bin acc 79.4 F1 77.4 AUROC 0.924 ECE 0.148; mc acc 61.8 mF1 56.5 ECE 0.105 |
| img_pets | 222 | 97.3 | bin acc 96.4 F1 97.3 AUROC 0.999 ECE 0.036; mc acc 98.2 mF1 98.1 ECE 0.030 |
| img_rice | 200 | 93.0 | bin acc 91.0 F1 90.9 AUROC 0.972 ECE 0.090; mc acc 95.0 mF1 95.0 ECE 0.041 |
| img_snacks | 200 | 94.0 | bin acc 93.0 F1 93.8 AUROC 0.995 ECE 0.076; mc acc 95.0 mF1 95.0 ECE 0.056 |
| img_trash | 204 | 96.1 | bin acc 97.1 F1 97.1 AUROC 0.999 ECE 0.061; mc acc 95.1 mF1 95.1 ECE 0.044 |

## by hard case

| slice | n | question acc % |
|---|---|---|
| (none) | 2002 | 91.2 |

## by state tokens

| slice | n | question acc % |
|---|---|---|
| 00000-00127 | 2002 | 91.2 |

## by candidates

| slice | n | question acc % |
|---|---|---|
| 01 | 951 | 93.4 |
| 02 | 100 | 79.0 |
| 03 | 102 | 100.0 |
| 05 | 100 | 95.0 |
| 06 | 102 | 95.1 |
| 10 | 200 | 86.0 |
| 12 | 447 | 87.9 |

## Paraphrase groups

0 groups; same prediction —%; all correct —%

## Multiclass abstention (coverage vs error on accepted)

| abstain_below | coverage % | error % |
|---|---|---|
| 0.0 | 100.0 | 10.8 |
| 0.4 | 97.5 | 9.1 |
| 0.5 | 94.4 | 7.9 |
| 0.6 | 87.5 | 6.1 |
| 0.7 | 81.2 | 3.8 |
| 0.8 | 73.4 | 2.1 |
| 0.9 | 62.7 | 1.5 |

## Reliability: binary

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.0,0.1) | 388 | 0.019 | 0.023 |
| [0.1,0.2) | 36 | 0.144 | 0.194 |
| [0.2,0.3) | 17 | 0.260 | 0.471 |
| [0.3,0.4) | 12 | 0.333 | 0.833 |
| [0.4,0.5) | 13 | 0.451 | 0.692 |
| [0.5,0.6) | 14 | 0.560 | 0.786 |
| [0.6,0.7) | 26 | 0.659 | 0.846 |
| [0.7,0.8) | 27 | 0.758 | 0.741 |
| [0.8,0.9) | 54 | 0.854 | 0.944 |
| [0.9,1.0] | 364 | 0.971 | 0.992 |

## Reliability: multiclass

| bin | n | mean confidence | observed frequency |
|---|---|---|---|
| [0.2,0.3) | 4 | 0.262 | 0.250 |
| [0.3,0.4) | 22 | 0.367 | 0.227 |
| [0.4,0.5) | 33 | 0.451 | 0.545 |
| [0.5,0.6) | 72 | 0.543 | 0.694 |
| [0.6,0.7) | 67 | 0.650 | 0.642 |
| [0.7,0.8) | 82 | 0.758 | 0.805 |
| [0.8,0.9) | 112 | 0.853 | 0.946 |
| [0.9,1.0] | 659 | 0.981 | 0.985 |
