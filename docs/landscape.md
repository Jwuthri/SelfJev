# Jev and open alternatives

## What Jev is

Jev (TypeSafe, `typesafe/jev`, served through OpenRouter) turns a model into a typed decision engine: send a text (the
*state*) and questions of type `noul` (yes/no), `choice` or `score`, get typed answers with probabilities, with no text
generation. SelfJev copies the **interface**, not the model: `selfjev serve` answers Jev's requests at Jev's paths
(`/v1/systemone`, `/api/alpha/decisions`, `/v1/decisions`), so Jev clients work by changing the base URL and the key
([API](api.md), [how it works](how_it_works.md)).

**What TypeSafe discloses** (public web, read 2026-09-23):

- "Transformer-based, but it is not a large language model", with a "new model architecture, parallel sampler": all
  outputs come from one pass.
- Questions run "in parallel and in isolation against the same state". That is the shape of our shared-prefix tree.
- Limits: 64K tokens per request; 32K for the state plus the longest question. Rate limit 250K tokens/s.
- Training: "Reinforcement Learning for Calibrated Decisions (RLCD)", no details. Their benchmark's reference answer is
  the average of GPT-6 Astra and Fable 5.1.
- Not disclosed: size, base model, data. They "cannot prove the price is unsubsidized".

Sources: typesafe.ai/blog/introducing-system-one-models-and-jev, docs.typesafe.ai/models.md,
marktechpost.com/2026/09/19/typesafe-ai-releases-jev/.

**What we measured about it:**

| | result |
|---|---|
| accuracy | eval2 97.2%, eval_llm 92.5%, dev benchmark 82.7% (GPT-6 Astra 85.8%) |
| weakest slices | eval2: temporal 89.2, numeric 92.0, multilabel exact match 94.2; eval_llm: verify 86.7, multilabel exact match 81.3 |
| latency | flat 143–178 ms p50 from California, 8 → 4,096 tokens, 1 or 16 questions |
| marginal speed | 132–137 ms fixed + 2.2–2.6 ms per 1,000 tokens ≈ 400K tokens/s |
| long texts | reads the whole text: 97.2% on evidence at the end of 4K–17.6K-token texts |
| tokenizer | its billed token count is 1.036× Qwen's, so probably not the Qwen tokenizer |
| price | $0.042 per million input tokens; the whole dev benchmark cost $0.06 |
| as an annotator | agrees with authoring models on 93.0% of round-2 questions; worst on temporal |

