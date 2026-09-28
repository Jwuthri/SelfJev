## Health and observability

`GET /health` returns 200 after the model loads, with queue depth. `GET /metrics` exposes Prometheus metrics for requests, latency, questions, tokens, and queue depth. Both routes are open; restrict network access if these operational details should be private.

Every response includes `x-request-id`. Server errors include the id so you can match a client failure to the server logs.

## Batching and overload

The service batches concurrent requests into shared forward passes, with up to 32 requests and a 5 ms batching wait. When 256 requests are waiting, it returns HTTP 529 and `Retry-After`. The SDK retries transient failures with backoff.

These are queue defaults, not a throughput promise. Measure with your actual document lengths, question counts, candidate counts, and GPU before choosing production limits.

## Common failures

| Symptom | What to check |
|---|---|
| CUDA unavailable | GPU visibility, driver installation, container GPU access |
| Adapter fails to load | Run Git LFS pull; files must be weights, not LFS pointers |
| Slow first startup | Base model download and dependency installation |
| Out of memory | Reduce packed tokens, context length, questions, and candidates |
| HTTP 422 | Schema details and the state-plus-longest-question token limit |
| HTTP 529 | Queue saturation; backoff or add serving capacity |
| Runpod proxy 524 | Request exceeded the proxy timeout |
| HTTP 401 | Client key must match one of `SELFJEV_API_KEYS` |

## Safe public serving

Configure Bearer keys, HTTPS, and inbound network rules. Keep client keys on your application backend, not in a public website bundle. The marketing website does not call the model and does not need an API key.

## Reproducibility

Record the model, adapter hash, engine, dtype, GPU, request mix, warmup, and whether latency is measured inside the server or at the client. Use the [research reports](https://github.com/Jwuthri/SelfJev/tree/master/reports) as examples. Accuracy and latency from different engines or models should not be presented as one benchmark.
