# Image datasets for fine-tuning

Where to find labelled images to teach `selfjev-4b` a visual task, checked on the Hugging Face API on 2026-09-29 (rows,
classes and licence as the dataset card states them; a blank licence means the card gives none: treat it as research-only).
Turn any of them into fine-tuning rows with one command:

```bash
uv run --group data python scripts/data/hf_images_to_rows.py ethz/food101 --split train --out data/food_train.jsonl \
    --question "What dish is in this photo?" --per-class 40      # streams, never downloads the whole set
```

Each photo becomes a multiclass question (the true class among 12 random ones) and a yes/no one; `selfjev finetune --data`
reads the file, and the fine-tuning endpoint takes the same photos as `state` (a data URL, or a list of text and image parts).
The frozen vision tower encodes the image; only the language LoRA trains. Mix in text rows (`data/all.jsonl.gz`) so the
model keeps its text skills.

| dataset (HF id) | task | classes | rows | licence | note |
|---|---|---|---|---|---|
| `timm/oxford-iiit-pet` | pet breeds | 37 | 3.7K + 3.7K | CC BY-SA 4.0 | our test set `data/eval_pets.jsonl` is its test split |
| `zalando-datasets/fashion_mnist` | clothing type | 10 | 60K + 10K | MIT | tiny 28 px grey images |
| `AI-Lab-Makerere/beans` | bean leaf disease | 3 | 1.3K | MIT | |
| `nateraw/rice-image-dataset` | rice variety | 5 | 75K | CC0 | |
| `Bingsu/Cat_and_Dog` | cat or dog | 2 | 10K | CC0 | |
| `Matthijs/snacks` | snack type | 20 | 4.8K | CC BY 4.0 | |
| `jonathan-roberts1/Satellite-Images-of-Hurricane-Damage` | damage yes / no | 2 | 10K | CC BY 4.0 | aerial |
| `Falah/Alzheimer_MRI` | MRI stage | 4 | 6.4K | Apache-2.0 | medical: a demo, not a product |
| `ethz/food101` | dishes | 101 | 75K + 25K | none stated (scraped) | research use |
| `uoft-cs/cifar100`, `uoft-cs/cifar10` | objects, 32 px | 100 / 10 | 60K each | none stated | |
| `tanganke/dtd` | textures | 47 | 3.8K + 1.9K | none stated | |
| `tanganke/eurosat` | land use, satellite | 10 | 21.6K + 2.7K | none stated | |
| `tanganke/gtsrb` | German traffic signs | 43 | 26.6K + 12.6K | none stated | |
| `tanganke/stanford_cars` | car model | 196 | 8.1K + 8.0K | none stated | |
| `tanganke/sun397` | scenes | 397 | 19.9K + 19.9K | none stated | more than 255 classes: the converter samples 12 options |
| `Donghyun99/CUB-200-2011` | bird species | 200 | 6.0K + 5.8K | none stated | |
| `dpdl-benchmark/oxford_flowers102` | flowers | 102 | 1K + 6.1K | none stated | |
| `dpdl-benchmark/caltech101` | objects | 102 | 3.1K + 6.1K | none stated | |
| `zh-plus/tiny-imagenet`, `timm/mini-imagenet` | objects, 200 / 100 classes | 200 / 100 | 100K / 50K | none stated / other | ImageNet subsets |
| `ILSVRC/imagenet-1k` | objects | 1,000 | 1.3M | gated, research | needs a Hugging Face login and the terms |
| `clip-benchmark/wds_*` (aircraft, country211, resisc45, pcam, …) | the CLIP benchmark suite | varies | varies | none stated | WebDataset shards; another 20 tasks |

Licences decide what can ship: a model trained on "none stated" or research-only data should stay a research model.
The cleanly licensed rows above (CC0, MIT, CC BY, Apache) are safe for the released weights.

## Test sets (frozen: never train on them)

| file | what | built by |
|---|---|---|
| `data/ova/eval_pets.jsonl` | Oxford-IIIT Pet test split: cat breed (12), all breeds (37), is it a cat; 1,853 questions | `scripts/data/build_eval_pets.py` |
| `data/ova/eval_images_v1.jsonl` | test photos of the 6 images-v1 training datasets + 4 held-out classification sets (hurricane damage, snacks, indoor scenes, painting style); 2,002 questions | `scripts/data/build_images_v1.py` |
| `data/ova/eval_images_heldout.jsonl` | **the generalization test**: 7 question-answering sets no mix may train on, photos and documents, human labels; 1,027 questions over 842 images (sha256 `7865bfc8…`) | `scripts/data/build_eval_images_heldout.py` |

The generalization test, per dataset (150 questions sampled at random each, VizWiz 127; DocVQA and others can ask two
questions about one image):

| dataset | images | questions | licence |
|---|---|---|---|
| TextVQA (validation) | photos with text (Open Images) | read the text: brand, sign, number | CC BY 4.0 |
| VizWiz (validation) | phone photos taken by blind people | everyday questions; answers >= 3 of 10 annotators agree | CC BY 4.0 |
| DocVQA (validation) | scanned documents | find a value, date, name | mirror card: Apache-2.0; check the original's terms |
| ChartQA (human test) | charts | read and compare values | GPL-3.0 |
| RealWorldQA (test) | driving and street photos | spatial, counting, directions | mirror card: CC BY 4.0; check the original's terms |
| AI2D (test) | science diagrams | diagram reasoning | not stated on the mirror; check the original's terms |
| CV-Bench (test, no COCO images) | indoor and outdoor scenes | counting, relations, depth, distance | Apache-2.0 |

Open answers become a multiple choice among the answer and 3 wrong ones of the same shape (numbers: x0.5 / x0.75 / x1.25 /
x1.5, never within 5%, never over 100 for a percentage; text: another question's answer with digits if the answer has
them, about as many words, that no annotator gave); yes/no answers become binary questions. Their images come from none of
the sources a training mix uses (COCO and Visual Genome for VQAv2, A-OKVQA and GQA). UI screenshots are not covered yet
(no loadable screen-QA set found). Test-only use: none of these reach the weights, whatever their terms.

## Beyond fixed labels

A classifier set fixes one question per photo. `selfjev`'s text data works the other way: an LLM writes many typed questions
per state, an authored target is checked by a blind judge (`scripts/data/gen_hardcases.py`, `judge_hardcases.py`). The image
version is the same recipe over photos with a licence that allows it (COCO and Open Images photos are CC BY 2.0) and a vision
model as writer and judge: "is anyone wearing a helmet", "which of these describes the scene", counting, colours. It costs API
money (about the text batches' price per question), so it needs the user's OK first.
