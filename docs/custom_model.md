# Custom shared-state model

This is the "encode the text once, then cross-attention + small heads" architecture from the v1 spec, built on the
same `Qwen/Qwen3-Reranker-0.6B` backbone as the stock backend. It is implemented, trained, tested and benchmarked.

**Bottom line.**
- **As specified, it scores 39.0% question accuracy** on the 3,471-question test split. For comparison, the
  unmodified stock reranker scores 61.0% and the stock reranker + LoRA 73.5%.
- **With an opt-in similarity (MaxSim) term trained jointly with LoRA, it reaches 58.2%.** It matches or beats the
  stock LoRA on Banking77 and AG News, but still loses on unseen label sets and fails on yes/no questions.
- **Speed is where it wins.** The text is encoded once per request, so with 16 questions × 3 candidates on an
  8K-token text it answers in 626 ms versus 24,024 ms on the same A10G GPU. With one short question it is about
  as fast as the stock model.

Every number below is read from the file cited next to it.

## Results (test split, 3,471 questions)

Source: `reports/<run>/test/report.json`; side-by-side table in [reports/comparison_custom.md](../reports/comparison_custom.md).

| | stock base | stock + LoRA | custom (spec) | custom + similarity | custom + similarity + joint LoRA |
|---|---|---|---|---|---|
| run | `baseline` | `lora_pilot` | `custom_frozen` | `custom_sim_frozen` | `custom_sim_lora` |
| question accuracy % | 61.0 | **73.5** | 39.0 | 48.0 | 58.2 |
| binary AUROC | 0.605 | **0.863** | 0.536 | 0.524 | 0.514 |
| multiclass accuracy % | 73.3 | **78.3** | 39.1 | 53.9 | 70.2 |
| multiclass macro-F1 % | 79.6 | **82.3** | 24.9 | 54.3 | 76.1 |
| multiclass ECE (top label) | **0.026** | 0.027 | 0.112 | 0.033 | 0.030 |
| multilabel label AUROC | 0.679 | **0.882** | 0.565 | 0.544 | 0.686 |
| multilabel micro-F1 % | 23.6 | **62.9** | 12.5 | 8.6 | 6.8 |

**Accuracy % by family.** "Unseen" families never appear in training, and neither do their label sets.

| family | n | stock base | stock + LoRA | custom (spec) | + similarity | + similarity + joint LoRA |
|---|---|---|---|---|---|---|
| hf_intent_banking77 | 300 | 89.3 | 92.7 | 57.7 | 76.0 | **93.0** |
| hf_topic_agnews | 300 | 77.3 | 86.7 | 87.7 | 81.7 | **89.0** |
| hf_sentiment_tweets | 300 | 54.3 | **66.7** | 41.7 | 45.3 | 62.3 |
| heldout_intent_clinc (unseen) | 300 | **92.3** | 89.3 | 20.7 | 61.0 | 79.3 |
| heldout_topic_dbpedia (unseen) | 300 | 89.3 | **91.7** | 25.7 | 58.0 | 81.7 |
| heldout_emotion_multiclass (unseen) | 300 | 51.0 | **56.0** | 15.0 | 27.0 | 45.3 |
| heldout_question_type_trec (unseen) | 300 | 64.3 | **68.0** | 27.3 | 31.0 | 43.3 |
| hf_nli (binary) | 300 | 56.7 | **89.0** | 63.7 | 63.7 | 64.3 |
| heldout_boolq (unseen, binary) | 300 | 59.3 | **70.3** | 41.0 | 40.3 | 41.0 |
| heldout_sentiment_sst2 (unseen) | 300 | 50.0 | **76.7** | 50.0 | 50.0 | 50.0 |
| hf_emotions_multilabel | 300 | 0.0 | **32.3** | 0.0 | 0.0 | 0.0 |

The seven `eval_*` families (17–32 test questions each) are in the full comparison table.

