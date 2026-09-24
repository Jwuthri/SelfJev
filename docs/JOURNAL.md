# Journal: what is running, what happened when

**Current state** (every test result, conclusions, dead ends, open ideas to claim) lives in
[experiments.md](experiments.md). This file is the chronological part: jobs in flight and a dated log, newest first.
Times are PDT (the user's clock) unless marked UTC. Rules for every session: [AGENTS.md](../AGENTS.md).

## In flight (add a row when you start, delete it when you are done)

| job | owner session | where | since | ends |
|---|---|---|---|---|
| T5Gemma matched round-2b: correcting decoder-only targeting bug; full encoder+decoder retraining, then same-L40S controls; H100 unavailable | Codex tree latency/compact | original master; Ohio L40S `i-087b024b35cff657b` ($3.00424/h) | 2026-09-24 UTC | cap 2026-09-24 14:38:54 UTC; collect/terminate earlier |
| **owner unknown**: "selfjev-challengers-20260924" | not this session, fork or fork 2 (a Codex session?). Owner: add yourself here | AWS `i-03916322f7dd879be` g6e.4xlarge, `i-0683c5909b7440e8f` g5.4xlarge | 20:27–20:51 | ? |

## Spend so far (real cost, BYOK upstream included)

| item | cost | who |
|---|---|---|
| Jev + GPT-6 Astra on the 3,471 test questions (`reports/external/full`) | $19.34 (Jev $0.06, Astra $19.27 on the OpenAI key) | Jev classifier with Qwen reranker |
| AWS: stock 4B and 8B pipelines, one g6e.xlarge, 3.16 h | ≈ $5.89 | Jev classifier with Qwen reranker |
| AWS: 10 learning-curve runs on 8 g5.xlarge | ≈ $23 | fork 2 |
| AWS: tree LoRA-capacity ablation, 2 g5.xlarge, 21:05–21:46 and 21:05–21:59 | ≈ $1.60 | fork 2 |
| AWS: combined levers (r2b data + r=64 / + MLP), 2 g5.xlarge, 00:17–02:38 and 00:17–03:10 | ≈ $5.26 | fork 2 |
| Round-2 hard-case generation (OpenRouter) + blind Astra judge (OpenAI batch) + Jev second opinion | $22.86 + $36.24 + $0.27 | Synthetic data generation strategy |
| Latency sweep: Jev calls $0.04 + AWS g5.xlarge `selfjev-latency` 20:16–21:09 (52 min, terminated) ≈ $0.87 | ≈ $0.91 | fork |
| Round-3 data: writing (Luna $10.17, Gemini $55.30, Grok $49.06) + Astra batch judge (28.5M in / 0.93M out tokens, ≈ $165.61 at list batch prices, an upper bound) | ≈ $280 (approved ≈ $250) | fork |
| AWS 09-24: all-options box ≈ $2.90, 27B teacher box ≈ $6.20, distillation box ≈ $2.90 (all terminated) | ≈ $12.00 | fork |
| eval2 build (generation + 2 judges + Jev second opinion) | $32.72 | Synthetic data generation strategy |
| Jev scored on eval2 (`reports/external/eval2`) | $0.05 | Jev classifier with Qwen reranker |
| AWS: round-3 box `i-01e7e056786127d8e` g5.xlarge 04:24–10:17 (stopped by someone else) + g5.2xlarge 10:32–10:47 for scoring, terminated; SG, key pair deleted | ≈ $6.25 | Jev classifier with Qwen reranker |
| AWS: Instruct control box `i-093d2861dcb9d84fb` g5.xlarge, 01:10–03:36 PDT, terminated | ≈ $2.45 | Jev classifier with Qwen reranker |
| AWS: eval2 scoring box `i-08aed2c38168e5da6` g5.xlarge, 23:52–00:58 PDT, terminated; SG and key pair deleted | ≈ $1.12 | Jev classifier with Qwen reranker |
| AWS: round-2 box `i-09dfa0077851dfadc` g6e.4xlarge (tree r2 + stopped stock r2 + tree r2b), 19:04–21:18, terminated; SG `sg-0fe165a71c7b812e6` and key pair `personal-jev-gpu` deleted 23:10 (eval2 scored on the Mac instead) | ≈ $6.70 | Jev classifier with Qwen reranker |

The tree and custom-model GPU runs and the unknown boxes are not in this table yet: their owners should add them.

## Log

### 2026-09-24 11:50 PDT: docs site and cleanup (cloud session, branch `claude/modest-shannon-epq8g4`; $0, nothing run)

- **What:** every finding of the project, formatted as a docs site built with Zensical from `docs/` (`zensical.toml`,
  GitHub Pages workflow `.github/workflows/docs.yml`). New pages: `index`, `findings` (24 findings with evidence),
  `leaderboard` (embeds the generated eval2 summary and the ledger), `speed`, `dead_ends`, `stock_model`,
  `challengers`, `data`, `landscape`, `next`, `costs`, `how_it_works`, `reproduce`. Numbers copied from the generated
  tables and report files; the 27B teacher's eval2 score re-computed from `reports/teacher/qwen38_27b_eval2.jsonl`.
- **Cleanup:**
  - README rewritten as a short landing page; its detailed 0.6B/4B/8B sections moved to `docs/stock_model.md`.
  - `experiments.md` restructured: current conclusions first, done ideas moved out of the open-ideas table, and the
    ledger sorted by eval2 (`scripts/ledger.py` now sorts that way and links Jev/Astra rows to their real reports).
  - Absolute `/Users/julien/...` links in `reports/*.md` made repo-relative; `tmp/pdfs/` page renders removed; the two
    review PDFs moved from `output/pdf/` next to their sources.
- **Merge note:** other sessions edit `docs/experiments.md` and this file on `master`; merge this branch with care.

### 2026-09-24 10:45 PDT: partial round-3 checkpoint scores 90.8 on eval2, inconclusive (the run was stopped at step ≈ 500 / 915)

- Owner: Jev classifier with Qwen reranker. Scored `runs/tree_4b_instruct_r3_step300`, the best-validation-loss checkpoint
  saved before the 10:17 stop (see below). Reports: `reports/tree_4b_instruct_r3_step300/{eval2,test}`.
- Scores:

  | checkpoint | eval2 | old test |
  |---|---|---|
  | tree_4b_instruct_r3_step300 (partial) | **90.8** | 81.5 |
  | control `tree_4b_instruct_r2x64` (finished) | 92.7 | 82.7 |

- Not a verdict on round 3.
  - Step 300 of 915 had seen about a third of the 52K-question mix, at peak learning rate with no decay.
  - The control finished its schedule.
  - A full round-3 run (~10 h on an A10G, ~$10) is needed to judge the data.
- Cost ≈ $6.25. Box terminated; SG, key pair and pem deleted. Nothing of this session runs in AWS.


### 2026-09-24 10:42 PDT: Qwen3.5 / Qwen3.8 as the next base, and Eikos-4B (session "SelfJev state of play"; $0, nothing run)

- **What exists.** Qwen3.8 has no small dense model: only 27B (`qwen3_5_text`, 48 linear-attention + 16 full layers), a
  180B MoE "Flash-Next" and a 2.4T MoE. Qwen3.5 has 0.8/2/4/9/27B plus Base variants; 4B = 32 layers, 24 Gated DeltaNet +
  8 full attention, hidden 2560, 262K positions.
- **We already have a Qwen3.5 result**, in the Codex challenger worktree (`~/.codex/worktrees/1d33/SelfJev`,
  `reports/challengers/qwen35`, trainer `scripts/run_challenger.py`, scorer `src/personal_jev/challengers.py`):
  Qwen3.5-2B + LoRA r16 on all its projections (DeltaNet `in_proj_*`/`out_proj` included), shared document with the
  native cache (recurrent state + KV) forked per branch, round-1 data only. Old test **79.9%** (tree 4B 81.6, stock 4B
  80.3, 0.6B 73.5); 853 steps in 17 min on an L40S. Never scored on eval2.
- **Speed, same L40S, p50 ms** (`bench.json`): Qwen3.5-2B vs tree 4B: 512 tok × 1 q 125 vs 114; 2K × 16 q 319 vs 339;
  8K × 1 q 394 vs 805; 8K × 16 q 765 vs 1,050. Linear attention pays off only on long texts; at ≤2K the MLPs dominate.
- **Eikos-4B** (`caiovicentino1/Eikos-4B`, MIT, created 2026-09-23): a full fine-tune of Qwen3.5-4B, distilled from
  GLM-5.3-Flash on finance/rules data; options as letters, softmax over the letter logits; vLLM ≥ 0.30 with
  `--enable-prefix-caching --mamba-cache-mode all` shares the state across questions (the card reports vLLM 0.11 lost
  3–6 points on batched long shared documents). Own-harness claims: JevBench public hard 72.1 (Jev 73.0 on the official
  leaderboard), long context to 32K trained, ECE 0.033. Not comparable with our numbers.
- Proposal (awaiting the user's OK on the GPU spend): open idea "Qwen3.5-4B tree-equivalent" in experiments.md.

### 2026-09-24 10:36 PDT: survey of open "Jev-like" models on Hugging Face (session "SelfJev state of play")

- Read the model cards of the trending text-classification models; nothing downloaded or run; $0.
- Two camps. Small encoders, 0.15–0.4B: Laya (ModernBERT / mmBERT), open-jev-deberta-v3-large, rlcd-modernbert-151m
  (GLiClass), plus MLX / CoreML ports. LoRA on decoders with answer-token readout, 0.6–27B: kev 0.5/0.8/4/9B and decider
  0.8/2/4/35B-A3B (Qwen3.5 bases), openjev (Qwen3.5 0.8/2/4B), Bespoke-Nimble-9B (Qwen3.5-9B), AutoJev-27B (Qwen3.8-27B),
  Lumma-fev-0.6b (own base).
- Their claims, each on its own benchmark and not comparable with ours: AutoJev-27B 84.6 vs Jev 82.8; kev-4b beats Jev in
  distribution but trails out of domain (0.817 vs 0.857); kev-0.8b trails Jev everywhere; decider-35b-a3b JevBench hard
  0.676, decider-4b 0.541. Small models advertise speed (33–46 ms vs a quoted 236–276 ms for Jev; we measured 143–178 ms).
- Same pattern as ours: sub-1B trails (our 0.6B −17.7 on eval2, jina 0.6B 73.3), 4B and up is where quality is. Most
  decoder entries use our recipe (LoRA, logit readout, no generation). Many use Qwen3.5 bases, whose linear-attention layers
  our tree cannot branch.
- "JevBench" public items exist and several cards report on them: a shared yardstick. Open idea added.

### 2026-09-24 10:17 PDT: round-3 training box stopped by an unlogged `aws ec2 stop-instances` from this Mac

- Owner of the box: Jev classifier with Qwen reranker (`i-01e7e056786127d8e`, "personal-jev-instruct-r3", tagged, listed in
  In flight).
- What happened, per CloudTrail:
  - `StopInstances` at 17:17:57 UTC by `julien@connectly.ai`, from this Mac's IP.
  - User agent `aws-cli … md/command#ec2.stop-instances`: a CLI call, not the console.
  - No session logged it. Training was at step ≈ 500 of 915.
- Rule for every session: **never stop, terminate or modify another session's box.** Check JOURNAL In flight first; if a
  box looks orphaned, ask its owner session or the user.
- Recovery (user's choice): score the best checkpoint saved before the stop.
  - That is step 300: val loss 0.176, val acc 89.2%. Step 500 was 0.178 / 89.2, so it wasn't saved.
  - The box restarted as a g5.2xlarge, since its AZ had no g5.xlarge capacity. Results in the next entry.
- Validation trajectory: 78.5 (init) → 85.3 (100) → 87.8 (200) → 89.2 (300) → 89.5 (400) → 89.2 (500).
  - This validation set includes round-3 questions, so it does not compare with the control's 85.8.

### 2026-09-24 10:32 PDT: review of Laya (NandhaKishorM/laya), an open "Jev-style" engine (session "SelfJev state of play")

- What: read the repo (README, BENCHMARKS pointers, `laya/common.py`, `laya/agent.py`) at commit `970dc8c`. Nothing was run
  or downloaded beyond the git clone; $0.
- Architecture: a bidirectional encoder (ModernBERT-large 421M for English, mmBERT-base 322M multilingual), one sequence per
  question `[CLS] type question [SEP] [MASK] opt0 [MASK] opt1 … [SEP] state [SEP]`, all options in one listwise row. A new
  2-layer transformer head + MLP scores each `[MASK]`; softmax over options. `noul` is a 2-option choice (false/true),
  `score` a softmax over levels. Trained end to end with a GRPO-style policy gradient on proper-scoring-rule rewards
  (log + spherical + RPS), which they call RLCD. A script/language router picks one of three checkpoints.
- Limits it documents: the state is **truncated** to max_len − head_max_len (≈320 tokens on `laya`, ≈768 on multilingual;
  up to 8K opt-in), options share a 192–256-token budget (Banking77 0.425 vs Jev 0.870), base checkpoints are near chance
  zero-shot on its own typed-decisions set (0.36 vs 0.318 random; 0.766 only after fine-tuning on that set's train split),
  negation and `noul` label-following failures, over-confident before temperature fitting (ECE 0.466 → 0.081).
- Its Jev numbers are third-party published, on different samples and prompts: not comparable with ours. Its Jev latency
  (236–276 ms p50) is slower than what we measured (143–178 ms, `reports/latency/summary.md`).
- Relation to our work: the listwise idea (a candidate sees its alternatives) is what `tree_4b_ova` added (+1.0 on eval2).
  The new-head-on-encoder idea resembles our custom model, but Laya keeps state and options in one sequence, so they
  interact in every layer. Closest measured analogue: our jina v3.5 0.6B listwise run, 73.3 on eval2 (`docs/jina_model.md`).
- Verdict: Laya is the faster and multilingual option (≈33 ms on a T4, CPU/ONNX), not the more accurate one on long,
  trap-heavy texts; ours reads up to 32K tokens untruncated. Expected, not measured: well below our 92.7 on eval2. Scoring
  it on eval2 is free on the Mac and is logged as an open idea.

### 2026-09-24 06:20 PDT: distilling the 27B into the tree does not help (fork session)

- Run: `tree_4b_ova_kd`, the tree_4b_ova recipe with `teacher_weight` 0.5 and `data/teacher/qwen38_27b_ova_train.json`.
  - The teacher file holds Qwen3.8-27B-FP8 zero-shot probabilities on the 8,372 target-task training rows and gold on
    the 8,000 hf rows.
  - Hardware: g5.xlarge, 241 steps, ≈ $2.90, box terminated.
- Scores vs tree_4b_ova (the same run without the teacher):
  - Old test: 82.5 vs 82.6 (45 / 50, p = 0.68).
  - eval2: 91.0 vs 91.6 (33 / 45, p = 0.21). By type: multiclass +0.7, binary −0.9, multilabel −1.9.
  - Validation: 86.1 vs 86.2.
- Verdict: the 50/50 ensemble's +2.9 on eval2 (94.5%) does not transfer through soft targets on the training rows.
  - Where the teacher disagrees with the verified label (12–20% of rows), the 0.5 weight pulls toward a wrong answer.
  - Untested variants: teacher on multiclass only (where it is strongest), a lower weight, the r64 student.
  - Logged as a dead end for this setting in experiments.md.

### 2026-09-24 04:22 PDT: round-3 data built (38.6K verified), all-options wins, the 27B teacher is complementary (fork session)

- **04:22 (09-24): round-3 training data built: `data/hardcases_r3.jsonl`, 38,628 verified questions** (fork; sha256
  `d20ecb98…`; review `data/hardcases_r3/review/REVIEW.md`).
  - Writers, via `gen_hardcases.py --round3`: GPT-6 Luna 23,336, Gemini 3.8 Flash 9,772, Grok 4.7 5,520 (60/25/14%).
    Never eval2's writers or its NOVEL_* domain lists.
  - Blind Astra judge (OpenAI Batch): 97.0% agree with the authors (simple 98.8, hard 96.5, very hard 95.6). Only
    agreements are kept. 0 states dropped by the 8-gram guard vs eval.jsonl + eval2.jsonl.
  - Splits: train 34,868 / validation 3,760. Types: binary 16,770 / multiclass 12,402 / multilabel 9,456.
  - "None" correct in 7.0% of the multiclass questions offering a none-like option (round 2: 28%); 54% of multilabel
    questions have 3+ positives (round 2: 21%).
  - Cost ≈ $280 (writing $114.5, judge ≈ $165.6 at list batch prices, $4.16 per 1K questions) vs ≈ $250 approved.
  - Training on it: owned by "Jev classifier with Qwen reranker" (Instruct base, r64). Remember `cap_exempt_families` for
    r2_*/r3_*.
- **03:25 (09-24): the 27B teacher is as good as our best model on eval2, and its errors differ from ours** (fork;
  `reports/teacher/`). eval2 is used here for reporting only: nothing was tuned on it.
  - Qwen3.8-27B-FP8 zero-shot on eval2: **91.4%** (binary 93.4, multiclass 97.8, multilabel 75.9); tree_4b_ova 91.6%.
  - Paired: 112 questions only ours gets right, 108 only the teacher (p = 0.84). Either one right: 97.0%.
  - A fixed 50/50 average of the two models' probabilities (nothing fitted) scores **94.5%** (binary 95.7, multiclass 98.5,
    multilabel 85.1); Jev scores 97.2%. That is the case for distillation.
  - Training split: the teacher scored 22,893 of 22,919 train rows (26 overlong), agreeing 80.1% with the labels.
    - Teacher file: `scripts/teacher_scores.py teacher-file --gold-families hf_`. The hf rows keep gold targets
      because the teacher is weaker on them on validation (69.7%).
  - Cost: g6e.xlarge us-east-2 07:06–10:26 UTC ≈ $6.20. Box terminated; SG and key pair deleted.
- **02:45 (09-24): all options listed in the question wins on both test sets** (fork; `tree_4b_ova`).
  - What: `scripts/options_in_question.py` lists every candidate in the question text, in a fixed random order per
    question ("one vs all in context"). Each leaf still judges one candidate, but now sees all the alternatives.
    - The r2b recipe is otherwise unchanged (`scripts/run_tree_ova.sh`, `data/ova/`, same 1,600-per-family cap).
    - 154 overlong questions were dropped at max_length 8192.
  - Old test (3,471 q): **82.6%** vs r2b 81.2% (130 vs 82, p = 0.001), vs tree_4b 81.6% (p = 0.02), vs Jev 82.7%
    (p = 0.93, tied).
    - By type vs r2b: multilabel 57.8 vs 51.7, multiclass 83.6 vs 82.8, binary 89.2 vs 88.1.
  - eval2 (1,991 q): **91.6%** vs r2b 90.6% (66 vs 46, p = 0.07); Jev 97.2%. Every type is 0.8–1.6 points up.
  - Validation: 86.2 vs 86.1, loss 0.234 vs 0.247.
  - Caveat: one run each. Binary rows, which the transform leaves unchanged, also moved ~1 point, so part of the gain may
    be run-to-run variance.
  - Inference must apply the same transform to requests.
  - Cost: g5.xlarge 23:53–02:46 ≈ $2.90. Box terminated; SG and key pair deleted.
  - The round-3 owner decides with the user whether round 3 uses it.
- **01:30 (09-24): Qwen3.8-27B-FP8 zero-shot as a soft-label teacher, validation check** (fork;
  `scripts/teacher_scores.py`, AWS us-east-2 L40S; scores in `reports/teacher/qwen38_27b_validation.jsonl`).
  - Method: vLLM, thinking off; the answer probability is read from the next-token distribution restricted to the answer
    tokens.
  - Validation, 2,121 questions (hf, synthetic, eval and hardcases validation rows): 82.4% overall.
    - by file: hf 69.7%, synthetic 98.2%, eval (authored) 93.2%, hardcases (Astra-verified) 88.1%;
    - by type: binary 89.4, multiclass 88.4, multilabel 61.1.
  - Same 868 hf + eval validation questions: our r2b 79.8% vs the teacher 72.9% (115 vs 55, p = 5e-6).
    - On the 118 authored ones the teacher leads: 93.2% vs 83.1%.
    - It loses on public-set label conventions and wins on target-task questions.
  - Its probabilities are graded (23% of values within 0.05–0.95, vs 0.8% for Astra's verbalized ones), so it is usable as
    a soft-label teacher for the target-task rows, not the public-set rows.
  - It agrees with Astra-verified labels on 88.1% of hard cases, so it cannot replace Astra as the checker.
  - Its training-split scores are running (for a later, separate distillation ablation, not the round-3 run). A reference
    eval2 score (test: reporting only) follows.

### 2026-09-24 03:35 PDT: Instruct base + round-2 data + r64 scores 92.7 on eval2, the best of our runs

- Owner: Jev classifier with Qwen reranker.
- Run: `tree_4b_instruct_r2x64`, the control for round 3.
  - Recipe: `configs/tree_4b_instruct_r3.json` with `R3=0`: Qwen3-4B-Instruct-2507, tree, LoRA r64 on q/k/v/o, max_length 8192.
  - Data: hf + synthetic + `hardcases_nb`, with the r2_* families uncapped. 18,681 questions, 218 steps.
  - Hardware: AWS g5.xlarge, MBT 8192 × GA 4, about 2.3 h. Cost ≈ $2.45, box terminated.
  - Best checkpoint: the last one (val loss 0.226, 85.8%); reload exact.
- Scores:

  | eval2 | overall | binary | multiclass | multilabel EM |
  |---|---|---|---|---|
  | tree_4b_instruct_r2x64 | **92.7** | 94.6 | 95.4 | 83.5 |

  - Old test: 82.7, identical to Jev (213 / 214, p = 1).
- Paired tests on eval2 (only-row / only-other):

  | vs | only-row / only-other | p |
  |---|---|---|
  | r2b | 90 / 47 | 0.0003 |
  | tree_4b_ova | 78 / 55 | 0.06 |
  | r2b + r64 + MLP | 87 / 59 | 0.03 |
  | Instruct base on round-1 data (88.1) | 123 / 32 | 9e-14 |
  | Jev | 25 / 115 | 5e-15 |

- Verdict: the Instruct base stacks with the data. Most of the gain over r2b is the base, since r2b + r64 alone gives
  90.3.
- Jev still leads by 4.5 points, with multilabel EM 94.2 vs 83.5 the biggest gap.
- Round 3 uses the same recipe plus `data/hardcases_r3.jsonl`.

### 2026-09-24 03:17 PDT — combined levers: round-2b data + LoRA capacity

- Owner: fork 2. Two g5.xlarge (no g6e capacity), max_batch_tokens 8192 × grad_accum 4 (same 32K effective batch), 208
  steps each; ≈ $5.26; both boxes terminated, SG and key pair deleted. Configs `configs/curve/tree_4b_r2b_r64*.json`,
  runner `scripts/run_curve.sh` (tree_* branch now also scores eval2); tables `reports/curve/summary.md`,
  `reports/eval2/summary.md`, ledger.
- `tree_4b_r2b_r64` (r=64, 47.2M params): eval2 **90.3%** vs 90.6 for r2b (44 / 50, p = 0.61); old test 81.2 (= r2b);
  validation 86.6. The +2.1 that r=64 gave on round-1 data is gone on round-2b data.
- `tree_4b_r2b_r64_mlp` (r=64 + gate/up/down, 132.1M params): eval2 **91.3%** (59 / 44 vs r2b, p = 0.17); old test **82.4**
  (129 / 88 vs r2b, p = 0.0065; best old-test score of any of our models); validation **87.0** (best). vs Jev 26 / 144,
  p = 5e-21; Jev 97.2.
  - Slices vs r2b: binary 93.7 vs 92.9, multilabel EM 80.4 vs 78.8, multiclass 94.3 vs 94.1; very-hard tier 89.6 vs 86.5;
    by author Opus +1.1, GLM +1.3, Kimi −0.2; every trap tag with n ≥ 150 improves (+2 to +4: paraphrase, injection,
    numeric, long_state, temporal). Small everywhere, significant nowhere: consistent with a real but sub-point gain,
    not with style overfitting.
- Verdict: capacity and verified data overlap; the best recipes today are r2b data + r=64 + MLP (91.3 eval2) and the fork's
  `tree_4b_ova` (91.6, options listed in the question), within noise of each other and 6 points below Jev. The remaining
  gap is not a capacity or volume problem; it needs data or format changes aimed at the very-hard tier and multilabel
  (80 vs 94). Instruct base + round-2 data + r=64 is training in the "Jev classifier with Qwen reranker" session.

### 2026-09-24 08:17 UTC: T5 adaptation scope correction; initial pilot was decoder-only

- Owner: Codex tree latency/compact. The initial target filter missed native `model.encoder.text_model.layers`; the first adapter has 208 decoder tensors, zero encoder tensors, 2,981,888 trainable parameters. Earlier entries describing full text adaptation are superseded by this audit.
- Initial 73.84% development / 76.80% eval2 and 266.61 ms primary latency remain valid **decoder-only** measurements, archived in `reports/t5_round2b_2026-09-24/decoder_only_audit/`. They cannot decide the intended full-adaptation experiment. Historical R1 reproduction remains valid: all 3,471 old decisions match, 75.37%; eval2 72.98%.
- Fixed exact module coverage and added an actual native full T5 + PEFT unit test, plus independent encoder/decoder first-step gradient audits. Rerun uses `configs/t5gemma2_r2b_full.json`, the unchanged frozen 16,375/1,388 questions, seed and recipe. Correction was discovered after evaluation; no evaluation labels enter training or checkpoint selection.
- H100 attempts failed in all Ohio zones; no instance launched, no H100 compute charge. Corrected smoke/training use our existing L40S `i-087b024b35cff657b`, $3.00424/hour, with the original termination cap. Other sessions' resources untouched.

### 2026-09-24 01:00 PDT: eval2 re-scoring. The Instruct base and rank 64 help on the real task; 0.6B is far behind

- Owner: Jev classifier with Qwen reranker.
  - Scored on AWS g5.xlarge `i-08aed2c38168e5da6`, ≈ $1.12, terminated; SG and key pair deleted.
  - The Mac run was stopped at the user's order: no evals or training on the laptop, now in AGENTS.md.
  - Table: `reports/eval2/summary.md`; lever table in `experiments.md` (eval2 section).
- eval2 accuracy, all trained on round-1 data unless noted:

  | model | eval2 acc % | old test |
  |---|---|---|
  | tree_4b_r2b (round-2 data) | 90.6 | 81.2 |
  | tree_4b_r2 (round-2 data) | 90.4 | 80.6 |
  | **tree_4b_instruct** | **88.1** | 80.4 |
  | **tree r64** | **87.2** | 81.5 |
  | stock 4B pairs | 86.5 | 80.3 |
  | tree + MLP targets | 86.3 | 81.6 |
  | tree_4b | 85.1 | 81.6 |
  | 0.6B stock | 68.8 | 73.5 |

- Paired tests vs tree_4b (only-row / only-ref):

  | model | only-row / only-ref | p |
  |---|---|---|
  | Instruct base | 129 / 69 | 2e-5 |
  | r64 | 77 / 36 | 1e-4 |
  | MLP targets | 62 / 38 | 0.02 |
  | stock pairs | 129 / 101 | 0.08 |

- The old test ranked these the opposite way, or called them ties.
- Round 2 vs r2b: equal overall. r2 is better on multiclass (95.8 vs 94.1) and r2b on multilabel (78.8 vs 75.4). The
  "none" cap only mattered for CLINC.
- Verdict: three independent levers measured one at a time: data +5.5, Instruct base +3.0, rank 64 +2.1.
  - fork 2's combined run (r2b data + r64) uses the reranker base. An Instruct-base + r2b-data (+ r64) run is the
    missing combination.
  - The 0.6B size is out for quality: −17.7 vs stock 4B.

### 2026-09-24 07:58 UTC — T5 matched-R2b pilot: quality shortfall

- Owner: Codex tree latency/compact. Training completed in 3,685 seconds, 228 steps; best validation loss selected the final checkpoint (77.59% validation accuracy, loss 0.379396). Reload matches scores exactly on 32 validation questions. Adapter SHA256 `4c4d1f9d683052f0f2b32196f409a9b46a250255ae84caf49b3288131bfa9c43`, saved locally at `runs/t5gemma2_r2b/adapter/`.
- Fixed unmerged T5 with bounded 16-branch decoder batches: **73.84%** on the 3,471-question development benchmark, **76.80%** on eval2 (1,991 questions); primary same-L40S local latency **266.61 ms p50 / 269.38 ms p95**, 100 fresh-prefix 2K × 16 × 3 requests. [Predictions](../reports/t5_round2b_2026-09-24/decoder_only_audit/t5_r2b/eval2/report.md), [timings](../reports/t5_round2b_2026-09-24/decoder_only_audit/t5_r2b/bench.json), [protocol](../reports/t5_round2b_2026-09-24/README.md).
- Verdict so far: large quality shortfall versus the existing round-2b eval2 report (90.56%); this pilot is not a replacement. Same-GPU tree controls, old-T5 rescore, merged/prefix-cache treatments and conditional hardware follow-up are still running. No test-driven retraining or checkpoint change. Compute spend and resource cleanup remain in progress. Ledger refreshed from report files.

### 2026-09-24 07:19 UTC — prior T5 experiment found; matched round-2b follow-up underway

- Owner: Codex tree latency/compact, original `master`. The user correctly recalled the earlier T5Gemma 2 experiment in the challenger worktree. It already used the pretrained full encoder/decoder and shared cross-KV: 75.37% old development accuracy versus R1 merged tree 81.50%, and 203 versus 297 ms on its L40S 2K × 16 × 3 benchmark. The preceding architecture memo now carries a correction. Historical reports/hashes are preserved under [the new experiment folder](../reports/t5_round2b_2026-09-24/README.md).
- Matched-data pilot: replayed original R2b sampling/length eligibility exactly, 16,375 train / 1,388 validation questions; all original file hashes match. No train/validation overlap in IDs, source IDs or exact states. One epoch, attention LoRA rank 16, LR 2e-4, 228 larger optimizer updates; checkpoint selection by validation loss. This does not isolate data from training recipe compared with the old T5 run's 823 updates.
- Prototype: bounded decoder batches, view-based document cross-cache, optional native decoder common-prefix sharing. 26 local checks pass; real pretrained FP32 independent/shared inference error <= 0.000014. Current validation at step 100: 73.20% question accuracy, loss 0.445829; initial validation 37.25%, loss 1.006185. No new development/eval2 result yet; 2× speed / <=1 pp quality-loss gate is pending. Source snapshots, checks, exact requests and progress are saved in `reports/t5_round2b_2026-09-24/` and `runs/t5gemma2_r2b/`.
- Cloud: user explicitly authorized GPU provisioning in the conversation. Dedicated Ohio L40S `i-087b024b35cff657b`, verified $3.00424/hour, eight-hour terminate-on-shutdown cap at 14:38:54 UTC. Virginia capacity attempts launched no instances; their temporary SG and key are deleted. Final cost and Ohio cleanup pending.

### 2026-09-24 00:11 PDT — correction: LoRA capacity does help, on eval2

- Owner: fork 2. My 22:00 verdict "capacity is not the ceiling" was measured on the old test only and is wrong for the
  target task. Recomputed from the prediction files: on eval2, `tree_4b_r64` scores **87.2%** (77 / 36 vs `tree_4b`,
  p = 0.00014) and `tree_4b_mlp` **86.3%** (62 / 38, p = 0.021) vs 85.1%, with the same adapters that tie on the old test
  (81.5 / 81.6 vs 81.6). The trainer's validation split predicted the ranking; the old test did not.
- Updated: `docs/experiments.md` (conclusion 2, dead-end row struck, idea status), `reports/curve/summary.md` (eval2
  columns in the tree-capacity section, generated), the ledger table (new eval2 column, `scripts/ledger.py`), README.
- Proposed next run (needs the user's OK): round-2b data + r=64 (and + MLP), one A10G each, ≈ $3 each; the two gains have
  only been measured separately. Cost of this correction: $0.

### 2026-09-24 06:27 UTC — next architecture recommendation

- Owner: Codex tree latency/compact. Reviewed current eval2, controlled latency, previous cross-attention implementation, and primary model/paper sources. Recommendation: pretrained encoder–decoder with shared full-token memory and pretrained independent readers; T5Gemma 2 1B–1B is the proposed pilot, with the other session's smaller-tree work as control.
- Evidence and bounded protocol: [architecture memo](../reports/architecture_next_2026-09-24.md). Current eval2: round-2b 90.6% versus Jev 97.2% (`reports/eval2/summary.md`). Current compact experiment's speed gain is 7.4% (`reports/latency_optimization_2026-09-24/acceptance.json`). No proposed architecture has been trained or benchmarked here.
- Findings: our tree already shares the document and avoids generation; the prospective gain must come from cheaper pretrained token processing. The old two-block custom reader does not test a deeply pretrained encoder–decoder. More questions still require more arithmetic. Jev's exact internals and training origin remain undisclosed in the official announcement.
- Cost: $0 new cloud/API spend. Verdict: research proposal only; no new branches, commits, GPU instances or model downloads. Eval2 must stay out of tuning, with a fresh final confirmation set after these test-informed choices.

### 2026-09-24 06:17 UTC — latency/compact work integrated into original master

- Owner: Codex tree latency/compact. At the user's request, moved this session's completed experiment into the original `master` checkout, preserving the newer source and concurrent edits. No new commits. Removed only this session's extra branch/worktree; the other experiment's worktree remains.
- Code and results: [conclusions](../reports/latency_optimization_2026-09-24/conclusions.md), [integration record](../reports/latency_optimization_2026-09-24/integration.json). Compact weights are at `runs/tree_4b_compact_v2/adapter`. Archived the former worktree and its Git history in `runs/latency_optimization_2026-09-24/integration_archive` and verified every one of its 597 regular files. Verified all 24 migrated model/metadata files.
- Verification in the original checkout: 16 focused tree/compact tests passed, 2 real-model tests excluded (previous GPU evidence is in the experiment report). All 190 preexisting files outside the explicitly updated documentation remained byte-identical.
- Completed experiment findings are now available to the other sessions: direct branch-mask allocation preserves scores; vLLM's development quality was checked; compact training reduces branch tokens but fails the predeclared 15% cold-prefix vLLM speed-improvement gate and increases CLINC over-rejection. See measured tables and raw predictions in `reports/latency_optimization_2026-09-24/`. These runs use R1 and have not been evaluated on eval2.
- This session owned `i-0172e64b9d0dc20ac` (`selfjev-tree-compact-20260924`); it is terminated and its security group/key pair are deleted. Root EBS deletion remains asynchronous (`cleanup.json`). The two `selfjev-challengers` instances belong to another session. Faster GPU launches failed due to capacity/quota; no faster-GPU measurements exist from this experiment.
- Cost of this integration: $0 new cloud/API spend. Prior experiment billing has not been reconciled. Verdict: all further work stays in the original branch; compact remains experimental.

### 2026-09-24

- **01:30–02:00: jina-reranker-v3.5 (0.6B, listwise) trained the tree-r2b way** (Synthetic data generation strategy;
  write-up `docs/jina_model.md`, box `selfjev-jina-20260924` g5.xlarge $1.006/h, ≈ 1.5 h ≈ $1.60).
  - What: new backend `jina.py` (state = query, every question/candidate = a passage in one causal context, logit =
    scale·cos(proj(query), proj(passage)) + bias; LoRA r=16 on q/k/v/o + the projector + 2 head scalars), trainer
    `train_jina.py`, `pjev --jina` / `train-jina`, config `configs/jina_r2b.json` = the r2b recipe (hf + synthetic +
    hardcases_nb, max_length 8192, 1 epoch). 16,301 train questions / 11,774 contexts, 346 steps, 72 min on the A10G.
  - Numbers: validation 77.4 (tree 4B r2b 86.1); old test 76.6 (calibrated 75.9; 0.6B Qwen LoRA 73.5, tree 4B r2b 81.2);
    **eval2 73.3** (tree 4B r2b 90.6, Jev 97.2): binary 79.8 / multiclass 83.5 / multilabel EM 40.1; simple 80.6 / hard
    70.7 / very hard 68.5. Zero-shot 58.6 validation, 46.5 eval2. Reload check 0.0.
  - Verdict: behaves like the 0.6B Qwen reranker, not like the 4B: ≈ 17 points behind the tree on eval2, multilabel and
    long/distractor/injection cases worst. Its late-epoch gains equal the 4B's, so it is a slower learner from a lower
    start, not a steeper one. Speed on the same A10G, eval2: jina 58 ms per question vs tree 4B r2b 118 ms
    (`reports/tree_4b_r2b_gpu/eval2_timing`, 90.4 there): only 2× faster for 17 points less. License CC BY-NC 4.0: experiments only.
  - Follow-ups prepared, not run: `configs/jina_r2b_e2.json` (2 epochs), `configs/jina_r2b_r64.json` (r=64 + MLP),
    `scripts/run_jina_followups.sh`.
- **00:40: judge_hardcases.py made crash-safe for large runs** (Synthetic data generation strategy): `submit()` saves
  `review/batches.json` after every chunk and stops cleanly on an OpenAI error (e.g. enqueued-token limit), so a rerun
  submits only the remaining sources instead of paying twice. Pitfall list for the round-3 run sent to the fork session
  (judge ≈ $3.40 per 1K questions ≈ $135 for 40K; Grok 4× Gemini per state; one judge process per review dir; one
  generator per prefix; check the none-correct rate after the build).

- **23:05: first eval2 scores: the round-2 data is worth +5.5 points on the real task, and Jev leads by 6.6**
  (session "Jev classifier with Qwen reranker"; table `reports/eval2/summary.md` via `scripts/eval2_summary.py`).
  - Scores: Jev 97.2%; tree_4b_r2b 90.6%; tree_4b 85.1%.
  - Paired tests: r2b vs r1 142 / 34 (p = 7e-17). r2b vs Jev 24 / 157 (p = 4e-25).
  - Multilabel exact match: 63.9 → 78.8, Jev 94.2.
  - Very-hard tier: 79.8 → 86.5, Jev 96.5.
  - Traps, r1 → r2b (Jev):
    - improved: multi-positive 67 → 80 (96), numeric 67 → 79 (92), temporal 70 → 78 (89), injection 72 → 82 (97),
      sarcasm 72 → 83 (97), distractor 80 → 88 (97);
    - unchanged: paraphrase 83.5 → 83.9 (95).
  - Text length is not a weakness: 1K–4K tokens scores 93.9, >4K 91.6.
  - By author: Opus-written questions are hardest for us (87.7), Kimi's easiest (93.4).
  - Takeaways:
    - The old test's near-tie was a public-label-noise ceiling.
    - Verified target-task data is the lever the old test could not see. The round-1 "saturation" and dead ends need
      re-checking on eval2.
  - How it was scored:
    - `scripts/run_eval2.sh` on this Mac (MPS bf16, `--max-length 16384`), about 22 min per tree model.
    - Jev via `compare_external.py --data data/eval2.jsonl --ours tree_4b/eval2 --only jev --tag eval2`, $0.05
      (a re-run on the corrected file came from cache for $0).
    - tree_4b and r2b were scored on the first export and their ids remapped (`meta.remapped_to`), after checking
      every target, type and candidate list.
- **≈ 21:20–23:40: eval2, the frozen target-task test set, built** (session "Synthetic data generation strategy";
  `data/eval2.jsonl`, sha256 `2fa954592d0a3124…`, review `data/eval2/REVIEW.md`, human spot-check `data/eval2/review/SPOTCHECK.md`).
  - What: 1,991 questions / 647 states, every row split=test. Authors never used for training data: Claude Opus 5.5
    (560 q, $13.05), Kimi K3 (649 q, $5.55), GLM 5.3 (782 q, $2.81). Tiers 673 / 664 / 654 (hard / simple / very hard);
    lengths 177–222 questions per bucket of the 8 → 8K ladder; types 1,016 binary / 593 multiclass / 382 multilabel;
    per-trap n 57–474 (evidence_start 17); multilabel with 3+ positives 245 of 382; `none` offered in 391 multiclass
    questions and correct in 14.8% of them. A third of the calls used domains, genres and instruction styles absent from
    the training brief.
  - Judges: GPT-6 Astra (OpenAI batch, $7.95) and Gemini 3.1 Pro (sync, $3.32), blind; kept only where both equal the
    author: 1,991 of 2,070 (96.2%; Astra alone 97.5%, Gemini alone 97.0%). 0 states dropped by the 8-gram guard.
  - Jev on eval2 (never used for keep/drop): **97.2%** (Jev $0.05; the other session's compare_external run agrees,
    1,981 of 1,991 decisions identical, the rest is Jev's own run-to-run noise). Weakest: numeric, temporal, multilabel.
    On the old test Jev scores 82.7, so most of that gap was public-set label noise.
  - Correction 00:10: the first export (sha `f18549eb…`) used source-format lines, which renumber question ids after a
    drop, so my review answers no longer joined and I reported Jev 95.2%. The file now holds expanded rows with the raw
    ids (sha `2fa95459…`, same 1,991 questions and targets); `data/eval2/review/id_map_sourceformat_to_real.json` remaps
    reports scored on the first export.
  - Cost: $32.72 total, all API. Scoring of tree r1 / r2 / r2b, stock 4B and Jev on eval2 is the other session's job.
  - Verdict: usable now; still LLM-verified only, the 50-question SPOTCHECK is for the user.

### 2026-09-23

- **23:35: what TypeSafe discloses about Jev** (fork; public web, no spend).
  - Architecture: per MarkTechPost, TypeSafe says Jev is "transformer-based, but it is not a large language model",
    with a "new model architecture, parallel sampler": all outputs come from one pass, with no token-by-token
    generation.
  - Questions run "in parallel and in isolation against the same state" (docs).
  - Limits: "64k tokens per request; 32k tokens for `state` plus the longest question" (docs/models); rate limit
    250K tokens/s. This is the shape of our tree: each question sees the state plus itself.
  - Training: "Reinforcement Learning for Calibrated Decisions (RLCD)", with no details. Their benchmark's reference
    answer is the average of GPT-6 Astra and Fable 5.1.
  - Not disclosed: size, base model, data, context details. They "cannot prove the price is unsubsidized".
  - Sources: typesafe.ai/blog/introducing-system-one-models-and-jev, docs.typesafe.ai/models.md,
    marktechpost.com/2026/09/19/typesafe-ai-releases-jev/.
  - Reading, with our own evidence:
    - the gap is mostly training, not architecture;
    - model 4B → 8B, adapter r64/MLP and stock → tree each moved ≤ 1.3 points, while 10K verified target-task
      questions moved eval2 +5.5;
    - candidates next: soft Astra targets (already paid for), more verified data, a listwise choice branch.
- **23:15: how Jev stays flat** (fork; free analyses of data already paid for).
  - Fit on the 400 Jev requests of the latency sweep: time = 132–137 ms fixed + 2.2–2.6 ms per 1,000 input tokens.
    That is ~400K tokens/s of marginal speed for one request; our tree 4B with vLLM on the A10G does 165 ms per 1,000
    tokens (~6K tokens/s).
  - Jev reads the whole text:
    - on the verified round-2 hard cases (`data/hardcases.jsonl` × `data/hardcases/review/jev_answers.jsonl`), it is
      right on 97.2% of the 107 questions tagged `evidence_end` whose text is over 4K tokens (up to 17.6K);
    - start and middle score 96.8% and 98.8%;
    - its accuracy by text length is 94.7% up to 256 tokens and 97–98% from 2K to 8K+.
    - So it doesn't truncate.
  - Reading: every architecture must touch each token, so the flat curve means a very small cost per token, not "no
    attention". Consistent with a ~0.5–1B-parameter model (or an MoE with ~1B active parameters) on H100/B200-class
    GPUs, or a larger model split over several GPUs.
  - Jev's billed token count for our text is 1.036× Qwen's, so it probably doesn't use the Qwen tokenizer.
- **21:17: tree 4B round 2b result: 81.2%** (`runs/tree_4b_r2b`, `reports/tree_4b_r2b`; box terminated, ≈ $6.70 for
  all of round 2).
  - Overall: vs round 1 81.6 p = 0.39, vs round 2 80.6 p = 0.08, vs Jev 82.7 p = 0.02. Calibrated: 80.9.
  - CLINC is back to 92.0% (round 1: 94.7, round 2: 83.3). In-scope requests sent to `none`: 24 (16, 50).
  - Authored slice: 83.0% (round 1: 78.4, round 2: 81.9, Jev: 94.7).
  - Traps vs round 1: temporal 52 → 69, numeric 44 → 69, multi-positive 44 → 51, long state 76 → 84,
    exception 29 → 57 (small n).
  - TREC dropped 88.7 → 84.7: numeric/description questions sent to `entities`. Cause unknown; single seed.
  - Outside CLINC, rounds 1, 2 and 2b score 80.35 / 80.35 / 80.23. The round-2 data changes only what this test
    barely measures.
  - Verdict: keep `tree_4b` as the aggregate reference. `tree_4b_r2b` is the candidate for the target task, and
    eval2 decides. The CLINC fix came from a test diagnosis.
  - Scripts: `scripts/rebalance_nota.py`, `scripts/run_tree_r2.sh`.
  - Ready for eval2: `scripts/run_eval2.sh` (our 4B models, `--max-length 16384`), and
    `scripts/compare_external.py --data data/eval2.jsonl --ours <run>/eval2 --only jev` for Jev on the same questions.
- **21:10: latency and cost vs Jev, text 8 → 4,096 tokens** (fork; `scripts/latency_sweep.py`,
  `src/personal_jev/vllm_tree.py`; tables in `reports/latency/summary.md`).
  - Setup:
    - the same decisions-API requests from the Mac (California), one at a time, endpoints in random order;
    - Jev through OpenRouter (edge 12 ms away) vs our tree 4B + LoRA (`runs/tree_4b`) on one AWS A10G in us-east-1
      (71 ms away);
    - 1 or 16 choice questions × 3 options, 10 timed rounds, fresh random text each time.
  - Jev: flat 143–178 ms p50 at every size, including 4,096 tokens × 16 questions. OpenRouter's server timing
    (OpenRouter + Jev) is 109–154 ms.
  - Ours, p50 from the Mac (8 → 4,096 tokens):

    | server | 1 question | 16 questions |
    |---|---|---|
    | transformers | 196 → 1,062 ms | 688 → 1,700 ms |
    | transformers, merged LoRA (`--merge`) | 153 → 938 ms | 602 → 1,517 ms |
    | vLLM | 120 → 755 ms | 336 → 1,195 ms |

  - vLLM beats Jev end to end up to 128 tokens with 1 question (120–133 vs 143–165 ms), despite the 71 ms network
    handicap. Jev is 5× faster at 4,096 tokens and 2–7× faster with 16 questions.
  - The A10G is the limit: it processes 6.5–10K tokens/s with vLLM (4.7–6K with transformers). Jev's flat curve means
    its compute for about 6K tokens takes tens of ms: much faster GPUs, a smaller model, or both.
  - Cost with the GPU fully busy ($1.006/h):
    - vLLM $0.005–0.27 per 1,000 requests vs Jev $0.016–0.27: 1.3–3× cheaper, and equal at 4,096 × 16;
    - Jev charges $0.042 per million input tokens and bills about 372 tokens of overhead per request plus about 113
      per extra 3-option question;
    - a g5.xlarge left on all month (≈ $734) beats Jev only above about 7 requests/s sustained, for 512-token requests.
  - vLLM path:
    - merged LoRA (bf16), with vLLM's prefix cache sharing the text between leaves;
    - readout = vLLM's Qwen3-reranker 1-logit head;
    - on the example request it makes the same decisions as the transformers path (max score difference 0.06 logit);
    - engine start takes about 6 min the first time (compilation) and about 1 min cached.
  - Cost: AWS ≈ $0.87, Jev $0.04. Box terminated; SG and key pair deleted.
  - Not measured: the vLLM path's accuracy on the test set, and any GPU faster than the A10G. The L40S was out of
    capacity in every zone.
- **22:00: tree LoRA capacity is not the ceiling** (fork 2; two g5.xlarge, ≈ $1.60, both terminated, SG and key pair
  deleted). Same data and recipe as `runs/tree_4b` (10,080 questions, 84 steps), configs `configs/curve/tree_4b_r64.json`,
  `tree_4b_mlp.json`, runner `scripts/run_curve.sh`; tables in `reports/curve/summary.md`.
  - r=64 on q/k/v/o (47.2M trainable, 4×): **81.5%** test (binary 88.5, AUROC 0.956, multiclass 83.0, multilabel EM 52.3);
    82 run-only vs 84 reference-only, p = 0.94. Validation 81.8% vs 80.2%.
  - r=16 on q/k/v/o + gate/up/down (33.0M, 2.8×): **81.6%** (binary 87.9, AUROC 0.955, multiclass 83.4, EM 51.7);
    72 vs 73, p = 1.0. Validation 81.4%.
  - Both vs Jev: p = 0.07–0.08, unchanged. Family swings (±5–12 points on eval_agent_output, TREC, eval_policy) go both
    ways and are within noise for 26–300-question slices.
  - Verdict: with this data, more adapter capacity fits validation better and moves the test by nothing. Together with
    the data curves and 4B = 8B, the recipe (data + objective), not the model or the adapter, sets the 80–82% level.
    Full fine-tuning is now low priority. Remaining levers: rejection/threshold policy (in progress in the other
    sessions) and new verified data for the binary families.
- **20:40: SST-2's binary gap is a bias, not a reading problem** (`reports/tree_4b/test`, a diagnosis on test only;
  nothing was tuned).
  - SST-2 is held out: no SST-2 data was trained on.
  - The tree ranks SST-2 reviews well (AUROC 0.973, Jev 0.994), but predicts "positive" on 34.7% of reviews when 50%
    are positive.
  - Accuracy is 84.0%; the best possible single threshold would give 91.7% (Jev 96.7%).
  - BoolQ is different: AUROC 0.927 vs Jev 0.965, best threshold only 84.3% vs 83.3% at 0.5. That's a real ranking gap.
  - Across all families, SST-2 and BoolQ account for about 60 of the 63 binary answers the tree is behind Jev.
  - Next step: a label-free fix, see experiments.md "Calibration policy". One option is contextual calibration:
    subtract each question's score on an empty text. Pick it on validation, then confirm on a fresh holdout. It is
    test-motivated now, so an SST-2 gain alone is not proof.
- **20:24: learning curves done: the stock 4B recipe saturates at 80–81%** (fork 2; 10 runs, 8 g5.xlarge 16:05–19:20,
  ≈ $23, all boxes terminated, SG and key pair deleted). Tables and paired tests: `reports/curve/summary.md`; README
  subsection "Data and base-model curves (4B)"; configs `configs/curve/`, runner `scripts/run_curve.sh`.
  - Nested data subsets 25/50/100% of the 10,112-question mix: 77.0 / 78.9 / 80.3 (1 epoch), 79.1 / 79.1 / 79.8
    (2 epochs). About 1.5 points per doubling; the second epoch never helps (best checkpoint inside epoch 1).
  - New task type: +100 / +300 / +1,000 / +3,000 BoolQ training questions → BoolQ test 84.3 / 83.3 / 84.3 / 86.7
    (from 83.3; Jev 90.7); overall 80.0 / 80.9 / 80.9 / 80.9, none significant (p ≥ 0.09).
  - Base model: Qwen3-4B-Instruct-2507 zero-shot 71.3 (binary 84.2) vs 62.8 for the reranker; after LoRA 80.6 vs
    80.3 (p = 0.68). Prompt picked on validation (`reports/curve/instruct_prompt_selection`).
  - Verdict: not a data-volume or model-size problem. Next lever claimed: tree LoRA capacity (r=64, MLP targets;
    `configs/curve/tree_4b_r64.json`, `tree_4b_mlp.json`, `scripts/run_curve.sh tree_4b_r64 tree_4b_mlp`), waiting for
    the user's OK on the spend.
- **20:19: tree 4B round 2b started.**
  - Why: round 2 lost CLINC (94.7 → 83.3%). In the hard-case training data, "none" is the correct answer in 23% of the
    multiclass questions that offer it, vs 8% in round 1.
  - Fix: `scripts/rebalance_nota.py` drops 160 random none-answer train questions to reach 10%, giving
    `data/hardcases_nb.jsonl` with 9,982 questions. Validation is unchanged.
  - Run: `TAG=tree_4b_r2b HARD_TRAIN=data/hardcases_nb.jsonl scripts/run_tree_r2.sh`.
  - Motivated by a test diagnosis: report CLINC with that caveat.
  - Validation during training: step 100 84.9% (round 2: 83.9%), step 150 85.4% (round 2: 85.6%).
- **20:15: stock 4B round 2 (`scripts/run_4b_r2.sh`) stopped before it finished** to free the GPU for r2b. No report
  exists; the stock-vs-tree round-2 control is still open.
- **≈ 19:20–20:10: tree 4B round 2** (`runs/tree_4b_r2`, recipe from the tree session, + `data/hardcases.jsonl`,
  max_length 8192): 80.6% vs 81.6% for round 1 (p = 0.01).
  - Traps improved: numeric +25, paraphrase +14, role reversal +13, injection +10, distractor +9 points.
  - CLINC in-scope requests routed to "none" rose from 16 to 50 of 255.
  - On the other 3,171 questions, rounds 1 and 2 score the same (80.35%).
  - Full analysis: `docs/hardcases_round2.md` and `reports/tree_review_2026-09-23/review.md`.
- **≈ 16:30–19:15: round-2 hard cases, OpenRouter part + blind judge** (session "Synthetic data generation strategy";
  write-up `docs/hardcases_round2.md`).
  - Why: more trap-heavy training data without Claude Code usage limits; the user asked for 1/3 simple / hard / very hard,
    a clean state-length ladder (8 → 8K tokens) and heavy prompt variance so the model learns the task, not one phrasing.
  - How: `scripts/gen_hardcases.py` (system prompt `data/hardcases/BRIEF.md`, random per-call ASSIGNMENT). Gemini 3.8
    Flash $12.87 → 950 states / 2,462 q; Grok 4.7 $8.19 → 319 / 1,022 (reasoning cannot be disabled, 4× Gemini per
    state); GPT-6 Luna $1.62 → 1,676 / 3,988; DeepSeek V4 Flash $0.17 → 458 / 1,264 (stopped early, slow provider).
    Total 3,403 states / 8,736 questions, $22.86.
  - Judge: `scripts/judge_hardcases.py`, GPT-6 Astra reasoning low, blind, OpenAI Batch API (OpenRouter's batch endpoint
    rejects this key). 5 batches, 0 failures, $36.24 for 10,627 questions incl. the 1,891 Sonnet ones; Jev second
    opinion $0.27. Author = judge 95.4% (Grok 98.9, Sonnet 98.3, Gemini 97.6, Luna 96.0, DeepSeek 82.1); tables in
    `data/hardcases/review/JUDGE.md`. 432 questions are author = Astra but Jev wrong.
  - Verdict: pipeline works and resumes; data quality good except DeepSeek; the retrain diagnosis above (CLINC `none`)
    is the data's one known flaw. Nothing in flight from this session; no AWS boxes launched by it.
- **≈ 14:20: custom shared-state model (v1 spec) finished and written up** (fork 2 + the "Synthetic data" fork;
  `docs/custom_model.md`, `reports/custom_diagnostics/`, tests in `tests/test_custom.py`, 0.6B backbone, A10G).
  - As specified (frozen backbone + cross-attention + heads): 39.0%. Joint LoRA alone: 39.7% (p = 0.32). With the
    similarity term + joint LoRA (`runs/custom_sim_lora`): 58.2%; distillation from the stock 0.6B teacher: no gain.
  - Why: label memorization, binary head at chance (text and question never meet inside the backbone), and the frozen
    features already match unseen labels better than the trained heads (MaxSim 75–77% vs 23–28%).
  - Speed: 38–43× faster than stock pairs for 16 × 3 questions on 8K–16K-token texts. Its lesson (share the text, keep
    deep joint reading) led to the tree scorer.
  - Engineering notes: MPS caches one graph per tensor shape, hence shape buckets in `custom.py`; an explicit attention
    mask was 1.7–2.2× slower for identical outputs and was removed.
- **Hard-case data, Sonnet part:**
  - 8 Claude Sonnet sub-agents wrote 700 sources / 1,891 questions (`data/hardcases/raw/h*`, brief
    `data/hardcases/BRIEF_sonnet_agents.md`).
  - The OpenRouter part and the Astra judge were run by the "Synthetic data generation strategy" session.
  - `scripts/build_hardcases.py` keeps only questions where the blind Astra judge agrees with the author: 10,142 kept.
- **Stock 4B and 8B on AWS** (`scripts/run_model.sh`, one g6e.xlarge, 3.16 h):
  - 4B: 62.8 → 80.3% with LoRA. 8B: 66.2 → 80.7%. 4B + LoRA ≈ 8B + LoRA (p = 0.52).
  - Tables: `reports/scale_comparison.md`.
- **Jev and GPT-6 Astra on the full test** (`scripts/compare_external.py`): Jev 82.7%, Astra 85.8%.
  - The questions we fail most: `reports/external/failures.md`. That's a test-set list: use it to design data, never
    to train on.
  - Decisions-API-shaped endpoint added to `server.py` (`/api/alpha/decisions`).
- **LinkedIn draft and chart:** `docs/linkedin_post.md`, `docs/linkedin_accuracy.png` (`scripts/make_post_chart.py`).

### 2026-09-22

- **Project built:**
  - Qwen3-Reranker yes/no scorer, validation, typed decisions, grouped-loss LoRA training, held-out calibration,
    evaluation harness, benchmark.
  - Data: `data/eval.jsonl` (398 authored questions, blind-reviewed by LLM), `data/hf.jsonl` (16,800 questions from 11
    pinned datasets, 6 of them held-out families), `data/synthetic.jsonl` (2,448 questions).
  - 0.6B on the Mac: 61.0% unmodified → 73.5% with LoRA (`reports/summary.md`).
