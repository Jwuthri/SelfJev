# eval2: frozen target-task test set

`data/eval2.jsonl` sha256 `2fa954592d0a31248b25810a2faeec653b4c5ef5e454ea5e1349afbb2379076a` — 1991 questions / 647 states, every row split=test. **Frozen: never train, select prompts, fit thresholds or temperatures on it.** Authors: anthropic/claude-opus-5.5, moonshotai/kimi-k3, z-ai/glm-5.3. Judges (blind, both must agree with the author): astra, gemini-3.1-pro-preview. Jev is reported, never used to keep or drop. LLM-verified; human spot-check list in review/SPOTCHECK.md. Rows are expanded (one question per line) so ids are the raw `<source_id>-q<i>` and join `review/answers_*.jsonl`; a first export on 2026-09-24 used source-format lines whose ids were renumbered after drops (sha `f18549eb…`): `review/id_map_sourceformat_to_real.json` maps those ids to the real ones, and the 95.2% Jev figure computed on that misalignment was wrong.

States dropped for 8-gram overlap ≥ 0.3 with training/eval files: 0 []

## Agreement (before the keep rule)

| family | judged | author = astra % | author = gemini-3.1-pro-preview % | kept (unanimous) | dropped | unanswered |
|---|---|---|---|---|---|---|
| e2_hard | 702 | 97.2 | 96.7 | 673 | 29 | 0 |
| e2_simple | 684 | 98.1 | 97.5 | 664 | 20 | 0 |
| e2_very_hard | 684 | 97.2 | 96.6 | 654 | 30 | 0 |
| **all** | 2070 | 97.5 | 97.0 | 1991 | 79 | 0 |

## Composition of the kept set, with Jev accuracy on it

### tier (family)

| tier (family) | n | Jev acc % |
|---|---|---|
| e2_hard | 673 | 96.4 |
| e2_simple | 664 | 98.6 |
| e2_very_hard | 654 | 96.5 |

### author

| author | n | Jev acc % |
|---|---|---|
| anthropic/claude-opus-5.5 | 560 | 96.2 |
| moonshotai/kimi-k3 | 649 | 98.0 |
| z-ai/glm-5.3 | 782 | 97.2 |

### type

| type | n | Jev acc % |
|---|---|---|
| binary | 1016 | 97.6 |
| multiclass | 593 | 98.1 |
| multilabel | 382 | 94.5 |

### length bucket (tokens)

| length bucket (tokens) | n | Jev acc % |
|---|---|---|
| 1024 | 214 | 97.2 |
| 128 | 222 | 96.8 |
| 2048 | 193 | 98.4 |
| 256 | 191 | 93.7 |
| 32 | 201 | 95.0 |
| 4096 | 196 | 99.5 |
| 512 | 190 | 96.8 |
| 64 | 214 | 97.7 |
| 8 | 193 | 98.4 |
| 8192 | 177 | 98.3 |

### hard case (all tags)

| hard case (all tags) | n | Jev acc % |
|---|---|---|
| (none) | 569 | 98.6 |
| contradiction | 172 | 98.8 |
| distractor | 474 | 97.3 |
| double_negation | 126 | 99.2 |
| evidence_end | 57 | 100.0 |
| evidence_middle | 114 | 99.1 |
| evidence_start | 17 | 94.1 |
| exception | 213 | 94.8 |
| hypothetical | 128 | 98.4 |
| injection | 151 | 97.4 |
| lexical_overlap | 201 | 98.5 |
| long_state | 191 | 99.0 |
| missing_evidence | 141 | 97.9 |
| multi_positive | 322 | 96.3 |
| multi_turn | 149 | 96.0 |
| negation | 257 | 98.8 |
| nota | 118 | 95.8 |
| numeric_reasoning | 224 | 91.5 |
| paraphrase | 218 | 95.0 |
| role_reversal | 187 | 96.8 |
| sarcasm | 149 | 98.0 |
| temporal_reasoning | 203 | 88.2 |
| zero_positive | 73 | 95.9 |
| zero_positive_distractor | 1 | 100.0 |

Multilabel positives: {0: 34, 1: 26, 2: 77, 3: 141, 4: 99, 5: 4, 6: 1}. Multiclass questions offering a none candidate: 391, none correct in 58 (14.8%).

