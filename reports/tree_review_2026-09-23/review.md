# SelfJev: updated review after the tree results

Reviewed 23 September 2026. This addendum supersedes the earlier strategy's assumption that tree quality and instruction-LoRA results were still pending. It also includes the newly available round-two tree results. Source code, saved predictions, training metadata, same-session benchmarks and the latest hard-case pipeline were reread. Application code and model weights were not changed.

**The tree model should now be the main development path.** It combines the benefits that the previous architectures demonstrated separately: useful pretrained decision behavior and sharing of document computation. The evidence no longer calls for an architectural replacement as the next default step. The immediate priorities are faster execution, better rejection semantics, and targeted quality improvements.

## What changed in the evidence

All quality rows below align on the same 3,471 question IDs, targets and candidate lists. Correctness and headline metrics were recomputed from saved predictions.

| Model | Overall accuracy | Binary AUROC | Multiclass accuracy | Multilabel exact match | Authored cases, 171 questions |
|---|---:|---:|---:|---:|---:|
| Stock 4B reranker + LoRA | 80.32% | 0.945 | 82.27% | 47.67% | 70.76% |
| Stock 4B Instruct + LoRA | 80.55% | 0.944 | 82.59% | 48.26% | 75.44% |
| Stock 8B reranker + LoRA | 80.67% | 0.945 | 82.87% | 47.97% | 74.85% |
| **Tree 4B reranker + LoRA, round 1** | **81.59%** | **0.953** | **83.85%** | **51.74%** | **78.36%** |
| Tree 4B Instruct + LoRA | 80.35% | 0.958 | 82.31% | 46.80% | 79.53% |
| Tree 4B reranker + LoRA, round 2 | 80.61% | 0.956 | 82.17% | 50.87% | 81.87% |
| Jev, cached API results | 82.71% | 0.981 | 84.60% | 40.12% | 94.74% |

Round-one tree has 2,832 correct answers versus stock 4B's 2,788. There are 182 tree-only wins and 138 stock-only wins; the paired question-level exact McNemar p-value is 0.0161. A new paired bootstrap resampling normalized-document groups gives an approximate 95% interval of **+0.29 to +2.28 percentage points**. This preserves questions from the same document together. It does not account for every shared authoring template or the accumulated use of this test set for development.

Relative to Jev, tree is 39 correct answers behind, with 217 tree-only wins and 256 Jev-only wins. The p-value of 0.0805 does **not** prove equivalence. The document-bootstrap interval for tree minus Jev is approximately -2.36 to +0.12 points. The authored slice still has a 16.4-point gap in round one, although it is small and noisy.

The aggregate also hides a useful decomposition: relative to Jev, round-one tree has 63 fewer correct binary answers, 16 fewer multiclass answers, and 40 more exact multilabel answers. Binary accuracy is 87.1% versus Jev's 93.5%. Binary judgments therefore remain a high-value quality target even though AUROC improved.

## Why the tree matters architecturally

[tree.py](../../src/personal_jev/tree.py) retains the pretrained transformer and yes/no readout. Each document root is processed once. Question tokens can attend to the document, and each answer leaf can attend to the document and its own question through every layer. Sibling branches are masked. Position IDs follow each root-to-leaf path.

The cached inference path is **two decoder passes**: document prefill, then all branch tokens against its cache. Packed training uses one whole-tree pass. There is no autoregressive answer generation. Saying simply “one forward pass” obscures the actual inference implementation, but the important saving is real: no repeated full document computation per candidate.

A cached tree is mathematically a shared execution of the same state-first leaf paths. Caching itself does not make those paths more accurate. The accuracy change relative to stock comes from the state-first format and the resulting training setup. Training data hashes match between the original stock and tree runs, but their optimization schedules differ: stock uses 216 optimizer steps, tree 84, because each tree batch holds more questions. This is a strong end-to-end result, not a clean attribution of all accuracy gains to token order alone.

Nine existing inference/gradient tests were rerun and passed in 9.06 seconds, including real 0.6B agreement, batching, branch isolation, control-token handling and gradient flow. The training-entrypoint test was excluded; no new training was launched. These tests support implementation correctness, not accuracy at every context length or bf16 equivalence on the deployed 4B GPU.

## The speed improvement is substantial and verified

Both benchmarked adapters match the hashes in their respective quality reports. These are A10G, bf16, same-session measurements with an unmerged adapter and one request at a time.

| Workload | Stock 4B | Tree 4B | Speedup |
|---|---:|---:|---:|
| 512 tokens, 1 question x 3 candidates | 375 ms | 192 ms | 2.0x |
| 512 tokens, 16 x 3 | 5,414 ms | 686 ms | 7.9x |
| 2,048 tokens, 16 x 3 | 20,460 ms | 1,091 ms | 18.8x |
| 8,192 tokens, 16 x 3 | 90,449 ms | 2,798 ms | 32.3x |
| 16,384 tokens, 16 x 3 | 206,915 ms | 5,638 ms | 36.7x |
| 16,384 tokens, 1 binary question | 4,324 ms | 4,483 ms | 0.96x |

The last row confirms the mechanism: one binary judgment has no repeated candidate encoding to eliminate. Conversely, even one multiclass question has several candidates and benefits from sharing.

