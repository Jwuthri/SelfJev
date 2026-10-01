| model | size | images | licence | Text Decisions | AI Response Review | held-out images | Text Decisions time (s) |
|---|---|---|---|---|---|---|---|
| Jev 1.13 (TypeSafe API, reference) | ? | no | paid API | 97.2 | 92.5 | — | — |
| [openjev](https://huggingface.co/openjev/openjev) | 27B | yes | CC-BY-NC-4.0 | 96.8 | 92.6 | 82.6 | 753 |
| [**SelfJev-4B Vision**](https://huggingface.co/Jwuthrich/selfjev-4b-vision) | 4B | yes | Apache-2.0 code | 94.7 | 90.7 | 85.1 | 242 |
| [Plumb-4B](https://huggingface.co/crh225/plumb-4b) | 4.2B | no | Apache-2.0 | 93.4 | 84.1 | — | 471 |
| [jpt-4b](https://huggingface.co/kirp/jpt-4b) | 4.5B | yes | CC-BY-NC-4.0 | 92.5 | 85.0 | 83.8 | 90 |
| [imajev-4b](https://huggingface.co/mohit67890/imajev-4b) | 4B | yes | Apache-2.0 | 91.5 | 84.9 | 85.2 | 489 |
| [decider-4b](https://huggingface.co/Mapika/decider-4b) | 4.2B | no | Apache-2.0 | 90.8 | 82.8 | — | 145 |
| [Mica-v0.1-4B](https://huggingface.co/sky7350/Mica-v0.1-4B) | 4.2B | no | Apache-2.0 | 89.6 ² | 84.1 ² | — | 162 |
| [kev-4b](https://huggingface.co/jaredpalmer/kev-4b) | 4B | no | Apache-2.0 | 88.4 | 74.7 | — | 109 |
| [Laya](https://huggingface.co/convaiinnovations/laya) | 0.4B | no | Apache-2.0 | 45.4 | 46.4 | — | 23 |

| model | size | JevBench public / hard | typed-decisions | trained or tuned on these public items? (its card) |
|---|---|---|---|---|
| Jev 1.13 (TypeSafe API, reference) | ? | 86.6 / 73.0 | 72.7 | not disclosed |
| [openjev](https://huggingface.co/openjev/openjev) | 27B | 87.4 / 74.8 | 71.1 | not stated |
| [**SelfJev-4B Vision**](https://huggingface.co/Jwuthrich/selfjev-4b-vision) | 4B | 83.5 / 66.7 | 66.1 | none (0 overlap with both, checked) |
| [Plumb-4B](https://huggingface.co/crh225/plumb-4b) | 4.2B | 89.6 / 80.2 | 61.4 | **JevBench: its public scores shaped the recipe** |
| [jpt-4b](https://huggingface.co/kirp/jpt-4b) | 4.5B | 87.9 / 78.4 | 78.8 ¹ | **typed-decisions: trained on its train split** |
| [imajev-4b](https://huggingface.co/mohit67890/imajev-4b) | 4B | 85.7 / 71.2 | 68.5 | states JevBench was decontaminated |
| [decider-4b](https://huggingface.co/Mapika/decider-4b) | 4.2B | 83.1 / 65.8 | 68.0 | not stated |
| [Mica-v0.1-4B](https://huggingface.co/sky7350/Mica-v0.1-4B) | 4.2B | 82.7 / 64.0 | 68.0 | **JevBench: half the hard items used to pick the recipe** |
| [kev-4b](https://huggingface.co/jaredpalmer/kev-4b) | 4B | 75.8 / 54.1 | 67.0 | JevBench reported only |
| [Laya](https://huggingface.co/convaiinnovations/laya) | 0.4B | — | 36.0 | not stated |