**Paired exact McNemar tests** (questions only one of the two models gets right; computed from the same reports):
- stock + LoRA vs custom + similarity + joint LoRA: 749 vs 217 (p ≈ 4.3e-69).
- stock base vs custom + similarity + joint LoRA: 577 vs 478 (p ≈ 0.0025).
- custom (spec) vs custom + similarity: 217 vs 531 (p ≈ 3.2e-31).

## What is computed

```
memory = LN(W_m · z(Qwen(state)))                         [S, L, 256]  each distinct state encoded once per call
q      = W_c · z(Qwen(task + question + proposed answer))  [N, Lc, 256] one short sequence per candidate, same weights
q      = q + Attn(LN(q), [null; memory]);  q = q + FFN(LN(q))     × 2 new blocks, 8 heads, FFN 1,024
score  = head(mean over the candidate's tokens of LN(q))   binary_head: binary + multilabel · choice_head: multiclass
         (+ w_type · MaxSim, only with the opt-in "similarity" flag)
```

- **Backbone.** The reranker's transformer body (`AutoModel`: 595,776,512 parameters, 28 layers, width 1,024) with
  its stock causal attention. The vocabulary head is not used and there are no yes/no logits. The state and the
  candidates never share a sequence.
- **Text format (`custom-v1`, sha `b96b6174a187`).**
  - State: `Document:\n{state}`.
  - Each candidate: `Task: {type}\nQuestion: {instruction}\nProposed answer: {description}`, where binary questions
    use the answer `Yes`.
  - Tokenized with `split_special_tokens=True`, so `<|im_end|>` typed inside a state stays plain text.
  - Sequences are right-padded, and the checkpoint refuses to load if the format changes.
- **New trainable modules (2,172,418 parameters):**

  | module | parameters |
  |---|---|
  | memory projection | 262,912 |
  | candidate projection | 262,400 |
  | 2 cross-attention blocks (including the null slot) | 1,580,544 |
  | output norm | 512 |
  | binary head | 33,025 |
  | choice head | 33,025 |

  The similarity flag adds 2 parameters. LoRA r = 16 on q/k/v/o adds 4,587,520.
- **Typed outputs.** Scores go through the same `classify.decide` as the stock backend:
  - binary and multilabel: sigmoid;
  - multiclass: softmax over the question's own candidates;
  - held-out temperatures and thresholds apply as before.
- **Sharing.** Identical states in a call are encoded once. Candidate tokens are packed per state, so K/V are
  projected once per state per block and never copied per candidate. Candidates never attend to each other.
  Every response's `meta` counts `state_sequences`, `memory_rows` and tokens, and `tests/test_custom.py` checks all
  of this.
- **Checkpoint.** A complete checkpoint holds `modules.safetensors` (all new modules plus the standardization
  buffers), `adapter/` (LoRA) or `backbone.safetensors` (full fine-tune), and `config.json` (base revision, arch,
  format). Reloading reproduced scores within 9.5e-7 to 5.7e-6 (`reload_check` in each `runs/*/train_meta.json`).

### Additions beyond the spec, each measured

