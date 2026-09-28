---
base_model: Qwen/Qwen3.5-4B
library_name: peft
model_type: qwen3_5
pipeline_tag: text-classification
tags:
  - decision-model
  - self-hosted
  - lora
---

# SelfJev-4B — release draft

**Publication status:** This card is a local draft. Do not upload the current adapter until its Jev-output training provenance has been cleared for redistribution. TypeSafe's [customer agreement, §2.3(b)](https://typesafe.ai/legal/mca) restricts using its outputs for model distillation, training an imitator, or developing a similar product. No exception has been documented in this project.

SelfJev-4B is a 230 MB PEFT LoRA adapter for [Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B) at revision `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`. It answers structured questions about a supplied text and returns choices or probabilities. It requires the [SelfJev serving engine](https://github.com/Jwuthri/SelfJev/blob/master/src/selfjev/engine/tree.py), which shares the text computation across questions and scores answer choices rather than generating text. Loading this adapter as a generic text-generation model will not reproduce SelfJev's API or evaluations. The base model weights are not included.

## Training

The adapter was trained from a new rank-64 LoRA on 79,943 non-test questions. Targets mixed checked authored labels with stored Jev probabilities at equal weight. Question prompts listed all answer options. The maximum training text length was 16K tokens. Full recipe and provenance are in the [model manifest](https://github.com/Jwuthri/SelfJev/blob/master/weights/selfjev_4b/model.json).

## Evaluation

With the current TreeServer engine, the recorded scores are 95.7% on 1,991 text decision questions, 93.1% on 946 AI response review questions, and 83.8% on 3,471 broader text questions used during development. These scores come from [recorded reports](https://github.com/Jwuthri/SelfJev/tree/master/reports/selfjev_4b_treeserver), not a new independent final test. The focused test labels were authored and checked by AI and may be wrong. The broader text benchmark was reused during development. Results on new application data may differ.

## Intended use

Use the SelfJev SDK or HTTP API to ask yes/no, single-choice, ordered-score, or select-all questions about text. See the [quickstart](https://github.com/Jwuthri/SelfJev/blob/master/docs/deploy.md) and [API contract](https://github.com/Jwuthri/SelfJev/blob/master/docs/api.md). Run on an NVIDIA GPU; 24 GB VRAM is a practical starting recommendation, not a measured minimum.

## Release checks

- Resolve the TypeSafe output-use restriction through documented permission, or train and evaluate a new adapter without Jev outputs before publishing weights.
- Review the licenses and provenance of every training source used by the released adapter.
- Set the adapter's own distribution license only after those rights are clear; the Qwen base model's Apache 2.0 license does not settle rights in the training data or this adapter.
- Recheck the selected adapter hash and scores against its own report files before upload.
