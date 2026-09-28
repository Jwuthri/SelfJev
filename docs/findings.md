---
hide:
  - navigation
---

# Key findings

Everything we learned from 2026-09-22 to 2026-09-27, one finding per box. Each box gives the claim, the numbers and the
evidence file.

**How to read the numbers** (every other term is in the [glossary](glossary.md)):

- **eval2** is the frozen target-task test set (1,991 questions). It has been the primary benchmark since 2026-09-24.
- **eval_llm** is the frozen LLM-evaluation test set (946 questions: score, judge, verify, guardrail, jailbreak;
  [how it was built](llm_eval_data.md)), scored since 2026-09-26.
- **dev benchmark** is the original 3,471-question test split (`hf.jsonl` test + `eval.jsonl` test). It is 95% public
  datasets and was reused for many decisions, so it is a development benchmark, not a clean test.
- **p** is a paired exact McNemar test on the same questions. "142 / 34" means 142 questions only the first model gets
  right and 34 only the second.

## The headline

!!! success "1. Best model: `selfjev-4b`, 95.8% on eval2 and 93.1% on eval_llm (Jev 97.2% and 92.5%)"
    **`selfjev-4b`** (2026-09-26, the default, `weights/selfjev_4b`): Qwen3.5-4B + LoRA r64 trained with the
    shared-prefix tree, every option listed in the question, from scratch on 79.9K non-test questions of
    `data/all.jsonl.gz` (texts up to 16K tokens, the LLM-evaluation data and two new verified batches; the later batch
    `mpos_distr_num_v1` is not in it), with half-weight Jev probabilities as soft targets.

    - eval2 **95.8%**: Jev 97.2% (23 / 52, p = 0.001), its predecessor 95.6% (33 / 29, p = 0.70). Binary 96.8 vs Jev
      97.8, multiclass 97.0 vs 98.1, multilabel exact match 91.4 vs 94.2; the simple tier level (98.5 vs 98.5).
    - eval_llm **93.1%**: level with Jev's 92.5% (33 / 27, p = 0.52); its predecessor, which never saw this kind of
      data, 82.1%.
    - Dev benchmark 83.8%: above Jev's 82.7% (164 / 128, p = 0.04), 0.7 below its predecessor (103 / 127, p = 0.13),
      from Jev's targets on the public emotion set.
    - Confident mistakes on eval2 30 → 11 (Jev 7); long-text errors 8 → 3.

    Its predecessor, **`qwen35_4b_tree`** (2026-09-25; weights at tag `archive/pre-cleanup-2026-09-27`), is the same
    recipe on the older mix (round-2b + round-3 verified data), hard labels, texts up to 8K tokens (51.8K training
    questions):
    **95.6%** on eval2 (Jev 31 / 64, p = 0.0009) and **84.4%** on the dev benchmark (Jev 238 / 178, p = 0.004: ours is
    higher).

    - Above both previous best models, which tied at 94.5:
      - `qwen35_4b_combo`, the same base and data trained on full sequences capped at 2K tokens (18.5% of the data
        dropped): 52 / 31, p = 0.028. The tree in training is worth +1.1, in 38% less training time.
      - `tree_4b_combo`, Qwen3-4B-Instruct with the same levers: 63 / 41, p = 0.039.
    - The levers that got here stack: round-2b and round-3 verified data, the options listed in the question, LoRA
      r=64, the Qwen3.5 base, and the tree in training (which lets that base train on long texts).
    - Qwen3.5 is mostly Gated DeltaNet (a recurrence), which a tree mask cannot isolate: its tree runs those layers
      level by level from copied states, with gradients through them ([tree scorer](tree_model.md#qwen35-hybrid-deltanet)).

    Evidence: [eval2 summary](../reports/eval2/summary.md), [leaderboard](leaderboard.md), JOURNAL 2026-09-25 16:05 and
    2026-09-26 21:25.

!!! warning "1b. More verified hard cases from the same kind of writers has hit diminishing returns"
    On the Instruct base with r=64, each data round adds less on eval2:

    | data | eval2 | gain | paired test |
    |---|---|---|---|
    | round-1 data (`tree_4b_instruct`, r16) | 88.1 | | |
    | + round-2b hard cases, ~7K (`tree_4b_instruct_r2x64`) | 92.7 | +4.6 | 123 / 32, p = 9e-14 |
    | + round-3 hard cases, ~35K (`tree_4b_instruct_r3`) | 93.3 | +0.6 | 62 / 50, p = 0.3 |

    - The round-1 row also used r16, not r64, so its gain mixes data and capacity.
    - Round 3 had more multi-positive multilabel questions and far fewer "none" answers than round 2, but it came from
      the same kind of LLM writers (Luna, Gemini Flash, Grok) and the same Astra judge.
    - What moved eval2 after round 3 was the question format, not more data. Listing the options in the question adds
      +1.2 on top of round 3 (`tree_4b_combo`, 94.5; 60 / 37, p = 0.025; finding 13).
      - On round-2b data alone the same change ties (`tree_4b_combo_r2`, 92.9 vs 92.7, p = 0.83).
      - "Option pointers" (`tree_4b_combo_ptr`) is a dead end: −0.9 and only ~1.1× faster.
    - At 94.5, the 2.7 points left to Jev (97.2) needed something other than more of this data:
      - multilabel exact match (85.9 vs 94.2) was the biggest gap;
      - teacher ensembles scored 94.5 at 27B cost, and distilling them at weight 0.5 gave nothing (`tree_4b_ova_kd`).
    - What came next: the Qwen3.5 base trained with its own tree (95.6), then new kinds of verified data
      (LLM-evaluation texts, targeted batches) with Jev's soft targets (`selfjev-4b`, 95.8; finding 1).

!!! success "2. A frozen open 4B model plus a small adapter gets most of the way"
    The core idea behind Jev is not a moat. A LoRA adapter on 0.3% of the weights, trained on about 10K examples for
    under an hour on one cloud GPU:

    - moves Qwen3-Reranker-4B from 62.8% to 80.3% on the dev benchmark;
    - the shared-prefix tree reaches 81.6% (Jev 82.7%).

    With more verified data, the Qwen3.5 base and Jev's soft targets (80K questions, ≈ $21 on one L40S), `selfjev-4b`
    reaches 83.8% there and 95.8% on eval2 (Jev 97.2%). What remains is data for hard reasoning cases, calibration that
    holds on new tasks, and serving speed.

## Evaluation

!!! warning "3. The dev benchmark hid most real effects; eval2 exposed them"
    Every trained 4B model and both frontier models sit between 80% and 86% on the dev benchmark: Jev 82.7, GPT-6
    Astra 85.8.
    Label noise in public sets (GoEmotions, TweetEval, dair-ai emotion) sets that ceiling, and 3,300 of its 3,471
    questions are public datasets. A blind relabel (2026-09-26) found 317 of 778 dev-benchmark failures (41%) to look like
    label problems.

    On eval2 our models spread from 68.8% (0.6B) to 95.8% (`selfjev-4b`), and Jev scores 97.2%. Levers the dev
    benchmark called ties or losses turned out to be real on eval2:

    | lever | dev benchmark | eval2 |
    |---|---|---|
    | round-2 verified hard cases | −1.0 (round 2), −0.4 (round 2b) | **+5.5** (142 / 34, p = 7e-17) |
    | Instruct base instead of the reranker | −1.2 | **+3.0** (129 / 69, p = 2e-5) |
    | LoRA rank 64 instead of 16 | −0.1 | **+2.1** (77 / 36, p = 1e-4) |
    | MLP targets added | 0.0 | +1.2 (62 / 38, p = 0.02) |

    Lesson: decide on a test set that looks like the target task. Evidence: [eval2 summary](../reports/eval2/summary.md),
    [curve summary](../reports/curve/summary.md).

!!! info "4. eval2: 1,991 questions, three authors, two blind judges, $32.72"
    - Written by models never used for training data: Claude Opus 5.5, Kimi K3 and GLM 5.3.
    - A question is kept only when GPT-6 Astra and Gemini 3.1 Pro, both blind, agree with its author: 96.2% kept.
    - Balanced by construction: 3 difficulty tiers, a text-length ladder from 8 to 8K tokens, and n ≥ 57 for every
      main trap tag.
    - A `none` option is correct in 14.8% of the multiclass questions that offer one.
    - Jev scores 97.2% on it. GPT-6 Astra is not scored, since it was one of the judges.
    - Its labels hold up: a blind Claude Opus 5.5 relabel of every question `qwen35_4b_tree` or Jev got wrong
      (2026-09-26) found 114 of 119 failures to be real model errors and one clear label error (`eg-0024-q1`). eval2
      stays frozen, with an errata list.

    Evidence: [data/eval2/REVIEW.md](../data/eval2/REVIEW.md), [failure audit](../reports/audit_2026-09-26/AUDIT.md).

!!! warning "5. Both test sets are now development sets"
    - The dev benchmark has driven many choices. An early review found 22 test questions whose MNLI premise also
      appears in a selection split, and near-duplicate authored policy texts across splits.
    - eval2 has since informed the research direction, although nothing was trained, tuned or calibrated on it. Its
      failure audit (2026-09-26) motivated two training batches, labeled as test-diagnosis-motivated.
    - eval_llm has not been mined for our errors, but it informs choices too: `selfjev-4b`'s promotion and the next
      retrain's decision rule use it.
    - A fresh final set is needed before claiming a result against Jev.

    Evidence: [review 2026-09-23](../reports/review_2026-09-23.md).

!!! warning "5b. One run is not a measurement: the same recipe, run again, moves by about a point"
    - `selfjev-4b`'s exact recipe, rerun on the same data in the same order with the same seed (`selfjev_4b_repro`,
      2026-09-27), scored eval2 95.08 vs 95.78, eval_llm 91.97 vs 93.13 and dev benchmark 83.81 vs 83.75; none of the
      differences is significant (p = 0.12, 0.13, 0.92), and its final validation was 92.7 vs 93.7.
    - So a single-run difference of about a point says little either way: `selfjev-4b` was a good draw, and a change
      that "wins" or "loses" by a point needs two or more runs per arm (≈ $20 each) before it counts.
    - The batch-2 retrain (`selfjev_4b_v2`, eval_llm 90.49) read as a big loss against `selfjev-4b`; against the rerun
      it is 90.49 vs 91.97 (p = 0.07).

    Evidence: `reports/selfjev_4b_repro/`, `reports/selfjev_4b_v2/`, [JOURNAL 2026-09-27 22:25](JOURNAL.md).

## Data

!!! success "6. Verified target-task data is the biggest lever: +5.5 on eval2"
    Round 2 added about 10K hard-case questions (five authoring models, blind GPT-6 Astra judge). Tree 4B, round 1 vs
    round 2b, on eval2: **85.1 → 90.6** (142 / 34, p = 7e-17).

    | eval2 slice | round 1 | round 2b | Jev |
    |---|---|---|---|
    | multilabel exact match | 63.9 | 78.8 | 94.2 |
    | very hard tier | 79.8 | 86.5 | 96.5 |
    | numeric reasoning | 67.0 | 78.6 | 92.0 |
    | injection | 71.5 | 82.1 | 97.4 |
    | sarcasm | 71.8 | 82.6 | 97.3 |
    | multi-positive | 66.8 | 79.5 | 96.0 |

    By comparison, 4B → 8B, adapter capacity and stock → tree each moved the dev benchmark by ≤ 1.3 points.
    Evidence: [round-2 write-up](hardcases_round2.md), [eval2 summary](../reports/eval2/summary.md).

!!! failure "7. One skewed class in the data cost 11 points on one family"
    In the hard and very-hard round-2 multiclass questions that offer `none`, `none` was the answer 28% of the time,
    against 8% in round-1 synthetic data and never in the public sets. CLINC intent accuracy fell from 94.7% to 83.3%.

    - All 34 newly wrong CLINC answers picked `none`; `none` predictions rose from 61 to 95, with 45 gold.
    - Ignoring `none`, both models rank the right intent first on 254 of 255 in-scope questions. The model did not
      forget intents; it became too willing to reject.
    - Capping `none`-correct at 10% (round 2b, `scripts/rebalance_nota.py` at tag `archive/pre-cleanup-2026-09-27`)
      brought CLINC back to 92.0%.

    This fix came from a test diagnosis, so it is labeled as such. Evidence:
    [tree review](../reports/tree_review_2026-09-23/review.md).

!!! info "8. More of the same data buys about 1.5 points per doubling"
    Stock 4B, nested subsets of the round-1 mix (dev benchmark):

    | share of 10,112 questions | 25% | 50% | 100% |
    |---|---|---|---|
    | 1 epoch | 77.0 | 78.9 | 80.3 |
    | 2 epochs | 79.1 | 79.1 | 79.8 |

    - The second epoch never helps: the best checkpoint is always inside epoch 1.
    - A new task type is expensive: +100 / +300 / +1,000 / +3,000 BoolQ questions move BoolQ test accuracy 83.3 →
      84.3 / 83.3 / 84.3 / 86.7 (Jev 90.7), and the overall score not at all (p ≥ 0.09).

    Evidence: [curve summary](../reports/curve/summary.md).

!!! success "9. Generating and judging training data with LLMs works, and it is cheap"
    - **Round 2:** 10,627 questions from Gemini 3.8 Flash, Grok 4.7, GPT-6 Luna, DeepSeek V4 Flash and 8 Claude
      Sonnet agents. 95.4% of them agree with a blind GPT-6 Astra judge; only the agreements are kept (10,142).
      Cost: $22.86 generation + $36.24 judging.
    - **Round 3:** 38,628 verified questions, 97.0% author–judge agreement, 54% of multilabel questions with 3+
      positives. About $280.
    - **Since then** every new set is a batch that grows one dataset (`data/all.jsonl.gz`, 93,237 questions): the
      LLM-evaluation data (9,443 training questions + the frozen `eval_llm`, $96.38), `llm_multilabel_v1` (7,570,
      $68.96), `numdate_neg_v1` (549, $3.08) and `mpos_distr_num_v1` (3,645, $19.81); author–judge agreement 89.7–95.6%.
    - Author quality varies: DeepSeek V4 Flash agrees with the judge only 82.1% of the time, Grok 4.7 98.9%.
    - Batch judging through OpenAI's Batch API costs about $3.40–4.60 per 1,000 questions.
    - Jev agrees with authors on 93.0%: a useful second opinion, never the gate.

    Evidence: [round-2 write-up](hardcases_round2.md), [data](data.md).

## Architecture and base model

!!! success "10. The shared-prefix tree: same quality, up to 37× faster"
    The text is read once, and every question and candidate branches off it with full attention to it through all
    layers (a tree attention mask). Each leaf scores exactly like the standalone pair (tested to 1.7e-5).

    - Dev benchmark: 81.6% vs 80.3% for stock pairs on the same data (182 / 138, p = 0.016).
    - eval2: 85.1% vs 86.5% for stock pairs (101 / 129, p = 0.08): no significant quality cost.
    - Speed (A10G, 16 questions × 3 candidates): 2.8 s vs 90.4 s at 8K tokens, 5.6 s vs 207 s at 16K.

    Evidence: [tree scorer](tree_model.md).

!!! tip "11. The base model matters more than its size"
    - **Instruct beats reranker once the data is good:** Qwen3-4B-Instruct-2507 in the tree scores +3.0 on eval2 with
      round-1 data (88.1 vs 85.1). On the dev benchmark it looked like a loss (80.4 vs 81.6).
    - **It stacks with the data:** 92.7 vs 90.6 for the reranker on round-2b data (90 / 47, p = 0.0003). That run also
      used r64 and kept every hard case (18,681 vs 16,375 questions), but r64 alone added nothing on round-2b data, so
      the base is most of the gain.
    - **4B ≈ 8B:** stock + LoRA 80.3% vs 80.7% on the dev benchmark (p = 0.52), and the 8B is about 1.5× slower.
    - **Sub-1B is out for quality:** the 0.6B stock model is 17.7 points below the 4B on eval2 (68.8 vs 86.5), and
      jina-reranker-v3.5 (0.6B) reaches 73.3 with the best data recipe.

!!! tip "12. Adapter capacity helps, but overlaps with data"
    - On round-1 data: rank 64 gives +2.1 on eval2 (87.2 vs 85.1, p = 1e-4) and MLP targets +1.2 (86.3, p = 0.02).
    - On round-2b data: rank 64 adds nothing (90.3 vs 90.6, p = 0.61); rank 64 + MLP adds +0.7 (91.3, p = 0.17).
    - Once the data is good, capacity adds ≤ 1 point.

    Evidence: [curve summary](../reports/curve/summary.md).

!!! tip "13. Showing every option in the question helps"
    Listing all candidates in the question text, so each leaf judges one option while seeing the alternatives
    (`tree_4b_ova`, `scripts/data/options_in_question.py`):

    - Dev benchmark 82.6 vs 81.2 (130 / 82, p = 0.001), multilabel exact match 57.8 vs 51.7.
    - eval2 91.6 vs 90.6 (66 / 46, p = 0.07).
    - One run each. Requests at inference time need the same transform: `selfjev serve` and `selfjev classify` apply
      it by default, and the evaluation files are transformed ahead (`data/ova/`). `selfjev-4b` and the three best
      models before it (`qwen35_4b_tree`, `qwen35_4b_combo`, `tree_4b_combo`) all use it.

!!! failure "14. A new cross-attention head on a shared encoding does not work (as specified)"
    The v1-spec model encodes the text once, encodes each candidate separately, and scores with 2 new cross-attention
    blocks and small heads.

    - 39.0% on the dev benchmark as specified, 58.2% with a MaxSim similarity term and joint LoRA (stock LoRA: 73.5%).
    - Binary AUROC stays at 0.45–0.54: yes/no questions are never learned.
    - Causes: it removes the pretrained yes/no readout and the deep joint reading of text and question; the heads
      memorize training labels (AG News 87.7% but CLINC 20.7%).
    - It is 38–43× faster than stock pairs at 16 × 3 on long texts. Its lesson, share the text but keep deep joint
      reading, led to the tree.

    Evidence: [custom model](custom_model.md).

!!! failure "15. The other challengers fall well short of the 4B tree"
    | challenger | eval2 | dev benchmark |
    |---|---|---|
    | T5Gemma 2 1B–1B, shared encoder + decoder branches (round-1 data) | 73.0 | 75.4 |
    | T5Gemma 2, round-2b data, **decoder-only LoRA by mistake** | 76.8 | 73.8 |
    | jina-reranker-v3.5 0.6B, listwise, round-2b data | 73.3 | 76.6 |
    | Qwen3.5-2B, shared document with forked native cache (round-1 data) | 84.3 | 79.9 |
    | *tree 4B, round-1 data (reference)* | *85.1* | *81.6* |
    | *tree 4B, round-2b data (reference)* | *90.6* | *81.2* |

    Qwen3.5-2B came closest (84.3 vs 85.1 on the same round-1 data); its 4B sibling has been the base of the best models
    since 2026-09-25, `selfjev-4b` included. Evidence: [other challengers](challengers.md), JOURNAL 2026-09-24 16:18.

## Distillation and calibration

!!! info "16. A 27B zero-shot teacher matches a strong 4B tree, and its errors differ"
    Qwen3.8-27B-FP8, zero-shot, reading the answer-token probabilities: **91.4%** on eval2 (binary 93.4, multiclass
    97.8, multilabel 75.9) vs 91.6% for `tree_4b_ova` (112 / 108, p = 0.84). One of the two is right on 97.0% of the
    questions, and a fixed 50/50 average of their probabilities scores **94.5%**.

!!! failure "17. ...but distilling it into the tree did not help"
    Soft targets from the 27B at weight 0.5 on the target-task training rows (`tree_4b_ova_kd`): eval2 91.0 vs 91.6
    (p = 0.21), dev benchmark 82.5 vs 82.6. Where the teacher disagrees with the verified label (12–20% of rows),
    the loss pulls toward the wrong answer. The follow-ups (multiclass only, a lower weight, an r64 student) were closed
    untried at the 2026-09-27 cleanup; the teacher's code is at tag `archive/pre-cleanup-2026-09-27`.

!!! success "17b. Jev's probabilities as soft targets cut confident mistakes; RLCD adds nothing over a fine-tune"
    From `qwen35_4b_tree` (eval2 95.58), one epoch on 69.5K non-test questions with the target 0.5 × verified label +
    0.5 × Jev's probabilities (the label stays the argmax, so Jev never decides a label):

    | eval2 | accuracy | Brier | confident mistakes (≥ 0.9 sure) |
    |---|---|---|---|
    | start | 95.58 | 0.0480 | 30 |
    | B: fine-tune on Jev's targets | 95.73 (19 / 16, p = 0.74) | **0.0438** | 14 |
    | A: RLCD on the same targets | 95.43 (vs B 4 / 10, p = 0.18) | 0.0446 | 22 |
    | C: B + RLCD with a 5× cost per confident mistake | 95.68 (vs B 9 / 10, p = 1) | 0.0518 | **8** |
    | Jev | 97.24 | 0.0335 | 7 |

    - RLCD with proper-score rewards is fine-tuning with noise: its rewards peak at the same target. On hard labels it
      did nothing either (2026-09-25).
    - C's 8 confident mistakes come from being less sure overall: at equal coverage it is no better than B. Jev's edge
      is ranking (8 mistakes among its 92% most confident decisions, B 20), not hedging.
    - Trained from scratch on all the data with these targets, the recipe became `selfjev-4b` (finding 1).

    Evidence: [fine-tune and RLCD](finetune.md), JOURNAL 2026-09-26 09:10 and 15:15.

!!! warning "18. Calibration: temperatures near 1, thresholds that hurt, and a bias on unseen tasks"
    - After LoRA the fitted temperatures are about 1: the raw scores are already calibrated in distribution (tree
      binary ECE 0.077, stock 0.056, Jev 0.045).
    - Calibration fitted in distribution does not transfer: LoRA 0.6B ECE 0.19 on SST-2 and 0.35 on agent-output.
    - F1-maximizing thresholds chosen on validation cut tree accuracy from 81.6% to 79.3%: serve with 0.5.
    - SST-2 (held out) is a bias, not a reading problem: AUROC 0.973, but "positive" on 34.7% of reviews when 50% are
      positive. 84.0% accuracy, 91.7% at the best single threshold (a test diagnosis).
    - The untrained 0.6B shows the limit: temperature brings binary ECE from 0.384 to 0.025 only by squashing every
      probability toward 0.5 (Brier 0.244).

## Speed and cost

!!! success "19. The speed gap was hardware: on one H100 the 4B tree beats Jev's server time"
    Same requests from California, one at a time, text 8 → 4,096 tokens; `tree_4b_combo` merged on vLLM. Jev through
    OpenRouter (11 ms away); ours on one p5.4xlarge spot (1× H100, ≈ $2.54/h, 61 ms away), 2026-09-26. p50 ms, wall /
    server-side:

    | text tokens | questions | Jev wall / server | A10G | L40S | H100 bf16 | H100 FP8 |
    |---|---|---|---|---|---|---|
    | 8 | 1 | 130 / 110 | 125 / 55 | 158 / 36 | **140 / 22** | 139 / 22 |
    | 512 | 1 | 135 / 115 | 204 / 136 | 177 / 55 | **149 / 30** | 146 / 29 |
    | 2,048 | 1 | 132 / 110 | 429 / 361 | 244 / 121 | **164 / 47** | 163 / 46 |
    | 4,096 | 1 | 142 / 122 | 770 / 698 | 356 / 228 | **200 / 82** | 195 / 75 |
    | 8 | 16 | 140 / 117 | 471 / 401 | 199 / 135 | **179 / 58** | 175 / 56 |
    | 512 | 16 | 145 / 123 | 566 / 496 | 279 / 163 | **166 / 76** | 190 / 71 |
    | 2,048 | 16 | 153 / 134 | 882 / 808 | 342 / 268 | **186 / 120** | 231 / 114 |
    | 4,096 | 16 | 156 / 134 | 1,336 / 1,263 | 505 / 424 | **250 / 189** | 245 / 179 |

    - Inside the machine the H100 is 2–5× faster than Jev's server time; the only slower cell is 4,096 tokens × 16
      questions (189 vs 134 ms). On the A10G the same model was 5× slower than Jev at 4,096 tokens.
    - End to end we trail by 10–100 ms, which is the network hop (61 vs 11 ms). Placed as close to the client as
      OpenRouter's edge, this model beats Jev's latency.
    - FP8 (vLLM dynamic) changes nothing: at 4B the H100 is overhead-bound, not compute-bound.
    - Jev's marginal cost per token is still ≈ 6× lower (2.2–2.6 vs ≈ 15 ms per 1,000 tokens), so it is a smaller model
      or more GPUs per request; up to 4K tokens the fixed costs decide.
    - These are the Qwen3 tree's numbers (`tree_4b_combo`, weights at tag `archive/pre-cleanup-2026-09-27`). The
      default `selfjev-4b` (Qwen3.5) is served by `TreeServer` (finding 20), whose latency has not been measured on an
      NVIDIA GPU yet. A separate M5 Pro experiment measures the current model on MPS and is not directly comparable.

    Evidence: [speed](speed.md#the-same-model-on-an-h100-2026-09-26), [latency summary](../reports/latency/summary.md),
    [JOURNAL 2026-09-26](JOURNAL.md).

!!! success "20. Serving: vLLM and merged weights are the useful speed-ups"
    - vLLM with the prefix cache: 967 → 700 ms at 2K tokens × 16 × 3; dev benchmark accuracy 81.53% vs 81.50%.
    - Merging the LoRA into the weights: 11–22% faster end to end in the latency sweep, for a small precision cost
      (dev benchmark 81.68 → 81.50). bf16 inference itself costs no quality (0.6B: 73.7 vs 73.5).
    - The vLLM path keeps `tree_4b_combo`'s eval2 accuracy: 94.42 in bf16 (5 of 1,991 decisions differ from
      transformers' 94.48) and 94.48 with dynamic FP8 (25 differ). On an H100, all of eval2 runs in 16–18 s.
    - A compact tree format (38.5% fewer branch tokens) failed its 15% speed gate (7.4% on vLLM) and added CLINC
      over-rejection. It stays experimental.
    - Qwen3.5 on vLLM keeps its accuracy (eval2 95.58, as in transformers) and answers one question in 87–131 ms
      server side up to 2K tokens (L40S; Jev 102–106 ms). With 16 questions it is slow (454–1,138 ms): vLLM caches its
      recurrent state only every 528 tokens, so each candidate recomputes the end of the text. The Qwen3 tree on vLLM
      takes 163–424 ms there.
    - So `selfjev serve` serves `selfjev-4b` with the Qwen3.5 training tree run forward only (`TreeServer`,
      `src/selfjev/engine/tree.py`, the default engine; vLLM stays an option): the text once, each question once, then
      each candidate, the same work as the Qwen3 tree. It matches standalone sequences in a CPU test; its latency on a
      NVIDIA GPU has not been measured yet. On an M5 Pro using PyTorch MPS, the current model's 10-run median is
      688 ms for one question and 6,786 ms for 16 questions at 8 text tokens; the unsupported Mac CLI and slower
      reference recurrent operation limit this result to an experiment ([raw report](../reports/latency/mac_m5_pro_selfjev4b.json)).

    Evidence: [latency optimization](../reports/latency_optimization_2026-09-24/conclusions.md),
    [JOURNAL 2026-09-25 18:05](JOURNAL.md).

!!! info "21. A busy GPU is cheaper than Jev; an idle one is not"
    - Fully busy, one A10G with vLLM costs $0.005–0.27 per 1,000 requests; Jev charges $0.016–0.27 ($0.042 per
      million input tokens). That is 1.3–3.1× cheaper for one question, 1.0–1.5× with 16 questions, and equal at
      4,096 tokens × 16 questions.
    - A g5.xlarge left on all month (≈ $734) beats Jev only above about 7 requests/s sustained, for 512-token
      requests.
    - On an L40S ($2.24/h) the Qwen3 tree on vLLM is below Jev in every cell ($0.005 vs $0.016 per 1,000 one-question
      requests at 8 tokens; $0.243 vs $0.265 at 4,096 tokens × 16 questions); Qwen3.5 costs 2–6× Jev with 16 questions.
    - On an H100 spot ($2.54–2.63/h) it is 2.1–6.5× cheaper than Jev in every cell: 294 requests/s and $0.0025 per
      1,000 at 8 tokens × 1 question (Jev $0.016), 5.9 requests/s and $0.124 at 4,096 × 16 (Jev $0.265). At the
      on-demand price ($6.88/h) it stays below Jev everywhere except within 10% at 4,096 × 16.

## Where the gap to Jev is

!!! abstract "22. Several correct answers, numbers and distractors"
    `selfjev-4b` vs Jev on eval2, every slice with n ≥ 100 and a gap of 3 points or more
    ([reports/eval2/summary.md](../reports/eval2/summary.md)):

    | slice | n | ours | Jev | gap |
    |---|---|---|---|---|
    | multi-positive | 322 | 91.0 | 96.0 | 5.0 |
    | numeric reasoning | 224 | 87.5 | 92.0 | 4.5 |
    | multi-turn | 149 | 92.6 | 96.0 | 3.4 |
    | distractor | 474 | 93.9 | 97.0 | 3.1 |

    - Just under 3 points: multilabel exact match (91.4 vs 94.2) and role reversal (94.1 vs 96.8). Level on the simple
      tier (98.5 vs 98.5), ahead on exceptions (96.2 vs 95.3).
    - Counted in wrong questions against Jev: multi-positive 29 vs 13, distractor 29 vs 14, numeric 28 vs 18 (JOURNAL
      2026-09-26 21:25). Batch `mpos_distr_num_v1` (3,645 questions) targets these three; it was motivated by a test
      diagnosis. The retrain with it (`selfjev_4b_v2`, 2026-09-27) came out worse: eval2 95.4 vs 95.8 (p = 0.42), eval_llm
      90.5 vs 93.1 (p = 0.0002); against a rerun of the recipe without it, 90.5 vs 92.0 (p = 0.07, box 5b). Either way,
      more targeted data did not close these gaps.
    - The previous default (`qwen35_4b_tree`) also had double negation (94.4 vs 99.2), hypothetical (94.5 vs 98.4),
      temporal (85.7 vs 89.2), paraphrase (92.2 vs 95.4), long state (95.8 vs 99.0), the very hard tier (93.4 vs 96.5)
      and multilabel exact match (90.1 vs 94.2) on this list; `selfjev-4b` brought each under 3 points. Multi-turn is
      new on it (94.0 → 92.6). With `tree_4b_instruct_r2x64` the gaps reached 10.7.
    - Text length is not our weakness: 97.6% at 1K–4K tokens and 97.6% above 4K (Jev 98.0 and 98.8). Numbers and dates
      are also Jev's weakest slices (92.0, 89.2), with multilabel (94.2).

## Process lessons

!!! warning "23. Audit before you trust a number"
    Three results were wrong at first and caught by audits:

    - **T5Gemma:** the LoRA target filter missed the encoder path, so the "full" adaptation trained the decoder only
      (208 decoder tensors, 0 encoder).
    - **eval2 ids:** a first export renumbered question ids after drops. Jev was briefly reported at 95.2% instead of
      97.2%.
    - **Benchmark prompt:** the stock latency benchmark ran prompt `task-v1` while its quality report used
      `answer-v1`.

    Check adapter coverage, join keys and formats before comparing.

!!! warning "24. Shared cloud accounts need a written owner for every box"
    - An unlogged `aws ec2 stop-instances` from the laptop killed the round-3 training run at step ≈ 500 of 915.
      Only the step-300 checkpoint survived: 90.8 on eval2, not a verdict on round 3.
    - GPU capacity was scarce on 2026-09-23/24: no g6e.2xlarge/4xlarge at first, no H100 in any Ohio zone, and L40S
      often unavailable. From 2026-09-25 every training run found an L40S (g6e.2xlarge, us-east-2); an H100 was found
      once, as spot (2026-09-26).
    - Rule since then: every box is tagged and listed in the JOURNAL's *In flight* table, and nobody touches another
      session's box.
