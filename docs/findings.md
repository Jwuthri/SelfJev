---
hide:
  - navigation
---

# Key findings

Everything we learned from 2026-09-22 to 2026-09-24, one finding per box. Each box gives the claim, the numbers and the
evidence file.

**How to read the numbers:**

- **eval2** is the frozen target-task test set (1,991 questions). It has been the primary benchmark since 2026-09-24.
- **dev benchmark** is the original 3,471-question test split (`hf.jsonl` test + `eval.jsonl` test). It is 95% public
  datasets and was reused for many decisions, so it is a development benchmark, not a clean test.
- **p** is a paired exact McNemar test on the same questions. "142 / 34" means 142 questions only the first model gets
  right and 34 only the second.

## The headline

!!! success "1. Best model: 92.7% on eval2, 4.5 points behind Jev"
    **Qwen3-4B-Instruct-2507 + LoRA r=64, shared-prefix tree, round-2b data with every hard case kept**
    (`tree_4b_instruct_r2x64`) scores
    **92.7%** on eval2 and **82.7%** on the dev benchmark.

    - Jev scores 97.2% on eval2 (25 / 115, p = 5e-15) and 82.7% on the dev benchmark, a tie (213 / 214).
    - Binary 94.6 vs 97.8, multiclass 95.4 vs 98.1, multilabel exact match 83.5 vs 94.2.
    - It is the only one of our runs above 92%. Next: listing all options in the question (91.6) and rank 64 + MLP
      adapters (91.3).

    Evidence: [eval2 summary](../reports/eval2/summary.md), [leaderboard](leaderboard.md).

!!! success "2. A frozen open 4B model plus a small adapter gets most of the way"
    The core idea behind Jev is not a moat. A LoRA adapter on 0.3% of the weights, trained on about 10K examples for
    under an hour on one cloud GPU:

    - moves Qwen3-Reranker-4B from 62.8% to 80.3% on the dev benchmark;
    - the shared-prefix tree reaches 81.6%, and the best recipe 82.7%, the same as Jev.

    What remains is data for hard reasoning cases, calibration that holds on new tasks, and serving speed.

## Evaluation

!!! warning "3. The dev benchmark hid most real effects; eval2 exposed them"
    Every trained 4B model and both frontier models sit between 80% and 86% on the dev benchmark: Jev 82.7, GPT-6
    Astra 85.8.
    Label noise in public sets (GoEmotions, TweetEval, dair-ai emotion) sets that ceiling, and 3,300 of its 3,471
    questions are public datasets.

    On eval2 our models spread from 68.8% (0.6B) to 92.7%, and Jev scores 97.2%. Levers the dev benchmark called ties or
    losses turned out to be real on eval2:

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

    Evidence: [data/eval2/REVIEW.md](../data/eval2/REVIEW.md).

!!! warning "5. Both test sets are now development sets"
    - The dev benchmark has driven many choices. An early review found 22 test questions whose MNLI premise also
      appears in a selection split, and near-duplicate authored policy texts across splits.
    - eval2 has since informed the research direction, although nothing was trained, tuned or calibrated on it.
    - A fresh final set is needed before claiming a result against Jev.

    Evidence: [review 2026-09-23](../reports/review_2026-09-23.md).

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
    - Capping `none`-correct at 10% (round 2b, `scripts/rebalance_nota.py`) brought CLINC back to 92.0%.

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
    - Author quality varies: DeepSeek V4 Flash agrees with the judge only 82.1% of the time, Grok 4.7 98.9%.
    - Batch judging through OpenAI's Batch API costs about $3.40–4.16 per 1,000 questions.
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
    (`tree_4b_ova`, `scripts/options_in_question.py`):

    - Dev benchmark 82.6 vs 81.2 (130 / 82, p = 0.001), multilabel exact match 57.8 vs 51.7.
    - eval2 91.6 vs 90.6 (66 / 46, p = 0.07).
    - One run each. Requests at inference time need the same transform.

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
    | Qwen3.5-2B, shared document with forked native cache (round-1 data) | not scored | 79.9 |
    | *tree 4B, round-2b data (reference)* | *90.6* | *81.2* |

    Evidence: [other challengers](challengers.md).

## Distillation and calibration

!!! info "16. A 27B zero-shot teacher matches a strong 4B tree, and its errors differ"
    Qwen3.8-27B-FP8, zero-shot, reading the answer-token probabilities: **91.4%** on eval2 (binary 93.4, multiclass
    97.8, multilabel 75.9) vs 91.6% for `tree_4b_ova` (112 / 108, p = 0.84). One of the two is right on 97.0% of the
    questions, and a fixed 50/50 average of their probabilities scores **94.5%**.

