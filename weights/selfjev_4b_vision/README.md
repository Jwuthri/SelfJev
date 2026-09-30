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
