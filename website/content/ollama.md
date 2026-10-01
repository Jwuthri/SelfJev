Run SelfJev through [Ollama](https://ollama.com) on a Mac, a laptop or a CPU box. No CUDA and no torch: SelfJev's API server sits in front of Ollama and speaks the same decisions API as the GPU server.

## Install

```bash
ollama pull hf.co/Jwuthrich/selfjev-4b-vision-GGUF:Q8_0
```

```bash
pip install "selfjev[ollama] @ git+https://github.com/Jwuthri/SelfJev"
selfjev serve --engine ollama --ollama-model hf.co/Jwuthrich/selfjev-4b-vision-GGUF:Q8_0
```

The `ollama` extra is not in the 0.3.0 release on PyPI yet, which is why the install comes from the repository. `Q8_0` is 4.6 GB; `Q4_K_M` is 2.8 GB. Ollama picks up the vision projector from the same repository, so both accept images. Then use the [API](/docs/api/) and the [client](/docs/) as with any SelfJev server.

## What it scores

Measured through Ollama on an NVIDIA L40S, on the same questions as the reference GPU engine:

| | Text decisions | AI response review | Images | Size |
|---|---|---|---|---|
| GPU engine, bf16 (reference) | 96.1 | 92.5 | 90.4 | 9 GB |
| Ollama Q8_0 | 95.7 | 92.7 | 89.4 | 4.6 GB |
| Ollama Q4_K_M | 95.7 | 91.9 | not run | 2.8 GB |

Q8_0 matches bf16 within noise. Q4_K_M loses 0.8 points on AI response review. The Ollama path is 0.4 to 1.0 points below the GPU engine at every precision; the cause is not isolated.

## Limits

- Slower than the GPU engine when one text carries many questions: Ollama has no shared-prefix pass, so the server sends one request per option. Good for a few questions on a laptop; use the [GPU server](/docs/) for many.
- Ollama's tokenizer merges one space differently from training, and it resizes images itself.
- Speed against the GPU engine has not been benchmarked.

Details, reports and the conversion recipe: [docs/ollama.md](https://github.com/Jwuthri/SelfJev/blob/master/docs/ollama.md).
