# Weights

The adapters worth keeping, tracked with Git LFS (`weights/**/*.safetensors`, see `.gitattributes`). Each folder is a
PEFT LoRA adapter plus a `model.json`: base model and pinned revision, recipe, prompt format, scores, sha256 and the
commands to serve it. Every other trained adapter stays in `runs/`, which is not in git.

| folder | base | eval2 | dev benchmark | eval_llm | use it for |
|---|---|---|---|---|---|
| **[selfjev_4b](selfjev_4b/model.json)** (`selfjev-4b`, the default) | Qwen/Qwen3.5-4B @ 851bf6e | **95.8** | 83.8 | **93.1** | the best accuracy (eval2, LLM evaluation), fewer confident mistakes |
| [qwen35_4b_tree](qwen35_4b_tree/model.json) (the previous default) | Qwen/Qwen3.5-4B @ 851bf6e | 95.6 | **84.4** | 82.1 | the public-dataset dev benchmark |
| [tree_4b_combo](tree_4b_combo/model.json) | Qwen/Qwen3-4B-Instruct-2507 @ cdbee75 | 94.5 | 82.7 | — | the fastest and cheapest serving (vLLM) |

All three were trained with every option listed in the question: serve them with `--options-in-question`.

To keep a new run: copy its adapter folder here and write a `model.json` like the ones above (the Git LFS rule picks up
the `.safetensors` file):

```bash
cp -r runs/mine_rlcd/adapter weights/mine_rlcd
```

Pull the files after cloning with `git lfs pull`.
