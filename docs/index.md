---
hide:
  - navigation
---

# SelfJev

**Can an open model do what Jev does?** [Jev](landscape.md) turns a text and a list of typed questions (yes/no, pick
one, pick many) into calibrated decisions in about 150 ms, with no text generation. SelfJev rebuilds that interface on
open Qwen3 models with small LoRA adapters, and measures every step against Jev on the same questions.

<div class="stat-grid" markdown>
<div class="stat"><strong>92.7%</strong><span>our best model on eval2, the target-task test set</span></div>
<div class="stat"><strong>97.2%</strong><span>Jev on eval2: we are 4.5 points behind</span></div>
<div class="stat"><strong>82.7%</strong><span>both on the 3,471-question dev benchmark: a tie</span></div>
<div class="stat"><strong>37×</strong><span>speed-up from reading the text once (shared-prefix tree)</span></div>
<div class="stat"><strong>~$457</strong><span>logged spend: data, judges, GPUs, Jev calls</span></div>
</div>

**The best model** is Qwen3-4B-Instruct-2507 with a rank-64 LoRA adapter, scoring every question and candidate as a
branch of one shared-prefix token tree, trained on public datasets plus about 10K verified hard cases
(`tree_4b_instruct_r2x64`).

## The story in eight steps

| when | step | result |
|---|---|---|
| 09-22 | Qwen3-Reranker-0.6B + LoRA on the laptop | 61.0 → 73.5% on the dev benchmark; Jev 82.7, GPT-6 Astra 85.8 |
| 09-23 | Scale to 4B and 8B on AWS | 80.3 / 80.7%: 4B = 8B, and fine-tuning matters far more than size |
| 09-23 | A custom cross-attention model that reads the text once | 38–43× faster but 39–58% accurate: yes/no never learned |
| 09-23 | The **shared-prefix tree**: read once, but every branch attends to the text in every layer | 81.6%, 32–37× faster than stock pairs |
| 09-23 | Learning curves, bigger adapters, an 8B, an Instruct base | everything lands at 80–82% on the dev benchmark |
| 09-23 | Round-2 data: 10K hard cases written by 6 models, kept only when a blind judge agrees | better on every trap, but CLINC over-rejection |
| 09-24 | **eval2**: a frozen 1,991-question target-task test set | the hidden effects appear: data +5.5, Instruct base +3.0, rank 64 +2.1 |
| 09-24 | Combine the levers | **92.7%** on eval2; a 27B teacher + our model reach 94.5% together |

## Where to go

<div class="grid cards" markdown>

-   :material-lightbulb-on-outline: **[Key findings](findings.md)**

    ---

    The 24 things we learned, each with its numbers and evidence.

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

-   :material-compass-outline: **[Open questions](next.md)**

    ---

    What to do next to close the last 4.5 points and the 5× speed gap.

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
