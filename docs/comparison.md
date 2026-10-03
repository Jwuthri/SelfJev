<!-- selfjev:comparison:start -->
# Compared with open Jev-like models

*Measured 2026-09-30.* Eight open "Jev-like" decision models from Hugging Face and SelfJev were each served with
their card's recommended setup on the same GPU (one NVIDIA L40S) and asked exactly the requests TypeSafe's Jev receives.
A request a model cannot answer counts as wrong. Jev is shown for reference.

**SelfJev's test suites.** Text Decisions (1,991 questions) and AI Response Review (946), published as
[selfjev-decision-bench](https://huggingface.co/datasets/Jwuthrich/selfjev-decision-bench), and photos:

| model | size | images | licence | Text Decisions | AI Response Review | held-out images | Text Decisions time (s) |
|---|---|---|---|---|---|---|---|
| Jev 1.13 (TypeSafe API, reference) | ? | no | paid API | 97.2 | 92.5 | — | — |
| [openjev](https://huggingface.co/openjev/openjev) | 27B | yes | CC-BY-NC-4.0 | 96.8 | 92.6 | 82.6 | 753 |
| [**SelfJev-4B Vision**](https://huggingface.co/Jwuthrich/selfjev-4b-vision) | 4B | yes | Apache-2.0 code | 94.7 | 90.7 | 85.1 | 166 |
| [Plumb-4B](https://huggingface.co/crh225/plumb-4b) | 4.2B | no | Apache-2.0 | 93.4 | 84.1 | — | 471 |
| [jpt-4b](https://huggingface.co/kirp/jpt-4b) | 4.5B | yes | CC-BY-NC-4.0 | 92.5 | 85.0 | 83.8 | 90 |
| [imajev-4b](https://huggingface.co/mohit67890/imajev-4b) | 4B | yes | Apache-2.0 | 91.5 | 84.9 | 85.2 | 489 |
| [decider-4b](https://huggingface.co/Mapika/decider-4b) | 4.2B | no | Apache-2.0 | 90.8 | 82.8 | — | 145 |
| [Mica-v0.1-4B](https://huggingface.co/sky7350/Mica-v0.1-4B) | 4.2B | no | Apache-2.0 | 89.6 ² | 84.1 ² | — | 162 |
| [kev-4b](https://huggingface.co/jaredpalmer/kev-4b) | 4B | no | Apache-2.0 | 88.4 | 74.7 | — | 109 |
| [Laya](https://huggingface.co/convaiinnovations/laya) | 0.4B | no | Apache-2.0 | 45.4 | 46.4 | — | 23 |

- Every model gets the same Jev-shaped questions; select-all questions become one yes/no per option, which costs SelfJev
  1.4–1.8 points against its native evaluation (96.1 and 92.5). **Held-out images**: the 4 image datasets of the SelfJev
  image test that none of these models trained on (772 questions). **Time**: Text Decisions end to end, 4 requests in
  flight. ² Refuses inputs over 8,192 tokens (2 % and 1 % of the questions), counted wrong.
- No other model trained on these suites, but they come from the same authors and judges as SelfJev's training data,
  so they favour SelfJev.
- SelfJev is the most accurate open model at 4.5B parameters or less on both suites (paired tests, p ≤ 0.023) and ties
  imajev-4b on held-out images; the 27B openjev is higher on Text Decisions. It is slower than most 4B models here.

Protocol, per-model setups, paired tests and raw reports: [reports/competitors](https://github.com/Jwuthri/SelfJev/blob/master/reports/competitors/README.md).
<!-- selfjev:comparison:end -->
