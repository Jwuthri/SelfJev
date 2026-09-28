SelfJev turns a state (your text) and a set of questions into typed answers with probabilities. You run the model on your own GPU; your application calls it over HTTP.

## Get the model

The releases are public on Hugging Face:

- [SelfJev-4B adapter](https://huggingface.co/Jwuthrich/selfjev-4b): the trained LoRA adapter for the native tree engine. `selfjev serve` downloads it on first start.
- [SelfJev-4B full merged model](https://huggingface.co/Jwuthrich/selfjev-4b-merged): the complete weights, tokenizer and configuration. Its model card includes download and vLLM serving instructions.
- [SelfJev Decision Bench](https://huggingface.co/datasets/Jwuthrich/selfjev-decision-bench): the evaluation questions, expected answers and scoring tools.

## 1. Start a GPU server

Use a Linux machine with an NVIDIA GPU. Start with **24 GB VRAM, 4 vCPUs, 16–32 GB system RAM, and 50 GB free disk**. These are planning recommendations, not a tested minimum. See [hardware and sizing](/docs/hardware/) for the evidence and limits.

Use Python 3.12+ and verify that `nvidia-smi` sees your GPU. Then:

```bash
pip install "selfjev[serve,gpu]"
export SELFJEV_API_KEYS="replace-with-a-long-random-key"
selfjev serve --host 0.0.0.0 --port 8000
```

You choose this key; no external provider issues it. Generate a long random value, for example with `python -c 'import secrets; print(secrets.token_urlsafe(32))'`, and keep it private. Copy the **same value** into the client’s `api_key` below. The server checks that the two match. If you leave `SELFJEV_API_KEYS` unset, the server accepts requests without a key, which is suitable only on a trusted local network.

The adapter (230 MB) and the pinned base model (about 9 GB) download on first start. Keep the terminal running. Model loading can take several minutes. Check readiness in another terminal:

```bash
curl --fail http://localhost:8000/health
```

Prefer a private network or SSH tunnel during setup. Configure HTTPS before sending credentials or private text over a public network. [Docker](/docs/docker/), [AWS](/docs/aws/), [Runpod](/docs/runpod/), and [Google Cloud](/docs/gcp/) have separate deployment guides.

## 2. Install the lightweight client

On the machine running your application, no GPU or model download is needed:

```bash
pip install selfjev
```

Already using TypeSafe's Python SDK? Keep it: set `TYPESAFE_BASE_URL` to your server and `TYPESAFE_API_KEY` to the same key, and your existing code runs against SelfJev unchanged.

## 3. Ask your first questions

With the server on the same machine, or an SSH tunnel forwarding local port 8000:

```python
from selfjev import SelfJev, Noul, Choice

client = SelfJev(
    base_url="http://localhost:8000",
    api_key="replace-with-the-same-key-set-on-your-server",
)
result = client.system_one(
    state="My invoice was charged twice. Please refund the second charge.",
    questions={
        "refund": Noul("Does the customer ask for a refund?"),
        "team": Choice("Which team should handle this?", {
            "billing": "payments and refunds",
            "tech": "outages and bugs",
        }),
    },
)
print(result.nouls["refund"].noul)
print(result.choices["team"].choice)
```

`noul` is a probability, and `choice` is one of your option keys. Results depend on the model; the examples on the home page are illustrations, not live inference.

## What to read next

The [API reference](/docs/api/) covers all four answer types. [How the model works](/docs/architecture/) explains shared context and isolated branches. For the evaluation history, use the [research explorer](/research/) or the [full lab notebook](https://jwuthri.github.io/SelfJev/).
