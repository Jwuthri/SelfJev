# Learning curves on Qwen3-Reranker-4B (test split, 3,471 questions)

Same recipe as `runs/lora_4b` (LoRA r=16 on q/k/v/o, lr 2e-4, bf16, prompt answer-v1); one A10G per run.

## Volume: nested subsets of the same 10,112-question mix

| run | train questions | epochs | question acc % | binary acc % | binary AUROC | multiclass acc % | multilabel EM % |
|---|---|---|---|---|---|---|---|
| vol25_e1 | 2,528 | 1 | 77.0 | 83.8 | 0.930 | 80.8 | 33.4 |
| vol50_e1 | 5,056 | 1 | 78.9 | 84.5 | 0.934 | 81.9 | 44.5 |
| lora_4b (reference) | 10,112 | 1 | 80.3 | 87.5 | 0.945 | 82.3 | 47.7 |
| vol25_e2 | 2,528 | 2 | 79.1 | 85.7 | 0.935 | 81.4 | 45.6 |
| vol50_e2 | 5,056 | 2 | 79.1 | 84.8 | 0.940 | 81.7 | 46.8 |
| vol100_e2 | 10,112 | 2 | 79.8 | 87.0 | 0.951 | 81.9 | 46.2 |

## Per-task: BoolQ training questions added to the mix (BoolQ test is otherwise never trained on)

| run | BoolQ train questions added | BoolQ test acc % | overall question acc % | binary acc % | binary AUROC | Jev on BoolQ |
|---|---|---|---|---|---|---|
| lora_4b (reference) | 0 | 83.3 | 80.3 | 87.5 | 0.945 | 90.7 |
| boolq_100 | 100 | 84.3 | 80.0 | 86.9 | 0.945 | 90.7 |
| boolq_300 | 300 | 83.3 | 80.9 | 88.0 | 0.940 | 90.7 |
| boolq_1000 | 1,000 | 84.3 | 80.9 | 88.8 | 0.954 | 90.7 |
| boolq_3000 | 3,000 | 86.7 | 80.9 | 88.9 | 0.954 | 90.7 |

## Base model: Qwen3-4B-Instruct-2507 vs Qwen3-Reranker-4B, same pair format and LoRA recipe

| run | train questions | epochs | question acc % | binary acc % | binary AUROC | multiclass acc % | multilabel EM % |
|---|---|---|---|---|---|---|---|
| Reranker-4B zero-shot | 0 | 0 | 62.8 | 55.0 | 0.604 | 76.2 | 2.0 |
| Instruct-4B zero-shot | 0 | 0 | 71.3 | 84.2 | 0.911 | 73.5 | 20.1 |
| Reranker-4B + LoRA | 10,112 | 1 | 80.3 | 87.5 | 0.945 | 82.3 | 47.7 |
| Instruct-4B + LoRA | 10,112 | 1 | 80.6 | 87.4 | 0.944 | 82.6 | 48.3 |

Instruct prompt selected on validation: `answer-v1` (answer-v1 0.802, task-v1 0.781, task-v2 0.788, hybrid-v1 0.783).

## Paired McNemar vs the reference (questions only one of the two gets right)

| run | run only | reference only | p |
|---|---|---|---|
| vol25_e1 | 84 | 200 | 4.5e-12 |
| vol50_e1 | 84 | 132 | 0.0013 |
| vol25_e2 | 99 | 143 | 0.0056 |
| vol50_e2 | 91 | 134 | 0.005 |
| vol100_e2 | 56 | 74 | 0.14 |
| boolq_100 | 65 | 75 | 0.45 |
| boolq_300 | 81 | 60 | 0.092 |
| boolq_1000 | 97 | 76 | 0.13 |
| boolq_3000 | 98 | 78 | 0.15 |
| instruct_lora | 144 | 136 | 0.68 |
