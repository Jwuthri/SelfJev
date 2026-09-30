Send a state and named questions to `POST /v1/systemone`. The aliases `/api/alpha/decisions` and `/v1/decisions` accept the same request. The interface follows Jev; the underlying model and probabilities are different.

Images work with the default tree engine: send an image data URL or mixed text/image parts as `state`; the SDK also accepts `Path`, bytes, and PIL images. See the [image request reference](https://github.com/Jwuthri/SelfJev/blob/master/docs/api.md#request).

## Images with the Python SDK

Install the image-capable 0.3.0 release on your server with `pip install "selfjev[serve,gpu]==0.3.0"`; client-only machines need `pip install selfjev==0.3.0`. The model name `selfjev-4b` now selects the image-and-text vision release.

```python
from pathlib import Path
from selfjev import SelfJev, Choice

client = SelfJev(base_url="http://localhost:8000")  # Uses SELFJEV_API_KEY.
result = client.system_one(
    state=[Path("cat.jpg")],
    questions={"breed": Choice("What breed is it?", {
        "persian": "a Persian cat",
        "siamese": "a Siamese cat",
        "other": "another breed",
    })},
)
```

The native engine shares the image across questions. The vLLM backend supports text only. Image rows also work with `/v1/fine_tuning/jobs`; see [fine-tuning with images](/docs/finetuning/#prepare-image-training-rows).

## Authentication

**You create the key yourself.** For example, run `python -c 'import secrets; print(secrets.token_urlsafe(32))'` and keep the result private. Set that value as `SELFJEV_API_KEYS` on the server. Set the same value as `SELFJEV_API_KEY` in your client environment, or pass it as `api_key` in the Python SDK. The client sends it in the `Authorization: Bearer ...` header and the server checks for an exact match. `SELFJEV_API_KEYS` can contain several comma-separated keys; any one is accepted. If you do not configure server keys, requests require no authentication.

This is **your SelfJev server key**, separate from a Hugging Face token, AWS credentials, or a TypeSafe/Jev key. The AWS deployment helper generates a key automatically if you do not pass `--api-key`; it prints it and stores it in `~/.selfjev/deployments/<name>.json`.

## Make a request

```bash
curl http://localhost:8000/v1/systemone \
  -H "Authorization: Bearer $SELFJEV_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "selfjev-4b",
    "state": "My invoice was charged twice. Please refund me.",
    "questions": {
      "refund": {
        "type": "noul",
        "instructions": "Does the customer ask for a refund?"
      },
      "team": {
        "type": "choice",
        "instructions": "Which team should handle this?",
        "criteria": {"billing": "payments and refunds", "tech": "technical issues"}
      }
    }
  }'
```

`SELFJEV_API_KEY` is the client-side environment variable; set it to one of the server’s configured keys.

## Four answer types

| Type | Criteria | Answer |
|---|---|---|
| `noul` | Optional true/false descriptions | Probability of yes, from 0 to 1 |
| `choice` | Map of 2–255 named options | One key, a probability distribution, and confidence |
| `score` | Array of 2–10 ordered level descriptions | Expected level index, distribution, and confidence |
| `multi` | Map of 1–255 named options | All keys with probability ≥ 0.5; independent probabilities |

`multi` is a SelfJev extension. Its probabilities do not sum to one. For `choice`, add an explicit “none of the above” option if that outcome is valid.

## Response shape

Illustrative response; probabilities below are examples, not a recorded inference:

```json
{
  "id": "dec_example",
  "model": "selfjev-4b",
  "answers": {
    "refund": {"type": "noul", "noul": 0.97},
    "team": {
      "type": "choice",
      "choice": "billing",
      "probabilities": {"billing": 0.99, "tech": 0.01},
      "confidence": 0.98
    }
  },
  "usage": {"input_tokens": 296, "output_tokens": 0}
}
```

`output_tokens` is always zero: the engine scores answers rather than generating them. For a choice with K options, confidence is `(K × max_probability − 1) / (K − 1)`. It is not a separate guarantee of correctness.

## Limits and errors

Up to 64 questions per request. The default path limit is 32,768 tokens, but training used texts up to 16K; longer accepted contexts are not validated. Invalid or oversized inputs receive 422, never silent truncation.

| Status | Meaning | Action |
|---|---|---|
| 401 | Missing or unknown key | Check your Bearer key |
| 404 | Unknown model or resource | Check the model name or resource id |
| 413 | Uploaded file too large | Keep training uploads within 512 MB |
| 422 | Invalid schema or input | Read `error.param` and `error.message` |
| 529 | Queue full | Retry with backoff and `Retry-After` |
| 500 | Server error | Save the `x-request-id` for diagnosis |

The Python SDK retries 429, 529, and 5xx responses. `AsyncSelfJev` provides the same methods with `await`.

## Further reference

See the [complete API contract](https://github.com/Jwuthri/SelfJev/blob/master/docs/api.md) for score and multi examples, file uploads, fine-tuning endpoints, and the native `/classify` schema.
