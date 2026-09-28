---
base_model: Qwen/Qwen3.5-4B
base_model_relation: finetune
library_name: transformers
pipeline_tag: text-classification
tags:
  - decision-model
  - self-hosted
  - merged
  - selfjev
---

# SelfJev-4B — merged weights

SelfJev turns text and questions into structured decisions: yes/no probabilities, one choice, an ordered score, or every option that applies. It runs on your own GPU and exposes a Python SDK and HTTP API.

This repository contains the **full Qwen3.5-4B checkpoint with the SelfJev LoRA merged into its language-model weights**, plus the tokenizer and configuration. It does not require a separate base-model or adapter download. The base is pinned to `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`.

The compact [adapter release](https://huggingface.co/Jwuthrich/selfjev-4b) contains the same fine-tuning weights separately. This merge preserves the original checkpoint layout, including the unmodified vision weights; SelfJev was trained and evaluated for text decisions only.

[Source code](https://github.com/Jwuthri/SelfJev) · [API reference](https://github.com/Jwuthri/SelfJev/blob/master/docs/api.md) · [Research notebook](https://jwuthri.github.io/SelfJev/)

## Use it

SelfJev requires its custom serving engine. It reuses the document computation across questions and scores answer choices directly, with no generated text. A generic Transformers text-generation or text-classification pipeline does not reproduce this API or the reported scores.

On a Linux NVIDIA GPU machine with uv, Git and a compatible vLLM installation, install SelfJev into that environment and download the complete checkpoint:

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/Jwuthri/SelfJev.git
cd SelfJev
# Run in your vLLM Python environment.
python -m pip install -e '.[serve]'
python - <<'PYTHON'
from huggingface_hub import snapshot_download
snapshot_download("Jwuthrich/selfjev-4b-merged", local_dir="weights/selfjev_4b_merged")
PYTHON

export SELFJEV_API_KEYS="replace-with-your-long-random-secret"
selfjev serve --engine vllm --model-dir weights/selfjev_4b_merged --host 127.0.0.1 --port 8000
```

Use SelfJev's vLLM backend for this checkpoint. The default TreeServer installation instructions use the separate adapter release. vLLM and Transformers must support Qwen3.5; a generic chat endpoint does not implement SelfJev's decision scoring.

In a separate terminal, use the same secret with the client:

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
        "team": Choice("Which team should handle this?", {
            "billing": "payments and refunds",
            "support": "technical issues",
        }),
    },
)
print(result.nouls["refund"].noul)
print(result.choices["team"].choice)
```

A 24 GB NVIDIA GPU is a practical starting recommendation, not a measured minimum. Plan for 16–32 GB host RAM and at least 50 GB free disk. Current-model GPU latency and a full-model CPU minimum have not been established. See the [deployment guide](https://github.com/Jwuthri/SelfJev/blob/master/docs/deploy.md) for Docker and AWS.

## Architecture and training

- Base: Qwen3.5-4B, with a rank-64 LoRA on attention and DeltaNet projections.
- Shared-prefix tree: read the document once, then evaluate questions and their answer choices in separate branches.
- Training: 79,943 non-test questions, one epoch, learning rate 2e-4, texts up to 16K tokens.
- Targets: 50% checked labels and 50% stored Jev probabilities as a teacher signal. Authored labels were checked by an AI judge; Jev predictions did not determine authored labels.
- All answer options are included in each question. The serving engine applies this transformation automatically.

See [model.json](./model.json) for the original manifest, checkpoint and provenance. Independent project; not affiliated with TypeSafe or Qwen.

## Recorded results

These are reference results for the source adapter using the **TreeServer engine**. They are not a new evaluation of this merged artifact or its vLLM backend:

| Task | Questions | Accuracy | Evidence |
|---|---:|---:|---|
| Text decisions | 1,991 | 95.7% | [report](https://github.com/Jwuthri/SelfJev/blob/master/reports/selfjev_4b_treeserver/eval2/report.json) |
| AI response review | 946 | 93.1% | [report](https://github.com/Jwuthri/SelfJev/blob/master/reports/selfjev_4b_treeserver/eval_llm/report.json) |
| Broader text tasks (development benchmark) | 3,471 | 83.8% | [report](https://github.com/Jwuthri/SelfJev/blob/master/reports/selfjev_4b_treeserver/test/report.json) |

Accuracy is the share of questions matching the expected answer. For select-all questions, the entire set must match. The two focused test sets were authored and checked by AI; their labels are not human ground truth. They have informed research direction, and a fresh final holdout remains necessary. The broader text benchmark was repeatedly used during development. Scores are single-run observations, not guarantees on application data.

The same adapter scored 95.8% on text decisions under the original evaluation engine. `model.json` preserves those original scores; the table above reports current serving-engine measurements. Historic latency results for earlier Qwen3 prototypes do not establish current SelfJev-4B latency.

## Artifact integrity

The source adapter SHA-256 is:

```
dfbf2834d883987893ec305a6093a345fd79c77f903f60f2f914cbe3b6058d1b
```

The base model license and any supplied notices are retained from the pinned Qwen checkpoint. No separate license for the SelfJev fine-tuning contribution has been declared. `merge_meta.json` records the base revision, source adapter hash, dtype and number of merged tensors; `SHA256SUMS` records the release file hashes.