!!! failure "17. ...but distilling it into the tree did not help"
    Soft targets from the 27B at weight 0.5 on the target-task training rows (`tree_4b_ova_kd`): eval2 91.0 vs 91.6
    (p = 0.21), dev benchmark 82.5 vs 82.6. Where the teacher disagrees with the verified label (12–20% of rows),
    the loss pulls toward the wrong answer. Untried: multiclass-only distillation, a lower weight, an r64 student.

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

!!! warning "19. Jev is flat at ~150 ms; we scale with the text"
    Same requests from California, one at a time, text 8 → 4,096 tokens:

    - **Jev:** 143–178 ms p50 at every size, even 4,096 tokens × 16 questions. A fit gives 132–137 ms fixed +
      2.2–2.6 ms per 1,000 input tokens, about 400K tokens/s of marginal speed.
    - **Ours (tree 4B, vLLM, one A10G, 71 ms away):** 120 ms at 8 tokens × 1 question, faster than Jev end to end
      up to 128 tokens; 755 ms at 4,096 tokens (5×) and 336–1,195 ms with 16 questions (2–7×).
    - The A10G is compute-bound at 6.5–10K tokens/s. Matching Jev needs much faster GPUs, a smaller model, or both.

    Evidence: [speed](speed.md), [latency summary](../reports/latency/summary.md).

!!! success "20. Serving: vLLM and merged weights are the useful speed-ups"
    - vLLM with the prefix cache: 967 → 700 ms at 2K tokens × 16 × 3; dev benchmark accuracy 81.53% vs 81.50%.
    - Merging the LoRA into the weights: 11–22% faster end to end in the latency sweep, for a small precision cost
      (dev benchmark 81.68 → 81.50). bf16 inference itself costs no quality (0.6B: 73.7 vs 73.5).
    - A compact tree format (38.5% fewer branch tokens) failed its 15% speed gate (7.4% on vLLM) and added CLINC
      over-rejection. It stays experimental.

    Evidence: [latency optimization](../reports/latency_optimization_2026-09-24/conclusions.md).

!!! info "21. A busy GPU is cheaper than Jev; an idle one is not"
    - Fully busy, one A10G with vLLM costs $0.005–0.27 per 1,000 requests; Jev charges $0.016–0.27 ($0.042 per
      million input tokens). That is 1.3–3.1× cheaper for one question, 1.0–1.5× with 16 questions, and equal at
      4,096 tokens × 16 questions.
    - A g5.xlarge left on all month (≈ $734) beats Jev only above about 7 requests/s sustained, for 512-token
      requests.

## Where the gap to Jev is

!!! abstract "22. Multilabel, numbers, dates, sarcasm and injections"
    Best model (`tree_4b_instruct_r2x64`) vs Jev on eval2, every slice with n ≥ 100 and a gap of 5 points or more:

    | slice | n | ours | Jev | gap |
    |---|---|---|---|---|
    | multilabel exact match | 382 | 83.5 | 94.2 | 10.7 |
    | sarcasm | 149 | 86.6 | 97.3 | 10.7 |
    | numeric reasoning | 224 | 82.1 | 92.0 | 9.9 |
    | multi-positive | 322 | 86.3 | 96.0 | 9.7 |
    | injection | 151 | 88.7 | 97.4 | 8.7 |
    | double negation | 126 | 90.5 | 99.2 | 8.7 |
    | paraphrase | 218 | 88.1 | 95.4 | 7.3 |
    | temporal reasoning | 203 | 82.8 | 89.2 | 6.4 |
    | long state | 191 | 92.7 | 99.0 | 6.3 |
    | hard tier | 673 | 90.5 | 96.7 | 6.2 |
    | `none` of the above offered | 118 | 89.8 | 95.8 | 6.0 |
    | distractor | 474 | 91.1 | 97.0 | 5.9 |
    | very hard tier | 654 | 90.8 | 96.5 | 5.7 |

    Text length is not our weakness: 96.1% at 1K–4K tokens and 94.6% above 4K. Numbers and dates are also Jev's
    weakest slices (92.0, 89.2), with multilabel (94.2).

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
    - GPU capacity was scarce throughout: no g6e.2xlarge/4xlarge at first, no H100 in any Ohio zone, and L40S often
      unavailable.
    - Rule since then: every box is tagged and listed in the JOURNAL's *In flight* table, and nobody touches another
      session's box.
