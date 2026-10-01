<!-- selfjev:comparison:start -->
## Compared with open Jev-like models

Measured with [SelfJev-4B Vision](https://huggingface.co/Jwuthrich/selfjev-4b-vision), the default release, which continues this adapter; on text the two score within half a point of each other (Text Decisions 96.1 vs 95.7).

*Measured 2026-09-30.* Eight open "Jev-like" decision models from Hugging Face and SelfJev were each served with
their card's recommended setup on the same GPU (one NVIDIA L40S) and asked exactly the requests TypeSafe's Jev receives.
A request a model cannot answer counts as wrong. Jev is shown for reference.

| model | size | images | licence | Text Decisions | AI Response Review | held-out images | typed-decisions | JevBench public / hard | Text Decisions time (s) |
|---|---|---|---|---|---|---|---|---|---|
| Jev 1.13 (TypeSafe API, reference) | ? | no | paid API | 97.2 | 92.5 | — | 72.7 | 86.6 / 73.0 | — |
| [openjev](https://huggingface.co/openjev/openjev) | 27B | yes | CC-BY-NC-4.0 | 96.8 | 92.6 | 82.6 | 71.1 | 87.4 / 74.8 | 753 |
| [**SelfJev-4B Vision**](https://huggingface.co/Jwuthrich/selfjev-4b-vision) | 4B | yes | Apache-2.0 code | 94.7 | 90.7 | 85.1 | 66.1 | 83.5 / 66.7 | 242 |
| [Plumb-4B](https://huggingface.co/crh225/plumb-4b) | 4.2B | no | Apache-2.0 | 93.4 | 84.1 | — | 61.4 | 89.6 / 80.2 | 471 |
| [jpt-4b](https://huggingface.co/kirp/jpt-4b) | 4.5B | yes | CC-BY-NC-4.0 | 92.5 | 85.0 | 83.8 | 78.8 ¹ | 87.9 / 78.4 | 90 |
| [imajev-4b](https://huggingface.co/mohit67890/imajev-4b) | 4B | yes | Apache-2.0 | 91.5 | 84.9 | 85.2 | 68.5 | 85.7 / 71.2 | 489 |
| [decider-4b](https://huggingface.co/Mapika/decider-4b) | 4.2B | no | Apache-2.0 | 90.8 | 82.8 | — | 68.0 | 83.1 / 65.8 | 145 |
| [Mica-v0.1-4B](https://huggingface.co/sky7350/Mica-v0.1-4B) | 4.2B | no | Apache-2.0 | 89.6 ² | 84.1 ² | — | 68.0 | 82.7 / 64.0 | 162 |
| [kev-4b](https://huggingface.co/jaredpalmer/kev-4b) | 4B | no | Apache-2.0 | 88.4 | 74.7 | — | 67.0 | 75.8 / 54.1 | 109 |
| [Laya](https://huggingface.co/convaiinnovations/laya) | 0.4B | no | Apache-2.0 | 45.4 | 46.4 | — | 36.0 | — | 23 |

- **Text Decisions** (1,991 questions) and **AI Response Review** (946) are SelfJev's frozen test suites, published as
  [selfjev-decision-bench](https://huggingface.co/datasets/Jwuthrich/selfjev-decision-bench). Every model gets the same
  Jev-shaped questions; select-all questions become one yes/no per option, which costs SelfJev 1.4–1.8 points against
  its native evaluation (96.1 and 92.5). **Held-out images**: the 4 image datasets of the SelfJev image test that none
  of these models trained on (772 questions). **typed-decisions**: [LocalLLaMA/typed-decisions](https://huggingface.co/datasets/LocalLLaMA/typed-decisions)
  test, 2,000 decisions. **JevBench**: the 231 public items of [JevBench](https://github.com/fstandhartinger/jevbench)
  through its official runner; hard = its 111-item tier. **Time**: Text Decisions end to end, 4 requests in flight.
- ¹ Trained on the typed-decisions train split (its card), so not zero-shot. ² Refuses inputs over 8,192 tokens (2 % of
  Text Decisions, 1 % of AI Response Review), counted wrong. Jev's row: our earlier API runs and the public leaderboards.
- Where we re-measured a card's own number, it matched (JevBench: decider-4b, kev-4b, Mica, Plumb-4B, jpt-4b).
- **Reading.** SelfJev is the most accurate open model at 4.5B parameters or less on both of its suites (paired tests,
  p ≤ 0.023) and ties imajev-4b on held-out images; the 27B openjev beats it on Text Decisions. On the public JevBench
  items and typed-decisions it is mid-pack: it never saw them (0 overlap with its training data), while several of
  these models report tuning on them. It is slower than most 4B models on this workload.

Protocol, per-model setups, paired tests and raw reports: [reports/competitors](https://github.com/Jwuthri/SelfJev/blob/master/reports/competitors/README.md).
<!-- selfjev:comparison:end -->
