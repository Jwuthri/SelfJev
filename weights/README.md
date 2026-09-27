# Weights

The adapters worth keeping, tracked with Git LFS (`weights/**/*.safetensors`, see `.gitattributes`). Each folder is a
PEFT LoRA adapter plus a `model.json`: base model and pinned revision, recipe, prompt format, scores, sha256 and the
commands to serve it. Training runs write to `runs/`, which is not in git; the training logs of past runs are in
`reports/train_meta/`.

| folder | base | eval2 | dev benchmark | eval_llm | use it for |
|---|---|---|---|---|---|
| **[selfjev_4b](selfjev_4b/model.json)** (`selfjev-4b`, the default) | Qwen/Qwen3.5-4B @ 851bf6e | 95.8 | 83.8 | 93.1 | the best accuracy (eval2, LLM evaluation), fewer confident mistakes |

It was trained with every option listed in the question; `selfjev serve` adds the list by default. Earlier adapters
(`qwen35_4b_tree`, the previous default: eval2 95.6, dev benchmark 84.4; the Qwen3 tree models) are in git history and
at the tag `archive/pre-cleanup-2026-09-27`; their reports stay in `reports/`.

To keep a new run: copy its adapter folder here and write a `model.json` like `selfjev_4b`'s (the Git LFS rule picks up
the `.safetensors` file):

```bash
cp -r runs/mine/adapter weights/mine
```

Pull the files after cloning with `git lfs pull`.
