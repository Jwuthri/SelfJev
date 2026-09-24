# Jev and open alternatives

## What Jev is

Jev (TypeSafe, `typesafe/jev`, served through OpenRouter) turns a model into a typed decision engine: send a text (the
*state*) and questions of type `noul` (yes/no), `choice` or `score`, get typed answers with probabilities, with no text
generation. SelfJev copies the **interface**, not the model: our native schema is our own, and `pjev serve` also
exposes a route with the same request/response shape ([how it works](how_it_works.md)).

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
| accuracy | eval2 97.2%, dev benchmark 82.7% (GPT-6 Astra 85.8%) |
| weakest slices on eval2 | temporal 89.2, numeric 92.0, exception 95.3, paraphrase 95.4 |
| latency | flat 143–178 ms p50 from California, 8 → 4,096 tokens, 1 or 16 questions |
| marginal speed | 132–137 ms fixed + 2.2–2.6 ms per 1,000 tokens ≈ 400K tokens/s |
| long texts | reads the whole text: 97.2% on evidence at the end of 4K–17.6K-token texts |
| tokenizer | its billed token count is 1.036× Qwen's, so probably not the Qwen tokenizer |
| price | $0.042 per million input tokens; the whole dev benchmark cost $0.06 |
| as an annotator | agrees with authoring models on 93.0% of round-2 questions; worst on temporal |

**Our reading:** the gap is mostly training, not architecture. 4B → 8B, a bigger adapter and stock → tree each moved
the dev benchmark by ≤ 1.3 points, while 10K verified target-task questions moved eval2 by +5.5. Its speed points to a
small model (~1B active parameters) on fast GPUs.

## Open "Jev-like" models (survey of Hugging Face model cards, 2026-09-24)

Nothing downloaded or run; claims are each model's own, on its own benchmark, and **not comparable with ours**.

| camp | models | notes |
|---|---|---|
| small encoders, 0.15–0.4B | Laya (ModernBERT / mmBERT), open-jev-deberta-v3-large, rlcd-modernbert-151m (GLiClass) | advertise 33–46 ms; long texts truncated |
| LoRA on decoders with answer-token readout, 0.6–27B | kev 0.5/0.8/4/9B, decider 0.8/2/4/35B-A3B, openjev, Bespoke-Nimble-9B, AutoJev-27B, Lumma-fev-0.6b, Eikos-4B | mostly Qwen3.5 bases; same recipe as ours (LoRA, logit readout, no generation) |

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
  Our closest measured analogue, jina 0.6B listwise, scores 73.3 on eval2. Scoring Laya on eval2 is free and open.

### Eikos-4B (`caiovicentino1/Eikos-4B`, MIT)

- A full fine-tune of Qwen3.5-4B distilled from GLM-5.3-Flash on finance and rules data; options as letters, softmax
  over the letter logits.
- vLLM ≥ 0.30 with `--enable-prefix-caching --mamba-cache-mode all` shares the state across questions (the card
  reports that vLLM 0.11 lost 3–6 points on batched long shared documents).
- Own-harness claims: JevBench public hard 72.1 (Jev 73.0 on the official leaderboard), ECE 0.033.
- Evidence that the Qwen3.5 base works for typed decisions; see the Qwen3.5-4B [open idea](next.md).

### Qwen3.5 and Qwen3.8 as bases

- Qwen3.8 has no small dense model: 27B (48 linear-attention + 16 full layers), a 180B MoE and a 2.4T MoE.
- Qwen3.5 has 0.8/2/4/9/27B; the 4B has 32 layers (24 Gated DeltaNet + 8 full attention) and 262K positions. Our tree
  cannot branch its linear-attention layers in one pass; a forked native cache can
  ([challengers](challengers.md#qwen35-2b-linear-attention-with-a-forked-cache)).