| addition | why | evidence |
|---|---|---|
| Fixed per-dimension standardization `z()` of Qwen's last hidden states | Raw token states share one dominant direction: mean pairwise cosine 0.492, 47.9% of the energy in the mean direction. Standardized: 0.002 and 0.000. | `reports/custom_diagnostics/logs/features.log`. Parameter-free MaxSim, last layer: Banking77 23/40 raw vs 31/40 standardized; AG News 11/40 vs 23/40 |
| Tied random init: `W_c = W_m`, per block `Wq = Wk` (random orthogonal), `Wo = Wvᵀ` | At step 0, each candidate token attends to the most similar state tokens | Banking77 validation accuracy at step 250 on a hard mix: 17.3% untied vs 40.0% tied (`fam_mix_untied.log`, `fam_mix.log`) |
| Learnable null key/value slot in the cross-attention | Lets a candidate token express "nothing matches" instead of forced averaging | Same probe: 40.0% → 58.0% (`fam_mix_null.log`). Full mix, epoch 1 validation loss: 1.001 → 0.952 (`custom_frozen_nonull.log`, `runs/custom_frozen.log`) |
| Heads' last layer initialized to zero | The untrained model outputs logit 0 (p = 0.5, uniform softmax) instead of noise | `test_untrained_heads_start_at_logit_zero` |
| No attention mask in the backbone | Right padding plus a causal model means real tokens never see padding. An explicit mask disabled the fast attention path on MPS. | MPS, bucketed, 8K-token state, 1 × 3: 6,073 → 3,937 ms. 32K, 1 binary: 47,974 → 24,418 ms (`reports/bench/pre_mask_fix/` vs `reports/bench/custom_*`) |
| MPS-only shape buckets (round rows and lengths up; at most 25% padding) | MPS compiles and keeps a graph for every new tensor shape, so memory grew every training step | 160 training steps: heap 210 → 2,694 MB without buckets vs 214 → 914 MB with buckets, for +6.7% time (179.6 s → 191.7 s; `shapes_nobuckets.log`, `shapes_buckets_25pct.log`). Off on CUDA and CPU. |
| Opt-in `similarity` term: `score += w_type · MaxSim` | Adds a generic "does this description match the text" signal. MaxSim is the mean over the candidate's content tokens (the description, or the question for binary) of each token's best cosine match in the state, on the standardized features. `w` starts at 20 for multiclass and 0 otherwise, so the untrained multiclass scorer is exactly the parameter-free MaxSim rule. | Test accuracy 39.0% → 48.0% frozen, 58.2% with joint LoRA (table above) |

## Training runs

Source: `runs/<run>/train_meta.json` and the `configs/<run>.json` files.
- Training data: 10,112 questions (the same selection as the stock LoRA pilot: seed 13, at most 1,600 per family).
- Validation: 983 questions.
- Precision: backbone in bf16, new modules in fp32.
- Optimizer: AdamW, lr 1e-3 for the new modules (3e-4 in the `custom_lora` Stage B run) and 2e-4 for LoRA, 20
  warm-up steps, then linear decay.
- Checkpoint selection: by validation loss.

| run | where | backbone | train questions | steps | wall | best validation loss / accuracy | test accuracy |
|---|---|---|---|---|---|---|---|
| `custom_frozen` (spec) | M5 Pro, MPS | frozen | 10,112 | 1,764 (6 epochs) | 23.7 min | 0.800 / 51.2% (step 1,176) | 39.0% |
| `custom_lora` (spec, Stage B) | M5 Pro, MPS | LoRA on top of `custom_frozen` | 10,112 | stopped at 390 of 882 | — | 0.800 → 0.829 → 0.810, no gain | not evaluated |
| `custom_distill_frozen` | M5 Pro, MPS | frozen | 16,671 (+ mixed labels) | 2,028 | 39.7 min | 0.838 / 45.7% | 37.7% |
| `custom_distill_lora` | A10G, CUDA | joint (50 warm-up steps) | 16,671 (+ mixed labels) | 2,028 | 49.7 min | 0.799 / 49.7% | 39.7% |
| `custom_sim_frozen` | A10G, CUDA | frozen | 10,112 | 1,176 | 7.6 min | 0.742 / 53.7% | 48.0% |
| `custom_sim_lora` | A10G, CUDA | joint (50 warm-up steps) | 10,112 | 1,176 | 28.9 min | 0.562 / 60.1% (step 882) | 58.2% |
| stock LoRA pilot (reference) | M5 Pro, MPS | stock scorer + LoRA | 10,112 | 183 | 1.05 h | 0.435 / 74.2% | 73.5% |

"Mixed labels" means `data/distill.jsonl` (`scripts/build_distill.py`):
- Each training state gets a multiclass question whose candidates are drawn from the descriptions of all training
  families.
