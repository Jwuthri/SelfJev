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
  - multimodal
  - image-classification
datasets:
  - timm/oxford-iiit-pet
  - zalando-datasets/fashion_mnist
  - AI-Lab-Makerere/beans
  - nateraw/rice-image-dataset
  - timm/eurosat-rgb
  - garythung/trashnet
---

# SelfJev-4B Vision

**Structured decisions from text and images. A 4B backbone. Your own GPU.**

The same decisions model as [SelfJev-4B](https://huggingface.co/Jwuthrich/selfjev-4b), now reading images as well as text:
ask yes/no, one-choice, scored or multi-select questions about a photo, a screenshot or a document, and get probabilities
back. It is the default model of [SelfJev](https://github.com/Jwuthri/SelfJev) since 2026-09-30.

This repository holds the **230 MB LoRA adapter**. The Qwen3.5-4B base (whose own vision encoder reads the image) downloads
separately.

## Quickstart

Image support needs `selfjev` 0.3.0 or later.

```bash
pip install "selfjev[serve,gpu]"
selfjev serve --adapter Jwuthrich/selfjev-4b-vision      # one CUDA GPU; an L40S was used below
```

```python
from pathlib import Path
from selfjev import Choice, Noul, SelfJev

client = SelfJev(base_url="http://localhost:8000")
res = client.system_one(
    state=[Path("cat.jpg")],                      # a Path, image bytes or a PIL image; text parts can sit next to it
    questions={
        "breed": Choice("What breed is it?", {"persian": "a Persian cat", "siamese": "a Siamese cat"}),
        "cat": Noul("Is there a cat in the photo?"),
    },
)
res.choices["breed"].choice, res.nouls["cat"].noul
```

On the wire an image is a base64 data URL (`data:image/jpeg;base64,…`) in `state`, alone or in a list with text. The image
is read once and every question is answered against it; images are resized to at most 1,024 × 1,024 pixels. Images need the
default engine (not `--engine vllm`).

## Results

Every number below comes from the report files in the GitHub repository (`reports/images_v1/`, `reports/external/`).

**Text: unchanged.** Paired with the text-only SelfJev-4B on the same engine, no benchmark differs significantly.

| benchmark | SelfJev-4B (text only) | **SelfJev-4B Vision** | Jev |
|---|---|---|---|
| eval2 (1,991 questions) | 95.68 | **96.13** | 97.24 |
| eval_llm (946, LLM prompts and outputs) | 93.13 | 92.49 | 92.5 |
| development benchmark (3,471) | 83.78 | **84.07** | 82.71 |

**Images.** A frozen test of 2,002 questions over 1,063 photos: about 100 test photos from each training dataset (never seen
in training) and four datasets never trained on at all.

| dataset | SelfJev-4B, zero-shot | **SelfJev-4B Vision** |
|---|---|---|
| rice varieties | 36.5 | **92.5** |
| EuroSAT land use (satellite) | 56.0 | **93.5** |
| bean leaf disease | 72.1 | **97.1** |
| TrashNet materials | 85.3 | **95.6** |
| Fashion-MNIST | 75.5 | **89.0** |
| Oxford-IIIT Pet breeds | 94.1 | **97.3** |
| **6 trained datasets** | 70.4 | **94.2** |
| snacks (never trained on) | 92.5 | 95.5 |
| indoor scenes (never trained on) | 94.8 | 95.5 |
| painting style (never trained on) | 70.6 | 70.6 |
| hurricane damage (never trained on) | 62.0 | 60.0 |
| **4 unseen datasets** | 83.5 | 84.3 |

The gains are on the kinds of images it was trained on; on new kinds of images it is about as good as before (+0.8, not
significant). For your own visual task, fine-tune on a few hundred labelled photos: `selfjev finetune` and the server's
fine-tuning endpoint take image rows.

**Speed** (one L40S, one warm request, median): text with one question 136 ms; one image with one question 163 ms; one image
with five questions 167 ms. The first image request after start-up loads the vision encoder; `selfjev serve` does that
during its warm-up.

<!-- selfjev:comparison:start -->
## Compared with open Jev-like models

*Measured 2026-09-30.* Eight open "Jev-like" decision models from Hugging Face and SelfJev were each served with
their card's recommended setup on the same GPU (one NVIDIA L40S) and asked exactly the requests TypeSafe's Jev receives.
A request a model cannot answer counts as wrong. Jev is shown for reference.

**SelfJev's test suites.** Text Decisions (1,991 questions) and AI Response Review (946), published as
[selfjev-decision-bench](https://huggingface.co/datasets/Jwuthrich/selfjev-decision-bench), and photos:

| model | size | images | licence | Text Decisions | AI Response Review | held-out images | Text Decisions time (s) |
|---|---|---|---|---|---|---|---|
| Jev 1.13 (TypeSafe API, reference) | ? | no | paid API | 97.2 | 92.5 | — | — |
| [openjev](https://huggingface.co/openjev/openjev) | 27B | yes | CC-BY-NC-4.0 | 96.8 | 92.6 | 82.6 | 753 |
| [**SelfJev-4B Vision**](https://huggingface.co/Jwuthrich/selfjev-4b-vision) | 4B | yes | Apache-2.0 code | 94.7 | 90.7 | 85.1 | 166 |
| [Plumb-4B](https://huggingface.co/crh225/plumb-4b) | 4.2B | no | Apache-2.0 | 93.4 | 84.1 | — | 471 |
| [jpt-4b](https://huggingface.co/kirp/jpt-4b) | 4.5B | yes | CC-BY-NC-4.0 | 92.5 | 85.0 | 83.8 | 90 |
| [imajev-4b](https://huggingface.co/mohit67890/imajev-4b) | 4B | yes | Apache-2.0 | 91.5 | 84.9 | 85.2 | 489 |
| [decider-4b](https://huggingface.co/Mapika/decider-4b) | 4.2B | no | Apache-2.0 | 90.8 | 82.8 | — | 145 |
| [Mica-v0.1-4B](https://huggingface.co/sky7350/Mica-v0.1-4B) | 4.2B | no | Apache-2.0 | 89.6 ² | 84.1 ² | — | 162 |
| [kev-4b](https://huggingface.co/jaredpalmer/kev-4b) | 4B | no | Apache-2.0 | 88.4 | 74.7 | — | 109 |
| [Laya](https://huggingface.co/convaiinnovations/laya) | 0.4B | no | Apache-2.0 | 45.4 | 46.4 | — | 23 |

- Every model gets the same Jev-shaped questions; select-all questions become one yes/no per option, which costs SelfJev
  1.4–1.8 points against its native evaluation (96.1 and 92.5). **Held-out images**: the 4 image datasets of the SelfJev
  image test that none of these models trained on (772 questions). **Time**: Text Decisions end to end, 4 requests in
  flight. ² Refuses inputs over 8,192 tokens (2 % and 1 % of the questions), counted wrong.
- No other model trained on these suites, but they come from the same authors and judges as SelfJev's training data,
  so they favour SelfJev.
- SelfJev is the most accurate open model at 4.5B parameters or less on both suites (paired tests, p ≤ 0.023) and ties
  imajev-4b on held-out images; the 27B openjev is higher on Text Decisions. It is slower than most 4B models here.

Protocol, per-model setups, paired tests and raw reports: [reports/competitors](https://github.com/Jwuthri/SelfJev/blob/master/reports/competitors/README.md).
<!-- selfjev:comparison:end -->

## Training

Continued from SelfJev-4B for one epoch (622 steps, learning rate 5e-5) on a 1:1 mix: 11,344 image questions (a multiple
choice among up to 12 classes and a yes/no per photo, about 1,000 photos per dataset) and 11,344 text questions replayed
from SelfJev-4B's own training data, whose targets mix the verified label with Jev's probabilities. The vision encoder is
frozen; only the language-model LoRA (rank 64) trains. Recipe and data build: `scripts/data/build_images_v1.py`.

Training images and their licences: Oxford-IIIT Pet (CC BY-SA 4.0), Fashion-MNIST (MIT), beans (MIT), rice images (CC0 1.0),
EuroSAT (MIT), TrashNet (MIT). The text data and its licence notes are those of SelfJev-4B.

## Limitations

- Image skill beyond the six trained kinds of images is the base model's own: no significant transfer was measured.
- One run, one seed; the image test has about 100 photos per dataset.
- eval_llm is 0.6 points below the text-only release (not significant).
- The answer only reflects what the image shows at up to 1,024 × 1,024 pixels.
