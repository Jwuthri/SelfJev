# selfjev-4b-vision quantized for an 8 GB GPU (SELA-003)

`selfjev eval|serve|bench --quantize 8bit|4bit` (bitsandbytes; adapter merged in bf16, then quantized while loading).
A10G with `torch.cuda.set_per_process_memory_fraction(7.2 GiB)` standing in for an RTX 4060 (8 GB, ~7.6 GiB usable),
`--max-batch-tokens 4096`. bf16 numbers are the vision release's own reports (`reports/images_v1/`, L40S, uncapped).

| Decision Bench suite | bf16 | 8-bit | 4-bit (NF4) |
|---|---|---|---|
| eval2 (1,991) | 96.1 | 95.2 (uncapped; OOM under the cap) | 94.7 |
| eval_llm (946) | 92.5 | 92.0 | 92.0 |
| compact challenge (720) | 100.0 (A10G, this run) | 100.0 | 100.0 |
| pooled, 3,657 questions | 95.9 | 95.3 | 95.0 |

| peak GPU memory, 1 question (MiB allocated) | bf16 (qsweep, A10G) | 8-bit | 4-bit |
|---|---|---|---|
| 2K-token text | 8,481 | 4,987 | 3,533 |
| 8K | n/a | 6,064 | 4,609 |
| 16K | n/a | out of memory at 7.2 GiB | 6,157 |

Latency, 2K text, 1 question, p50: 4-bit 604 ms, 8-bit 824 ms, bf16 584 ms (same A10G, `reports/bench/`). eval2 wall: 4-bit
767 s, 8-bit 925 s.

Raw reports: `4bit/`, `8bit/`, `bf16_compact_challenge_v1/`; `8bit/eval2_capped_oom.log` is the eval2 run that ran out of
memory under the 8 GB cap (a long text with 5.4 GB of int8 weights).

## Published checkpoints (2026-10-01)

`Jwuthrich/selfjev-4b-vision-4bit` (3.3 GB) and `-8bit` (4.8 GB), written by `selfjev quantize` and served with
`--quantized-model`. Reloaded from disk under the same 7.2 GiB cap: compact 100 / 100, 4-bit eval_llm 92.0
(`prequantized/`). The scores above are from the on-the-fly build, which loads the same merged weights with the same
bitsandbytes settings.
