# Where selfjev loses to Jev on eval2 (category level)

Ours: `reports/images_v1/eval2/report.json`; Jev: `reports/external/eval2/typesafe_jev-latest`. A test-set diagnosis: never train on items.

| slice | n | ours | Jev | only ours / only Jev | p |
|---|---|---|---|---|---|
| all | 1991 | 96.1 | 97.2 | 25 / 47 | 0.013 |
| trap: multi_positive | 322 | 90.7 | 96.0 | 4 / 21 | 0.00091 |
| type: multilabel | 382 | 90.8 | 94.2 | 9 / 22 | 0.029 |
| tier: hard | 673 | 94.9 | 96.7 | 11 / 23 | 0.058 |
| trap: distractor | 474 | 95.1 | 97.0 | 5 / 14 | 0.064 |
| tier: very_hard | 654 | 95.1 | 96.5 | 8 / 17 | 0.11 |
| type: multiclass | 593 | 97.3 | 98.1 | 6 / 11 | 0.33 |
| trap: numeric_reasoning | 224 | 89.7 | 92.0 | 5 / 10 | 0.3 |
| type: binary | 1016 | 97.4 | 97.8 | 10 / 14 | 0.54 |
| trap: multi_turn | 149 | 93.3 | 96.0 | 1 / 5 | 0.22 |
| trap: contradiction | 172 | 97.1 | 98.8 | 0 / 3 | 0.25 |
| trap: paraphrase | 218 | 94.0 | 95.4 | 3 / 6 | 0.51 |
| trap: double_negation | 126 | 96.8 | 99.2 | 0 / 3 | 0.25 |
| trap: hypothetical | 128 | 96.1 | 98.4 | 1 / 4 | 0.38 |
| trap: role_reversal | 187 | 95.7 | 96.8 | 3 / 5 | 0.73 |
| trap: negation | 257 | 98.1 | 98.8 | 2 / 4 | 0.69 |
| trap: injection | 151 | 96.0 | 97.4 | 1 / 3 | 0.62 |
| tier: simple | 664 | 98.3 | 98.5 | 6 / 7 | 1 |
| trap: none | 569 | 98.2 | 98.4 | 5 / 6 | 1 |
| trap: lexical_overlap | 201 | 98.0 | 98.5 | 1 / 2 | 1 |
| trap: temporal_reasoning | 203 | 88.7 | 89.2 | 9 / 10 | 1 |
| trap: evidence_middle | 114 | 98.2 | 99.1 | 1 / 2 | 1 |
| trap: long_state | 191 | 98.4 | 99.0 | 2 / 3 | 1 |
| trap: evidence_end | 57 | 98.2 | 100.0 | 0 / 1 | 1 |
| trap: sarcasm | 149 | 97.3 | 97.3 | 4 / 4 | 1 |
| trap: zero_positive | 73 | 95.9 | 95.9 | 3 / 3 | 1 |
| trap: nota | 118 | 95.8 | 95.8 | 3 / 3 | 1 |
| trap: zero_positive_distractor | 1 | 100.0 | 100.0 | 0 / 0 | 1 |
| trap: missing_evidence | 141 | 98.6 | 97.9 | 1 / 0 | 1 |
| trap: evidence_start | 17 | 100.0 | 94.1 | 1 / 0 | 1 |
| trap: exception | 213 | 97.2 | 95.3 | 6 / 2 | 0.29 |

Confident mistakes (wrong at >= 0.9): ours 9, Jev 3.

Accuracy on the questions each model is most sure about (same coverage):

| coverage | ours | Jev |
|---|---|---|
| 50% | 99.90 | 99.90 |
| 80% | 99.87 | 99.87 |
| 90% | 99.22 | 99.78 |
| 95% | 98.15 | 99.00 |
| 100% | 96.13 | 97.24 |