**Our reading** (2026-09-25 update: [what Jev's behaviour implies and what to build next](../reports/jev_hypothesis_2026-09-25.md)):
the gap is mostly training, not architecture. 4B → 8B, a bigger adapter and stock → tree each moved
the dev benchmark by ≤ 1.3 points, while 10K verified target-task questions moved eval2 by +5.5. Our default model,
`selfjev-4b`, is now 1.4 points behind on eval2 (95.8), level on eval_llm (93.1, p = 0.52) and ahead on the dev
benchmark (83.8). Jev's speed is mostly the hardware: on one H100 our Qwen3 4B tree is faster than Jev inside the
machine in every cell but 4,096 tokens × 16 questions (2026-09-26, [speed](speed.md#the-same-model-on-an-h100-2026-09-26));
Jev's per-token cost is still ≈ 6× lower than ours, so a smaller model or more GPUs per request, and the end-to-end
difference is network distance. `selfjev-4b`'s own serving engine is not timed on a GPU yet.

## The open field and the shared yardsticks (survey 2026-09-30)

About 50 model cards read from [HF `other=classification`](https://huggingface.co/models?other=classification)
(sorted by downloads, likes and trending, created since 2026-09-15), plus the benchmarks they cite. Nothing was run for
the survey. Session: Claude competitors, JOURNAL 2026-09-30.

**Shared yardsticks.** These are the only places where our numbers and theirs can meet:

| benchmark | what | size | who runs it | cited by |
|---|---|---|---|---|
| [JevBench](https://github.com/fstandhartinger/jevbench) (Benchmark Heaven, MIT, not TypeSafe's) | public easy/original/hard items; live board [benchmarkheaven.com/jev-models](https://benchmarkheaven.com/jev-models) | public 231 (48/72/111); board v1.5.4 scores 1,624 per system, 720 sealed | board: maintainers only; public-231: anyone, `typesafe` adapter on `/v1/systemone` | ≈ 15 cards |
| [LocalLLaMA/typed-decisions](https://huggingface.co/datasets/LocalLLaMA/typed-decisions) | 4 synthetic workflows, one request per case; gold = a ≈4B teacher, ceiling 0.735 | test 400 cases / 2,000 decisions | anyone | ≈ 10 cards |
| [Decision Index 0.2.1](https://huggingface.co/spaces/multimodalart/jev-decision-index) | 38 public benchmarks, chance-corrected `balanced_skill` | ≈ 120K requests, rebuild ≈ 7 GB | maintainer board; kit is open | ≈ 6 cards |
| Nimble 13-subset suite ("S1Bench", [PUBLIC_BENCHMARKS.md](https://github.com/bespokelabsai/nimble/blob/main/docs/PUBLIC_BENCHMARKS.md)) | human labels: VitaminC, MASSIVE en/de, BoolQ, SQuAD2, PAWS, MNLI, Civil Comments, Aegis2, HelpSteer2, SummEval ×2, PubMedQA | 3,880 | anyone (lev's `levbench`) | lev, decider, Nimble |
| [DecisionBench 1.0](https://huggingface.co/datasets/Hanno-Labs/decision-bench) (Hanno Labs) | 43 tasks, up to 255 candidates | 23,900 | board + open runner | imajev, Bosun, Winnow |
| [Image JevBench](https://benchmarkheaven.com/image-jev-bench) v0.1.4 | images | 684 (228 public) | maintainers | board only |

**Overlap check** (exact + 8-gram, `data/all.jsonl.gz` vs the benchmark states): JevBench public-231 0 / 231,
typed-decisions test 0 / 400. We never trained on either. On the Nimble suite, MNLI's train split is in our `hf_nli`.

**Accuracy matrix, published numbers only (%).** B = run by the board's maintainers, S = self-reported by the model's
author, † = the author used the public items for model selection or tuning, F = fitted on the benchmark's train split.
JevBench public-231 totals come from the per-tier numbers on each card where the card gives no total.

| model | params | images | JevBench public-231 | JevBench hard-111 | JevBench board v1.5.4 (rank) | Decision Index 0.2.1 | typed-decisions | Nimble 13 macro | DecisionBench | Image JevBench (rank / 50) |
|---|---|---|---|---|---|---|---|---|---|---|
| **selfjev-4b-vision (ours)** | 4B | yes | not run | not run | not submitted | not run | not run | not run | not run | not submitted |
| Jev 1.13.0 (API) | ? | no | 86.6 B | 73.0 B | 72.1 (#3) | 57.91 B | 72.7 | 76.0 S (Nimble) | 72.0 B | — |
| Cygnet (API) | ? | ? | 87.9 S (basal) | — | 73.7 (#1) | — | — | — | — | — |
| Winnow-12B | 12B | ? | 85.7 S | 73.0 B | 73.2 (#2) | 50.02 B | — | — | 76.7 B | — |
| JevK5 v0.3 | 4B | no | 87.9 S | 78.4 S | 71.9 (#4) | 38.81 B | — | — | — | — |
| Plumb-4B (JevK5-based) | 4B | no | 89.6 S† | 80.2 S† | 71.6 (#5) | — | — | — | — | — |
| decider-4b (v2 / v2.1) | 4B | no | 83.5 B (v2) / 82.7 S | 67.6 / 64.9 S | 71.3 (#7) | 40.70 B | — | 75.6 S | — | — |
| decider-2b (255K dl/30 d) | 2B | sibling | 71.0 B | 49.5 B | 45.1 (#30) | — | — | 70.6 S | 61.4 B | — |
| Wald-4B | 4B | no | 87.9 S† | 74.8 S† | not listed | 54.59 S (pending) | — | — | — | — |
| jpt-4b (NC licence) | 4B | yes | 87.9 S | 78.4 S | not listed | 43.04 B | 79.6 S F | — | — | 69.55 (#6) |
| jpt-9b (NC licence) | 9B | yes | 85.3 S | 73.0 S | not listed | 46.89 B | 80.6 S F | — | — | 65.82 (#12) |
| imajev-4b | 4B | yes | — | — | #1 on v1.4.2.2 (67.37) | — | — | — | 79.7 B | 76.39 (#1) |
| Mica-v0.1-4B | 4B | no | 83.1 S† | 64.9 S† | not listed | — | — | — | — | — |
| kev-4b | 4B | no | 75.8 S / 66.2 B (older build) | 54.1 S / 36.9 B | 38.1 (#37) | 34.64 B | — | — | 65.2 B | — |
| lev (interfaze-ai) | 4B | no | — | — | not listed | 38.54 B | — | 68.9 S (Jev 76.1, same harness) | — | — |
| Eikos-4B | 4B | no | — | 72.1 S | not listed | — | — | — | — | — |
| AutoJev-27B | 27B | yes | 87.0 S (basal) | 70.3 S (101 items) | 19.5 (#52, cost) | 56.40 B | — | — | — | 66.85 (#9) |
| openjev (27B, NC licence) | 27B | yes | — | — | not listed | — | — | — | — | — |
| Nimble-9B | 9B | no | 79.7 B | 62.2 B | 31.8 (#40) | — | — | 74.8 S | — | — |
| vjev-vision (distilled from Jev) | 4B | yes | — | — | — | — | — | — | — | 47.67 (#31) |
| Laya (the most liked, 4.6K) | 0.4B | no | 58.4 B | 35.1 B | 0.0 (#93) | 6.04 B | 36.2 S (base) / 76.6 S F | 62.5 B (6-subset) | 39.2 B | — |

On our own frozen sets the only open model scored so far is Eikos-4B: eval2 92.8 (`reports/eikos_4b/eval2`), against
selfjev-4b-vision 96.1 and Jev 97.2.

**What the survey says about our claims.**

- *Architecture.* The shared prefix is common now: Mica shares one prefill across questions, kev continues each
  question from the shared state, ArseneLupin has a `shared_prefix` mode, decider and Eikos lean on vLLM prefix caching.
  What remains ours: each candidate is scored from its own description inside one tree pass (no A–Z letter slot, no
  26/52-option chunking) and multilabel is native. Most others read letter logits; several cap options at 16–26.
- *Text and images in one model* is not unique: jpt-4b/9b, imajev-4b, openjev, vjev-vision, AutoJev-27B and
  decider-2b-vision take images too. imajev-4b leads Image JevBench (76.39). Our image test is mostly in distribution
  (JOURNAL 2026-09-30 02:05: no transfer to new image tasks), so a public image board is where this claim gets tested.
- *Real data.* Most cards report on their own sets or on public items they tuned against (†). Maintainer-run numbers
  (B) are rare and worth more: sealed accuracy on JevBench is far below public for everyone (Jev 36.7 sealed vs
  86.6 public on v1.4.2.2).
- Laya is the most liked but the weakest here: JevBench board #93, Decision Index 6.04, a ≈ 320-token state window.

## Open "Jev-like" models (survey of Hugging Face model cards, 2026-09-24)

Nothing was downloaded or run for the survey (Eikos-4B was scored later, below); claims are each model's own, on its
own benchmark, and **not comparable with ours**.

| camp | models | notes |
|---|---|---|
| small encoders, 0.15–0.4B | Laya (ModernBERT / mmBERT), open-jev-deberta-v3-large, rlcd-modernbert-151m (GLiClass) | advertise 33–46 ms; long texts truncated |
| decoders with answer-token readout (mostly LoRA), 0.6–27B | kev 0.5/0.8/4/9B, decider 0.8/2/4/35B-A3B, openjev, Bespoke-Nimble-9B, AutoJev-27B, Lumma-fev-0.6b, Eikos-4B | mostly Qwen3.5 bases; same recipe as ours (LoRA, logit readout, no generation) |

- Their claims: AutoJev-27B 84.6 vs Jev 82.8; kev-4b beats Jev in distribution but trails out of domain (0.817 vs
  0.857); kev-0.8b trails everywhere; decider-35b-a3b JevBench hard 0.676, decider-4b 0.541.
- The same pattern as ours: sub-1B trails, 4B and up is where the quality is.
- "JevBench" public items exist and several cards report on them: the only shared yardstick. Scoring our tree on it is
  an [open idea](next.md).

### Laya (reviewed at commit `970dc8c`)

- A bidirectional encoder (ModernBERT-large 421M, or mmBERT-base 322M multilingual), one sequence per question with
  every option and the state; a new 2-layer transformer head scores each option's `[MASK]`. Trained with a GRPO-style
  policy gradient on proper-scoring-rule rewards, which it calls RLCD.
- Documented limits: the state is truncated to ≈ 320 tokens by default (≈ 768 multilingual, up to 8K opt-in), options
  share a 192–256-token budget, base checkpoints near chance zero-shot on its own set, over-confident before temperature
  fitting (ECE 0.466 → 0.081).
- Its Jev latency figure (236–276 ms p50) is slower than we measured (143–178 ms).
- Verdict: the faster and multilingual option (≈ 33 ms on a T4), not the more accurate one on long, trap-heavy texts.
  Our closest measured analogue, jina 0.6B listwise, scores 73.3 on eval2. Scoring Laya on eval2 is open (no API cost;
  a small GPU box, never the laptop).

### Eikos-4B (`caiovicentino1/Eikos-4B`, MIT)

- A full fine-tune of Qwen3.5-4B distilled from GLM-5.3-Flash on finance and rules data; options as letters, softmax
  over the letter logits.
- vLLM ≥ 0.30 with `--enable-prefix-caching --mamba-cache-mode all` shares the state across questions (the card
  reports that vLLM 0.11 lost 3–6 points on batched long shared documents).
- Own-harness claims: JevBench public hard 72.1 (Jev 73.0 on the official leaderboard), ECE 0.033.
- Evidence that the Qwen3.5 base works for typed decisions. Zero-shot through our option mapping it scores 92.8 on
  eval2 (`reports/eikos_4b/`). Qwen3.5-4B has been the base of our best models since 2026-09-25, `selfjev-4b`
  included.

### Qwen3.5 and Qwen3.8 as bases

- Qwen3.8 has no small dense model: 27B (48 linear-attention + 16 full layers), a 180B MoE and a 2.4T MoE.
- Qwen3.5 has 0.8/2/4/9/27B; the 4B has 32 layers (24 Gated DeltaNet + 8 full attention) and 262K positions. A tree
  mask cannot branch its linear-attention layers in one pass. First a forked native cache did it
  ([challengers](challengers.md#qwen35-2b-linear-attention-with-a-forked-cache)); now our Qwen3.5 tree
  (`src/selfjev/engine/tree.py`) runs those layers level by level from copied states, in training and serving
  ([tree scorer](tree_model.md#qwen35-hybrid-deltanet)).
