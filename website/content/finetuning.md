Adapt SelfJev to your own decisions with supervised fine-tuning, or optimize probability reports using the RLCD objective. A 48 GB GPU is the established training class. Keep a held-out validation set and a separate final test set.

## Prepare training requests

For the HTTP API, use JSONL with one decisions request and its expected answers per line:

```json
{"state":"My card was charged twice.","questions":{"team":{"type":"choice","instructions":"Which team?","criteria":{"billing":"payments","tech":"bugs"}}},"answers":{"team":"billing"}}
```

Answers are booleans for `noul`, an option key for `choice`, a zero-based level index for `score`, and an array of keys for `multi`. The expected answers should come from your verified targets.

## Enable training on the server

```bash
uv run --no-sync selfjev serve --fine-tuning
```

This keeps the LoRA unmerged and enables uploads and jobs. Training shares the serving GPU and runs one job at a time. A 24 GB GPU alongside serving is untested and likely too small.

## Submit a job

```python
from selfjev import SelfJev

client = SelfJev(base_url="http://localhost:8000", api_key="your-key")
training = client.upload_file("train.jsonl")
job = client.create_fine_tuning_job(
    training.id,
    method="supervised",
    suffix="support",
)
print(job.id)

# Poll later; only use the new model after status is "succeeded".
job = client.fine_tuning_job(job.id)
print(job.status, job.fine_tuned_model)
```

A successful job registers its adapter under a new model name. Pass that name as `model` in subsequent decisions requests. Mount persistent storage for `~/.selfjev/server` if you need uploads and job state to survive a container replacement.

## Choosing an objective

Start with supervised training. In this project, RLCD did not reliably improve accuracy over fine-tuning on the same soft targets. An explicit cost for confident mistakes reduced those mistakes, with other probability-quality tradeoffs. Choose an objective based on what your application needs and evaluate it on held-out data.

The default model’s training included stored Jev probabilities as an additional teacher signal. [TypeSafe’s customer agreement, §2.3(b)](https://typesafe.ai/legal/mca) restricts using its outputs for model distillation, training an imitator, or developing a similar product. We have not established an exception that would permit publishing this adapter on Hugging Face.

For the full CLI training schema, reward settings, and recorded experiments, read [fine-tuning and RLCD](https://jwuthri.github.io/SelfJev/finetune/) and the [API job contract](https://github.com/Jwuthri/SelfJev/blob/master/docs/api.md#fine-tuning). HTTP training orchestration has not been exercised end to end in the recorded GPU runs.