- Labels come from the local stock reranker + LoRA acting as teacher. 6,559 of 12,260 questions were kept (teacher
  max p ≥ 0.7).
- The pool has 4,545 train-split descriptions; 937 held-out and eval descriptions were excluded
  (`reports/custom_diagnostics/logs/build_distill.log`).
- Teacher labels are not ground truth.

## Why the spec version scored 39%

1. **It memorizes training labels instead of learning to match.** The frozen model reaches 87.7% on AG News (in
   training) but 20.7% on CLINC and 25.7% on DBpedia, whose label sets it never saw (family table above).
2. **The frozen features already match unseen labels; the training throws that away.** On 100 test questions per
   family (`maxsim_heldout_frozen.log`), a parameter-free MaxSim over the same standardized features compares to the
   trained model like this:

   | family | MaxSim, no training | trained model |
   |---|---|---|
   | CLINC | 75% | 23% |
   | DBpedia | 77% | 28% |
   | Banking77 | 71% | 53% |
   | AG News | 67% | 91% |
3. **Yes/no questions are not learned, and they drag down the rest.** Banking77 validation accuracy at step 250 is
   72.7% when trained with other multiclass families only (`fam_mc.log`), versus 40.0% when NLI (binary) and
   GoEmotions (multilabel) are mixed in (`fam_mix.log`). Binary AUROC stays between 0.45 and 0.54 in every custom
   variant. In `custom_sim_frozen` and `custom_sim_lora`:
   - the learned binary similarity weight is 0.094 and 0.076, versus 19.75 and 20.03 for multiclass;
   - the binary head's last layer has norm 0.086 and 0.121: it barely moved from its zero start.
   (Read from `runs/custom_sim_*/checkpoint/modules.safetensors`.)
4. **The training schedule is not the bottleneck.**
   - Stage B LoRA on the spec model gave no validation gain (`runs/custom_lora.log`).
   - Joint LoRA from the start on the mixed-label data scored 39.7% vs 39.0% (301 vs 276 questions only one of them
     gets right, p ≈ 0.32).
   - More label variety alone did not help either (37.7%).
5. **Giving the score a direct matching term did help.** The similarity term plus joint LoRA lifted CLINC from 20.7%
   to 79.3% and DBpedia from 25.7% to 81.7%, and gave LoRA a gradient path that improves multiclass.

## Speed

**One CUDA GPU (AWS A10G), bf16, same session, both models with an unmerged LoRA adapter.**
- End-to-end p50 latency in ms, one request at a time.
- Source: `reports/bench/gpu_{stock_base,stock_lora,custom_lora,stock_long,custom_long}_bf16/` and
  `reports/bench/gpu_environment.txt` (driver 595.91.07, torch 2.14.0+cu130, transformers 5.17.0).
- The custom model here is `custom_sim_lora`.

| state tokens | questions × candidates | stock pairs | stock base | stock + LoRA | custom + similarity + LoRA |
|---|---|---|---|---|---|
| 512 | 1 × 3 | 3 | 74 | 96 | 95 |
| 512 | 16 × 3 | 48 | 976 | 1,312 | 158 |
| 2,048 | 1 × 3 | 3 | 246 | 323 | 164 |
| 2,048 | 16 × 3 | 48 | 3,949 | 5,138 | 227 |
| 8,192 | 1 × 3 | 3 | 1,213 | 1,505 | 558 |
| 8,192 | 16 × 3 | 48 | 19,339 | 24,024 | 626 |
| 16,384 | 1 binary | 1 | — | 1,254 | 1,304 |
| 16,384 | 16 × 3 | 48 | — | 59,392 | 1,379 |
| 32,000 | 1 binary | 1 | — | 3,362 | 3,428 |

**Apple M5 Pro (MPS), bf16, same afternoon.**
- Source: `reports/bench/lora_bf16/` (stock + LoRA), `reports/bench/custom_lora_bf16_nobuckets/` (exact shapes)
  and `reports/bench/custom_lora_bf16/` (MPS shape buckets, the default).
