---
hide:
  - navigation
---

# SelfJev

**Can an open model do what Jev does?** [Jev](landscape.md) turns a text and a list of typed questions (yes/no, pick
one, pick many) into calibrated decisions in about 150 ms, with no text generation. SelfJev rebuilds that interface on
open Qwen3 and Qwen3.5 models with small LoRA adapters, and measures every step against Jev on the same questions.

New to the shorthand (eval2, round 2b, r64, stock pairs…)? Hover any dotted-underlined term, or read the
[glossary](glossary.md).

<div class="stat-grid" markdown>
<div class="stat"><strong>95.8%</strong><span>our best model on eval2, the target-task test set</span></div>
<div class="stat"><strong>97.2%</strong><span>Jev on eval2: we are 1.4 points behind</span></div>
<div class="stat"><strong>93.1%</strong><span>on eval_llm, the LLM-evaluation test set, level with Jev's 92.5%</span></div>
<div class="stat"><strong>37×</strong><span>speed-up from reading the text once (shared-prefix tree)</span></div>
<div class="stat"><strong>~$619</strong><span>logged spend: data, judges, GPUs, Jev calls</span></div>
</div>

**The best model**, `selfjev-4b` ([weights/selfjev_4b](../weights/README.md)), is Qwen3.5-4B with a rank-64 LoRA adapter
trained with our shared-prefix tree on all 80K non-test questions (public datasets plus LLM-written cases that a blind
judge confirmed, texts up to 16K tokens), with half-weight Jev probabilities as soft targets and every option listed in
the question. It scores 95.8% on eval2 (Jev 97.2%) and 93.1% on eval_llm (Jev 92.5%), with 11 confident mistakes on
eval2 where its predecessor `qwen35_4b_tree` (95.6%) made 30. The fastest one to serve
was its Qwen3 sibling `tree_4b_combo` (94.5%, archived), which on vLLM was cheaper per request than Jev on a busy GPU.

## The story in eleven steps

| when | step | result |
|---|---|---|
| 09-22 | Qwen3-Reranker-0.6B + LoRA on the laptop | 61.0 → 73.5% on the dev benchmark |
| 09-23 | Jev and GPT-6 Astra on the same questions; scale to 4B and 8B on AWS | Jev 82.7, Astra 85.8; 4B 80.3 = 8B 80.7: fine-tuning matters far more than size |
| 09-23 | A custom cross-attention model that reads the text once | 38–43× faster but 39–58% accurate: yes/no never learned |
| 09-23 | The **shared-prefix tree**: read once, but every branch attends to the text in every layer | 81.6%, 32–37× faster than stock pairs |
| 09-23 | Learning curves, bigger adapters, an 8B, an Instruct base | everything lands at 80–82% on the dev benchmark |
| 09-23 | Round-2 data: 10K hard cases written by 5 models, kept only when a blind judge agrees | better on the traps, but CLINC over-rejection |
| 09-24 | **eval2**: a frozen 1,991-question target-task test set | the hidden effects appear: data +5.5, Instruct base +3.0, rank 64 +2.1 |
| 09-24 | Combine the levers: Instruct base, rank 64, round-2b data | 92.7% on eval2 |
| 09-24 | Round 3 (38.6K more verified questions) + every option listed in the question | **94.5%**: each adds about a point, and they stack |
| 09-25 | Qwen3.5-4B, a hybrid model (3 recurrent Gated DeltaNet layers per attention layer), same levers | 94.5% trained on full sequences capped at 2K tokens |
| 09-25 | A **tree for Qwen3.5**: its recurrent layers run level by level from copied states | **95.6%**, trained on texts up to 8K in 4.1 h |

After that: Qwen3.5 on vLLM keeps its accuracy but is slow with many questions (vLLM reuses its recurrent state only
every 528 tokens), and a first version of RLCD (Jev's name for training on calibration scores; despite the name, no reinforcement
learning is involved) gave no gain on hard labels
([fine-tune and RLCD](finetune.md)).

## Where to go

<div class="grid cards" markdown>

-   :material-lightbulb-on-outline: **[Key findings](findings.md)**

    ---

    What we learned, each finding with its numbers and evidence.

-   :material-podium: **[Leaderboard](leaderboard.md)**

    ---

    Every model on eval2 and the dev benchmark, with all slices.

-   :material-timer-outline: **[Speed and cost](speed.md)**

    ---

    Tree vs pairs, end-to-end latency vs Jev, vLLM, cost per request.

-   :material-close-circle-outline: **[What didn't work](dead_ends.md)**

    ---

    Negative results, so nobody pays for them twice.

-   :material-sitemap-outline: **[Shared-prefix tree](tree_model.md)**

    ---

    The architecture behind every best model.

-   :material-database-outline: **[Datasets and labels](data.md)**

    ---

    Public sets, LLM-written hard cases, blind judging, eval2.

-   :material-tune-variant: **[Fine-tune and RLCD](finetune.md)**

    ---

    Train the best recipe on your own data, then calibration training (what Jev calls RLCD).

-   :material-compass-outline: **[Open questions](next.md)**

    ---

    What to do next to close the last 1.6 points; speed is a deployment question since the H100 sweep (2026-09-26).

-   :material-notebook-outline: **[Lab notebook](experiments.md)**

    ---

    The live ledger and the dated journal the working sessions write.

</div>

!!! warning "Read the numbers with care"
    - **eval2** labels are written by LLMs and kept only when two blind LLM judges agree: LLM-verified, not
      human-verified.
    - The **dev benchmark** has been reused for many decisions, and eval2 has now informed the research direction:
      neither is a clean final test.
    - Every result is a single run with one seed. Paired McNemar tests give the significance; wins with p ≈ 0.06–0.07
      need a second seed.
