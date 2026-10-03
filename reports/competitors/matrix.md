| model | size, base, licence | eval2 s (1 L40S) | eval2 | eval_llm | image test: held-out / trained-on datasets | typed-decisions | JevBench public-231 / hard-111 | Nimble 13 macro |
|---|---|---|---|---|---|---|---|---|
| decider-4b | 4.2B, Qwen3.5-4B-Base full FT, text, Apache-2.0 | 145 | 90.8 | 82.8 | — | 68.0 | 83.1 / 65.8 | — |
| imajev-4b | 4B, Qwen3.5-4B + LoRA r64, text + images, Apache-2.0 | 489 | 91.5 | 84.9 | 85.2 / 70.1 | 68.5 | 85.7 / 71.2 | — |
| jpt-4b | 4.5B, Qwen3.5-4B merged LoRA, text + images, CC-BY-NC-4.0 | 90 | 92.5 | 85.0 | 83.8 / 71.4 | 78.8 | 87.9 / 78.4 | — |
| kev-4b | 4B, Qwen3.5-4B-Base + LoRA r16 + head, text, Apache-2.0 | 109 | 88.4 | 74.7 | — | 67.0 | 75.8 / 54.1 | — |
| laya | 0.4B, ModernBERT-large encoder, text, Apache-2.0 | 23 | 45.4 | 46.4 | — | 36.0 | — | — |
| laya-long | same, max_len 8192 / head 2048 | 108 | 46.9 | 45.6 | — | 36.0 | — | — |
| mica-4b | 4.2B, Qwen3.5-4B merged LoRA (llama.cpp BF16), text, Apache-2.0 | 162 | 89.6 (98% answered) | 84.1 (99% answered) | — | 68.0 | 82.7 / 64.0 | — |
| openjev-27b-fp8 | 27B, Qwen3.8-27B FP8, text + images, CC-BY-NC-4.0 | 753 | 96.8 | 92.6 | 82.6 / 72.8 | 71.1 | 87.4 / 74.8 | — |
| plumb-4b | 4.2B, JevK5 (Qwen3.5-4B), text, Apache-2.0 | 471 | 93.4 | 84.1 | — | 61.4 | 89.6 / 80.2 | — |
| selfjev-4b-vision | 4B, Qwen3.5-4B + LoRA r64, text + images, Apache-2.0 code; Jev soft targets in training | 166 | 94.7 | 90.7 | 85.1 / 94.0 | 66.1 | 83.5 / 66.7 | 74.8 |

| model | set | ours only right | model only right | p |
|---|---|---|---|---|
| decider-4b | eval2 | 122 | 43 | 5.9e-10 |
| imajev-4b | eval2 | 99 | 35 | 2.9e-08 |
| jpt-4b | eval2 | 81 | 37 | 6.3e-05 |
| kev-4b | eval2 | 153 | 28 | 4.7e-22 |
| laya | eval2 | 1001 | 18 | 6.8e-269 |
| laya-long | eval2 | 969 | 17 | 6e-261 |
| mica-4b | eval2 | 140 | 38 | 6.3e-15 |
| openjev-27b-fp8 | eval2 | 30 | 72 | 3.9e-05 |
| plumb-4b | eval2 | 79 | 52 | 0.023 |
| decider-4b | eval_llm | 107 | 32 | 1.2e-10 |
| imajev-4b | eval_llm | 88 | 33 | 5.9e-07 |
| jpt-4b | eval_llm | 82 | 28 | 2.5e-07 |
| kev-4b | eval_llm | 168 | 17 | 2.1e-32 |
| laya | eval_llm | 441 | 22 | 2.1e-102 |
| laya-long | eval_llm | 449 | 22 | 1.2e-104 |
| mica-4b | eval_llm | 85 | 23 | 1.5e-09 |
| openjev-27b-fp8 | eval_llm | 33 | 51 | 0.063 |
| plumb-4b | eval_llm | 84 | 22 | 1e-09 |
| imajev-4b | eval_images_v1 | 346 | 53 | 8.2e-54 |
| jpt-4b | eval_images_v1 | 326 | 38 | 3.3e-58 |
| openjev-27b-fp8 | eval_images_v1 | 336 | 56 | 9e-50 |
