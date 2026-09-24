# Comparison: LoRA vs ~typesafe/jev-latest

| | LoRA | ~typesafe/jev-latest |
|---|---|---|
| adapter | None | None |
| calibration | no | no |
| prompt | ours-LoRA (-) | ~typesafe/jev-latest (-) |
| n | 1991 | 1991 |

| slice | metric | LoRA | ~typesafe/jev-latest |
|---|---|---|---|
| overall | question acc % | 85.1 | 97.2 |
| overall | binary acc % | 89.4 | 97.8 |
| overall | binary F1 % | 87.9 | 97.5 |
| overall | binary AUROC | 0.959 | 0.999 |
| overall | binary ECE | 0.022 | 0.061 |
| overall | multiclass acc % | 91.6 | 98.1 |
| overall | multiclass macro-F1 % | 84.7 | 97.1 |
| overall | multiclass ECE | 0.022 | 0.004 |
| overall | multilabel exact % | 63.9 | 94.2 |
| overall | multilabel micro-F1 % | 89.4 | 98.8 |
| overall | multilabel label AUROC | 0.958 | 0.998 |
| overall | multilabel ECE | 0.052 | 0.045 |
| overall | binary brier | 0.078 | 0.019 |
| overall | binary log_loss | 0.259 | 0.099 |
| overall | multiclass brier | 0.125 | 0.028 |
| overall | multiclass log_loss | 0.248 | 0.055 |
| overall | multilabel brier | 0.083 | 0.014 |
| overall | multilabel log_loss | 0.281 | 0.076 |
| e2_hard | question acc % | 83.2 | 96.7 |
| e2_hard | binary acc % | 86.8 | 97.1 |
| e2_hard | binary F1 % | 82.6 | 96.1 |
| e2_hard | binary AUROC | 0.938 | 0.998 |
| e2_hard | binary ECE | 0.052 | 0.062 |
| e2_hard | multiclass acc % | 88.6 | 97.9 |
| e2_hard | multiclass macro-F1 % | 79.5 | 96.6 |
| e2_hard | multiclass ECE | 0.027 | 0.011 |
| e2_hard | multilabel exact % | 65.9 | 93.9 |
| e2_hard | multilabel micro-F1 % | 89.2 | 98.5 |
| e2_hard | multilabel label AUROC | 0.946 | 0.993 |
| e2_hard | multilabel ECE | 0.038 | 0.049 |
| e2_simple | question acc % | 92.3 | 98.5 |
| e2_simple | binary acc % | 96.2 | 98.5 |
| e2_simple | binary F1 % | 96.5 | 98.7 |
| e2_simple | binary AUROC | 0.985 | 1.000 |
| e2_simple | binary ECE | 0.039 | 0.049 |
| e2_simple | multiclass acc % | 98.5 | 99.5 |
| e2_simple | multiclass macro-F1 % | 96.8 | 99.4 |
| e2_simple | multiclass ECE | 0.034 | 0.005 |
| e2_simple | multilabel exact % | 70.8 | 96.7 |
| e2_simple | multilabel micro-F1 % | 92.0 | 99.4 |
| e2_simple | multilabel label AUROC | 0.986 | 1.000 |
| e2_simple | multilabel ECE | 0.092 | 0.042 |
| e2_very_hard | question acc % | 79.8 | 96.5 |
| e2_very_hard | binary acc % | 84.9 | 97.8 |
| e2_very_hard | binary F1 % | 80.8 | 97.2 |
| e2_very_hard | binary AUROC | 0.933 | 0.999 |
| e2_very_hard | binary ECE | 0.042 | 0.076 |
| e2_very_hard | multiclass acc % | 87.5 | 97.0 |
| e2_very_hard | multiclass macro-F1 % | 77.5 | 94.9 |
| e2_very_hard | multiclass ECE | 0.054 | 0.009 |
| e2_very_hard | multilabel exact % | 55.4 | 92.3 |
| e2_very_hard | multilabel micro-F1 % | 87.3 | 98.6 |
| e2_very_hard | multilabel label AUROC | 0.946 | 0.999 |
| e2_very_hard | multilabel ECE | 0.057 | 0.049 |

## Question accuracy % by hard-case tag

| tag | n | LoRA | ~typesafe/jev-latest |
|---|---|---|---|
| (none) | 569 | 94.4 | 98.4 |
| contradiction | 172 | 86.0 | 98.8 |
| distractor | 474 | 80.4 | 97.0 |
| double_negation | 126 | 85.7 | 99.2 |
| evidence_end | 57 | 82.5 | 100.0 |
| evidence_middle | 114 | 87.7 | 99.1 |
| evidence_start | 17 | 76.5 | 94.1 |
| exception | 213 | 78.4 | 95.3 |
| hypothetical | 128 | 92.2 | 98.4 |
| injection | 151 | 71.5 | 97.4 |
| lexical_overlap | 201 | 88.6 | 98.5 |
| long_state | 191 | 82.7 | 99.0 |
| missing_evidence | 141 | 92.9 | 97.9 |
| multi_positive | 322 | 66.8 | 96.0 |
| multi_turn | 149 | 83.9 | 96.0 |
| negation | 257 | 83.3 | 98.8 |
| nota | 118 | 83.1 | 95.8 |
| numeric_reasoning | 224 | 67.0 | 92.0 |
| paraphrase | 218 | 83.5 | 95.4 |
| role_reversal | 187 | 86.6 | 96.8 |
| sarcasm | 149 | 71.8 | 97.3 |
| temporal_reasoning | 203 | 69.5 | 89.2 |
| zero_positive | 73 | 80.8 | 95.9 |
| zero_positive_distractor | 1 | 100.0 | 100.0 |

## Paired tests vs our LoRA model (exact McNemar on the same questions)

| other | n | LoRA only right | other only right | p |
|---|---|---|---|---|
| ~typesafe/jev-latest | 1991 | 20 | 261 | 1.1e-54 |

Spend (USD, from OpenRouter account usage): {'~typesafe/jev-latest': 0.0}; total $0.00
