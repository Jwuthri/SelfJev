---
base_model: Qwen/Qwen3.5-4B
base_model_relation: adapter
library_name: peft
pipeline_tag: text-classification
tags:
  - decision-model
  - self-hosted
  - lora
  - selfjev
---

![SelfJev-4B: read the document once, branch across questions, and score their candidate answers.](assets/hero.png)

# SelfJev-4B

**Structured decisions from text. A 4B backbone. Your own GPU.**

Route a customer message. Check a claim. Review an AI response. SelfJev answers questions over the options you supply and returns probabilities through a Python SDK or HTTP API. Its default engine shares the document computation across questions and scores candidates directly, without generating an answer token by token.

[Quickstart](#quickstart) · [Results](#results) · [Public datasets](#public-datasets) · [Model size](#accuracy-and-model-size) · [Architecture](#architecture) · [Latency](#hardware-and-speed) · [Research](#the-research-path) · [Source code](https://github.com/Jwuthri/SelfJev)

| Ask for | Get back | Use it for |
|---|---|---|
| Yes / no | Probability of yes | Verification, guardrails, detection |
| One choice | Selected option and probabilities | Routing, intent, categorization |
| An ordered score | Score and probabilities over your levels | Review and grading |
| Every matching option | Selected set and per-option probabilities | Tags, checklists, multiple issues |

This repository contains the **230 MB LoRA adapter**, not the entire model. The Qwen3.5-4B base weights download separately. The 4B model size refers to the backbone; the adapter stores the learned update.

## Results

![SelfJev and Jev accuracy on two authored test suites and the public-source development tasks; exact values below.](assets/overview.png)

| Evaluation | Questions | SelfJev-4B | Jev API | SelfJev evidence |
|---|---:|---:|---:|---|
{{OVERVIEW}}

**What these measure.** Text decisions cover authored routing, policy, evidence and difficult language cases. AI response review covers verification, judging, scoring, guardrails and jailbreak detection. Public-source tasks cover 11 adapted datasets. Each score counts a question as correct only when the expected answer matches; for multiple selections, the entire set must match.

These are recorded results from the current **TreeServer** engine and matched Jev predictions, not scores from a newly merged vLLM release. The authored sets use AI-checked labels, not human ground truth. Both have informed research direction. The public-source set is a repeatedly reused development benchmark. A fresh independent evaluation remains necessary.

### How does it compare with another open model?

On the same 1,991 text-decision questions, the recorded **Eikos-4B** run scored **{{EIKOS}}%** using our task adapter and its letter-based readout. This is a comparison under this project's protocol, not a general ranking of open models. [Eikos report](https://github.com/Jwuthri/SelfJev/blob/master/reports/eikos_4b/eval2/report.json)

**S1Bench** (the 13 public subsets pinned by Nimble, 3,880 items, run through lev's harness on 2026-09-30): SelfJev-4B Vision **74.8** macro accuracy; lev's card reports 68.9 for lev and 76.1 for Jev through the same harness. The other shared benchmarks: [Compared with open Jev-like models](#compared-with-open-jev-like-models).

{{COMPARISON}}

## Public datasets

![Accuracy for all 11 public-source datasets. Orange circles are SelfJev; green squares are Jev. Values are also available in the table below.](assets/public-datasets.png)

**{{PUBLIC_SCORE}}% across 3,300 questions.** There are 300 questions per source, so the macro average over sources and the question-weighted average are equal. The 171 authored development questions are excluded here; the full 3,471-question development benchmark remains available in the reports.

| Source dataset | Task in our protocol | Training exposure | Questions | SelfJev | Jev |
|---|---|---|---:|---:|---:|
{{PUBLIC}}

“Held-out source” means that dataset was excluded from SelfJev's task-specific training. “Seen source” means other rows from that source were used in training. Neither establishes absence from Qwen's pretraining.

**These are adapted tasks, not official dataset leaderboard scores.** For example, Banking77 uses eight candidate options per question, CLINC uses seven or eight, and DBpedia uses six. MNLI is recast as binary entailment. GoEmotions scores exact matching over six candidate tags. Our preprocessing, sampling and answer sets are part of the evaluation and must accompany the numbers.

Known development-data issues include shared MNLI premises across splits and near-duplicate authored policy texts. See [data methodology](https://github.com/Jwuthri/SelfJev/blob/master/docs/data.md). All 11 slices are shown, including weaker emotion and sentiment results.

[Download chart data](assets/public-datasets.csv) · [SelfJev predictions](https://github.com/Jwuthri/SelfJev/blob/master/reports/selfjev_4b_treeserver/test/report.json) · [Matched Jev predictions](https://github.com/Jwuthri/SelfJev/blob/master/reports/external/full/typesafe_jev-latest/report.json)

## Accuracy and model size

![Accuracy against nominal backbone parameters for seven measured systems on identical public-source questions. Full results below.](assets/accuracy-size.png)

| Model / recipe | Backbone size | Training | Accuracy | Evidence |
|---|---:|---|---:|---|
{{SIZE}}

All points use the same 3,300 question IDs, labels and candidate sets. The stock models are rerankers mapped to our decision tasks. The earlier LoRA runs use older training recipes; SelfJev uses a different backbone generation and more training data. This shows the measured systems' trade-off between size and accuracy. It does **not** isolate the effect of parameter count or establish that a 4B model outperforms larger models generally.

Sizes are nominal backbone parameter counts, not checkpoint megabytes or runtime memory. Jev appears as a horizontal reference because its parameter count is undisclosed. We do not assign a guessed size to proprietary models.

## AI response review

Breakdown of the 946-question authored suite, using the same current-engine predictions as the overview:

| Task | Questions | SelfJev | Jev |
|---|---:|---:|---:|
{{LLM}}

Labels were authored and checked with AI judges. Questions about one document are correlated; small differences should not be read as proof of superiority. This suite measures our defined answer choices and criteria, not unrestricted judgment quality. [Dataset design](https://github.com/Jwuthri/SelfJev/blob/master/docs/llm_eval_data.md) · [Predictions](https://github.com/Jwuthri/SelfJev/blob/master/reports/selfjev_4b_treeserver/eval_llm/report.json)

## Quickstart

On Linux with an NVIDIA GPU, Git and uv installed:

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/Jwuthri/SelfJev.git
cd SelfJev
uv sync --frozen --no-dev --extra serve --extra gpu
uv run --no-sync python - <<'PYTHON'
from huggingface_hub import snapshot_download
snapshot_download(
    "Jwuthrich/selfjev-4b",
    local_dir="weights/selfjev_4b_hf",
    allow_patterns=["adapter_model.safetensors", "adapter_config.json", "model.json"],
)
PYTHON

# Choose a secret for your own server.
export SELFJEV_API_KEYS="replace-with-your-long-random-secret"
uv run --no-sync selfjev serve \
  --adapter weights/selfjev_4b_hf --host 127.0.0.1 --port 8000
```

In another terminal, use the same secret:

```python
from selfjev import SelfJev, Noul, Choice

client = SelfJev(
    base_url="http://127.0.0.1:8000",
    api_key="replace-with-your-long-random-secret",
)
result = client.system_one(
    state="I was charged twice. Please refund the duplicate payment.",
    questions={
        "refund": Noul("Does the customer want a refund?"),
        "team": Choice(
            "Which team should handle this?",
            {
                "billing": "payments and refunds",
                "support": "technical issues",
            },
        ),
    },
)
print(result.nouls["refund"].noul)
print(result.choices["team"].choice)
```

The example shows the interface; it does not present fabricated model output. A generic Transformers text-generation or classification pipeline does not reproduce SelfJev's prompts, scoring rules or API. The server key is a secret you choose for your deployment, unrelated to Hugging Face credentials.

[HTTP API](https://github.com/Jwuthri/SelfJev/blob/master/docs/api.md) · [Self-hosting and AWS](https://github.com/Jwuthri/SelfJev/blob/master/docs/deploy.md) · [Fine-tuning](https://github.com/Jwuthri/SelfJev/blob/master/docs/finetune.md)

## Architecture

![The shared-prefix tree: one document feeds independent question branches; each question feeds its candidate branches; scores become option probabilities. Attention sees ancestors only, and DeltaNet inherits parent recurrent states.](assets/prefix-tree.png)

The default engine builds a **shared-prefix tree**: compute the document once, branch for each question, then branch for candidate answers. It reads yes/no evidence from the logits and converts those scores into the requested answer type. The server includes every candidate in the question, matching training.

The tree saves repeated computation at two levels: every question reuses the document, and every candidate reuses its question. In full-attention layers, the tree mask lets a branch read its ancestors but not sibling branches. In DeltaNet layers, branches inherit the recurrent state of their parent. Each candidate therefore sees its own document → question → candidate path, up to numerical differences between kernels. The diagram describes TreeServer; vLLM uses its own prefix-cache execution.

| Component | Current release |
|---|---|
| Backbone | Qwen3.5-4B |
| Base revision | `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a` |
| Fine-tuning | Rank-64 LoRA on attention and DeltaNet projections |
| Default serving | TreeServer, shared document and question computation |
| Alternative serving | vLLM with a merged checkpoint and prefix caching |
| Training examples | 79,943 non-test questions; texts up to 16K tokens |
| Training target | 50% checked labels + 50% stored Jev probabilities |
| Training schedule | One epoch, learning rate 2e-4 |

Jev probabilities served as a teacher signal; they did not decide the authored training labels. Authored labels were checked by an AI judge. Full lineage is recorded in [model.json](model.json), with architecture detail in the [research documentation](https://github.com/Jwuthri/SelfJev/blob/master/docs/tree_model.md).

## The research path

![Recorded accuracy for selected research checkpoints, from the first shared-prefix tree to the current serving engine.](assets/research-path.png)

The improvements came from several changes: verified difficult examples, the instruct backbone, explicit option lists, broader training coverage, tree-aware training and soft teacher targets. The chart is a history of complete systems, not an ablation assigning each gain to one change.

The research also includes smaller stock rerankers, 8B models, Jina, T5Gemma, custom architectures, distillation and RLCD. The [full experiment ledger](https://github.com/Jwuthri/SelfJev/blob/master/docs/experiments.md) records results and dead ends; earlier implementations remain at the archive tag documented there. The checkpoint's original engine recorded a slightly different text-decision score; this card consistently uses the current engine for SelfJev's headline results.

## Hardware and speed

A **24 GB NVIDIA GPU** is a practical starting recommendation, not a measured minimum. Plan for 16–32 GB host RAM and at least 50 GB free disk. The adapter download size does not describe inference memory: the full backbone and runtime state must fit too.

The default engine avoids token-by-token answer generation and shares work across questions. Latency still depends on input length, question count, candidate count, GPU and concurrency. We have two sets of measurements below, with different models and engines. **Current SelfJev-4B has no controlled NVIDIA latency sweep yet.** Its CPU minimum is also unmeasured.

### Earlier prototype on NVIDIA GPUs

![Median server processing time on A10G, L40S and H100, for one or sixteen questions across four text lengths. This is the archived Qwen3 model on vLLM, not the current SelfJev checkpoint.](assets/latency-gpu.png)

| Text tokens | Questions | A10G | L40S | H100 |
|---|---:|---:|---:|---:|
{{GPU_LATENCY}}

These are **server-side medians**, excluding network time: ten warmed, successful requests per point, one request at a time, three answer options per question. All three sweeps use the archived `tree_4b_combo` Qwen3-4B model on vLLM in bf16. They were recorded in separate runs, not a simultaneous controlled hardware experiment. The plot uses a labeled logarithmic time axis; the table gives the actual milliseconds.

These measurements show what the earlier system achieved; they are not a latency promise for the current Qwen3.5 model or the merged release. [A10G samples](https://github.com/Jwuthri/SelfJev/blob/master/reports/latency/requests_combo.jsonl) · [L40S samples](https://github.com/Jwuthri/SelfJev/blob/master/reports/latency/requests_qwen35.jsonl) · [H100 samples](https://github.com/Jwuthri/SelfJev/blob/master/reports/latency/requests_h100.jsonl)

### Current SelfJev-4B on Apple Silicon

![Current SelfJev-4B on Apple M5 Pro: local call latency for eight or 512 text tokens and one or sixteen questions. Exact measurements below.](assets/latency-mac.png)

| Text tokens | Questions | M5 Pro / 48 GB |
|---|---:|---:|
{{MAC_LATENCY}}

This uses the current adapter merged into Qwen3.5-4B, the TreeServer engine, and PyTorch MPS in bf16 on a 20-core Apple M5 Pro GPU with 48 GB unified memory. Each cell is the median of ten timed calls after two warmups, with MPS synchronized before and after each call. Inputs are synthetic repeated text, with three answer options per question. Timing includes tokenization and model work; it excludes HTTP/network.

The MPS run uses the slower PyTorch recurrent fallback. It is a lower-level engine experiment, **not a validated Mac server**. Model and engine differences prevent a hardware-only comparison against the NVIDIA chart. The merged download also has not been benchmarked through vLLM using these workloads.

[Download latency samples, configuration and medians](assets/latency-data.json) · [Latency CSV](assets/latency-data.csv) · [Full speed research](https://github.com/Jwuthri/SelfJev/blob/master/docs/speed.md)

## Limits and reproducibility

- **Probability is not a guarantee.** The reported current-engine runs have no fitted calibration attached. Validate thresholds on application data before acting on confidence.
- **Some tasks remain weak.** Emotion labeling, fine-grained sentiment and selecting an exact set of labels are visibly harder than topic and intent classification.
- **Benchmarks have a scope.** AI-authored tests, reused development sets, sampled options and known overlap issues limit the conclusions. We make no general state-of-the-art claim.
- **Engine versions matter.** These accuracy results refer to the recorded current TreeServer runs. A merged checkpoint, quantization or another serving backend needs its own verification.

Every plotted value is regenerated from saved predictions or raw timing samples. The generator checks matched IDs, targets, question types and candidate sets for report-to-report comparisons, and recomputes latency medians from ten timed samples per cell. [Chart data and source SHA-256 hashes](assets/chart-data.json) · [Generator](reproduce/build_model_card.py) · [Architecture and latency plotting module](reproduce/model_card_figures.py) · [Card template](reproduce/model_card.template.md)

Place the downloadable generator, plotting module and template in `scripts/docs/` of a SelfJev source checkout, then run:

```bash
uv run --no-project --with matplotlib==3.11.1 python scripts/docs/build_model_card.py
```

This builds figures from reports and the canonical `data/all.jsonl.gz`; it performs no model inference. Rebuild the canonical file using the [data instructions](https://github.com/Jwuthri/SelfJev/blob/master/data/README.md) if absent.

| File | Purpose |
|---|---|
| `adapter_model.safetensors` | Trained LoRA weights |
| `adapter_config.json` | PEFT configuration |
| `model.json` | Base revision, training provenance and original recorded scores |
| `assets/*.png`, `assets/*.svg` | Model-card figures, raster and vector |
| `assets/chart-data.json`, `assets/public-datasets.csv` | Underlying results and source provenance |
| `assets/latency-data.json`, `assets/latency-data.csv` | Selected raw timing samples, methodology and recalculated medians |

Adapter SHA-256: `dfbf2834d883987893ec305a6093a345fd79c77f903f60f2f914cbe3b6058d1b`.

The adapter uses the Qwen base model linked above. No separate adapter license is declared in this repository. Independent project; not affiliated with TypeSafe or Qwen.