The measured speedups apply to this implementation and batching configuration. The stock benchmark still uses `task-v1`, whereas its quality report uses `answer-v1`; [benchmark.py](../../src/personal_jev/benchmark.py#L79) does not accept the selected prompt. That should be repaired before publishing a final matched quality/latency claim. It is unlikely to explain away a 32x reduction, but it prevents an exact same-format comparison. The 8K stock case runs 48 batches under its 16,384-token budget; an optimized stock baseline with a larger safe budget could change the ratio.

Tree benchmark cells have 3-10 samples; long stock cells have only 2. Their reported p95 values are essentially upper order statistics of a tiny sample, not production tail-latency evidence. The states are repetitive filler. These runs establish execution cost at long lengths, not long-document decision quality. Jev latency has not been measured on these requests.

## New diagnosis: round two's regression is concentrated in rejection

Round two uses 16,357 training questions after family caps and overlength exclusions, compared with 10,112 in round one. It includes the verified hard-case data, uses an 8K rather than 2K training path limit, and completes 224 steps. Reload matches exactly. The training validation mixture also changes, so its 85.7% internal validation score cannot be compared directly with round one's 80.2% as a generalization gain.

On the shared test, round two falls from 2,832 to 2,798 correct answers. Its 34-answer net loss is entirely accounted for by CLINC:

- CLINC accuracy falls from **94.7% to 83.3%**.
- All **34 newly incorrect CLINC decisions** select `none`.
- There are no CLINC decisions corrected in the opposite direction.
- `none` selections increase from **61 to 95**, while the true count remains 45.
- Both runs correctly reject all 45 gold out-of-scope examples.
- Excluding `none` from the ranking, both models put the correct intent first on **254 of 255** in-scope examples.

Other families change in both directions and cancel in total. Authored-case accuracy improves from **78.4% to 81.9%**. Thus the aggregate regression is not evidence that the model broadly lost its ability to distinguish intents. Its willingness to reject the supplied options changed.

A useful next experiment is to separate **which candidate fits best** from **whether any supplied candidate is acceptable**. At present the `none` leaf sees the generic description “matches none of the other options” without seeing the other candidate descriptions. The final softmax uses all scores, so rejection can work as an implicit threshold; however, the `none` branch cannot explicitly judge the alternative set.

Test a learned, permutation-invariant rejection rule over candidate scores, or include the full candidate bank in the shared question prefix before scoring leaves. The latter preserves document sharing but changes the path format and needs adaptation plus permutation checks. Train with matched examples where adding/removing a valid option flips the correct rejection decision. Do not simply subtract a test-tuned constant from `none` scores: this diagnosis used the test and requires a separate validation/fresh-test experiment.

Review label descriptions too. Some CLINC mappings are narrower than the original dataset intent: for example, a request to use a preferred name is represented as changing an account username. Greater literal adherence can conflict with that proxy label. The observed loss is real under the current gold labels; its cause is not yet established as poor language understanding or bad training data.

## What I would prioritize now

1. **Keep `tree_4b` round one as the aggregate reference.** Round two is a useful specialized variant and diagnostic, not an automatic replacement. Keep tree Instruct as a control: it loses overall but has slightly better binary ranking and authored accuracy, so “reranker is always the better base” is stronger than the evidence.
2. **Fix execution waste without changing model semantics.** [TreeModel.cached](../../src/personal_jev/tree.py#L183) still builds a complete T-by-T boolean mask and then discards the root query rows. A roughly 32K tree needs around a gigabyte for just one such CPU mask, plus temporaries. Build root visibility and the branch submask directly. Profile root prefill, branch attention, mask construction and projection work separately. Then test adapter merging and compatible structured attention kernels.
3. **Investigate candidate rejection before adding another large training batch.** The CLINC result gives a precise failure pattern and a cheap, falsifiable experiment. Add balanced in-scope/out-of-scope candidate-set examples and inspect description quality.
4. **Target the remaining judgments.** Agent-output grading remains 61.5% in round one and 57.7% in round two, versus Jev's 92.3% on 26 questions. BoolQ and SST-2 also remain behind. Use a new task-balanced evaluation to decide whether improvements to these matter more than the present public-dataset mixture.
5. **Make calibration goals explicit.** A temperature near one only says that this temperature-fitting procedure found little benefit on its calibration split. Round-one binary ECE is 0.077 versus stock's 0.056 and Jev's 0.045. The validation thresholds maximize F1, not overall accuracy; applying the full round-one calibration file drops test accuracy to 79.3%. Separate temperature effects from threshold objectives, and validate the deployment policy independently.
6. **Defer an architectural restart.** T5Gemma, GLiClass and hybrid backbones remain research options, but the tree has now earned priority. A smaller tree student is a logical later speed experiment; the next step should first establish what the current 4B model can retain under efficient execution.

## Data and reporting notes

The hard-case builder now requires agreement with a blind Astra labeler by default. It retains 10,142 questions: 8,999 train and 1,143 validation. Jev second opinions do not control the retained training examples. This is a meaningful improvement over unchecked generated labels, although agreement-based filtering can preferentially remove difficult or ambiguous cases. The source-ID split and an eval-overlap filter still do not establish template-level independence.

The earlier review's test-reuse and grouping limitations still apply. The new bootstrap is a robustness check, not a fresh final evaluation. No test-only threshold fix was applied, no model was trained by this review, and no live data-generation job was modified.

Reproducible calculations: [audit_update.py](audit_update.py). Saved metrics, paired comparisons, document-bootstrap intervals, benchmark alignment, source hashes and the 34 affected CLINC IDs: [audit.json](audit.json).