- The custom model here is the spec architecture with an unmerged, zero-initialized LoRA adapter, so it has the same
  compute as a trained one.

| state tokens | questions × candidates | stock + LoRA | custom, exact shapes | custom, shape buckets |
|---|---|---|---|---|
| 512 | 1 × 3 | 337 | 102 | 180 |
| 512 | 16 × 3 | 6,702 | 574 | 638 |
| 2,048 | 1 × 3 | 1,496 | 534 | 664 |
| 2,048 | 16 × 3 | 25,941 | 958 | 1,150 |
| 8,192 | 1 × 3 | 7,413 | 2,952 | 3,937 |
| 8,192 | 16 × 3 | 128,583 | 3,385 | 4,496 |

- **Where the time goes.** The stock model's cost is proportional to pairs × state tokens. The custom model reads the
  state once, then adds a short sequence per candidate, so its cost barely depends on the number of questions. With
  one question on a long text, both do one pass over the same tokens and take about the same time.
- **Shape buckets on MPS** cost 11% to 76% extra latency in this table (the smallest request pays the most). Without
  them, memory grows with every new batch shape, as measured in training above.
- **MPS long-context timings drifted during the day** on this laptop, so the MPS 16K/32K rows
  (`reports/bench/custom_long_context_bf16/`) are not compared with this morning's stock run. Use the CUDA table.

## Calibration

Source: `calib/<run>.json`, fit on the calibration split, with thresholds chosen on validation.

| run | temperatures (binary / multiclass / multilabel) | binary ECE | multiclass ECE | question accuracy |
|---|---|---|---|---|
| `custom_frozen` | 1.10 / 1.16 / 0.89 | 0.148 → 0.136 | 0.112 → 0.085 | 39.0% → 38.1% |
| `custom_sim_lora` | 0.91 / 1.23 / 1.14 | 0.141 → 0.154 | 0.030 → 0.046 | 58.2% → 59.6% |

The uncalibrated similarity model is already well calibrated on multiclass (ECE 0.030). Its binary scores carry
almost no signal, so no temperature can fix them: held-out temperature scaling made its binary ECE worse
(0.141 → 0.154).

## Limitations

- **Binary is unsolved in this architecture.** Test AUROC is 0.45–0.54 in all variants, so route yes/no questions
  to the stock backend.
- **Unseen label sets are still weaker than the stock model.** Examples: CLINC 79.3% vs 89.3%, TREC 43.3% vs 68.0%.
- **Every run used one seed and one hyperparameter setting.** The Stage B run on the spec model was stopped early.
- **Eval data caveats are the same as the stock backend's.** The `eval_*` families are LLM-written and small, and the
  public sets may overlap Qwen's pretraining data.
- **Some runs are on a different machine.** The distill-LoRA and similarity runs trained on an A10G; the others on
  the M5 Pro.

## Reproduce

```bash
uv run pytest tests/test_custom.py                 # new-model tests; the 3 real-model ones load the pinned base Qwen
scripts/run_experiments.sh custom                  # spec version, frozen backbone (~24 min on the M5 Pro)
scripts/run_experiments.sh custom_distill          # mixed-label data + frozen and joint-LoRA runs
scripts/run_experiments.sh custom_sim              # similarity variant, frozen and joint LoRA, then compare
scripts/run_experiments.sh custom_bench            # CUDA speed comparison
uv run pjev classify examples/request.json --checkpoint runs/custom_sim_lora/checkpoint
uv run pjev train-custom configs/custom_lora.json  # Stage B on top of custom_frozen (spec schedule)
```

The diagnostic scripts and their logs are in `reports/custom_diagnostics/`:
- `features.py`: anisotropy and MaxSim;
- `maxsim_heldout.py`: MaxSim vs the trained model;
- `families.py`: interference and init probes;
- `shapes.py`: MPS memory;
- `mixture.py`, `generalize.py`, `overfit.py`: earlier probes.
