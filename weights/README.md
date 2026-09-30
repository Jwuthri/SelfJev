# Weights

Download the current adapter and model card from [Jwuthrich/selfjev-4b-vision](https://huggingface.co/Jwuthrich/selfjev-4b-vision)
(text and images, the default since 2026-09-30). The text-only release stays at
[Jwuthrich/selfjev-4b](https://huggingface.co/Jwuthrich/selfjev-4b).

The **full merged checkpoint** (9.32 GB of weights, plus tokenizer and configuration) is available at
[Jwuthrich/selfjev-4b-merged](https://huggingface.co/Jwuthrich/selfjev-4b-merged). It includes the base weights (text-only release) and needs
no separate adapter download. Use the SelfJev vLLM backend; see the model card for setup. The default TreeServer
continues to use the adapter release.

The adapters worth keeping, tracked with Git LFS (`weights/**/*.safetensors`, see `.gitattributes`). Each folder is a
PEFT LoRA adapter plus a `model.json`: base model and pinned revision, recipe, prompt format, scores, sha256 and the
commands to serve it. Training runs write to `runs/`, which is not in git; the training logs of past runs are in
`reports/train_meta/`.

| folder | base | eval2 | dev benchmark | eval_llm | use it for |
|---|---|---|---|---|---|
| **[selfjev_4b_vision](selfjev_4b_vision/model.json)** (`selfjev-4b`, the default since 2026-09-30) | Qwen/Qwen3.5-4B @ 851bf6e | 96.1 | 84.1 | 92.5 | text and images: `selfjev_4b` + one epoch on 11.3K image questions (6 datasets) and 11.3K replayed text questions; image test 90.4 (`reports/images_v1/`) |
| [selfjev_4b](selfjev_4b/model.json) (text-only release, default until 2026-09-30) | Qwen/Qwen3.5-4B @ 851bf6e | 95.8 | 83.8 | 93.1 | text only; its `assets/` hold the figures the README, website and model card use |

Both were trained with every option listed in the question; `selfjev serve` adds the list by default. Earlier adapters
(`qwen35_4b_tree`, the previous default: eval2 95.6, dev benchmark 84.4; the Qwen3 tree models) are in git history and
at the tag `archive/pre-cleanup-2026-09-27`; their reports stay in `reports/`.

To keep a new run: copy its adapter folder here and write a `model.json` like `selfjev_4b`'s (the Git LFS rule picks up
the `.safetensors` file):

```bash
cp -r runs/mine/adapter weights/mine
```

Pull the files after cloning with `git lfs pull`.
