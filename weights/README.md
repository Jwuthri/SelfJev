# Weights

The adapters worth keeping, tracked with Git LFS (`weights/**/*.safetensors`, see `.gitattributes`). Each folder is a
PEFT LoRA adapter plus a `model.json`: base model and pinned revision, recipe, prompt format, scores, sha256 and the
commands to serve it. Every other trained adapter stays in `runs/`, which is not in git.

| folder | base | eval2 | dev benchmark | use it for |
|---|---|---|---|---|
| [qwen35_4b_tree](qwen35_4b_tree/model.json) | Qwen/Qwen3.5-4B @ 851bf6e | **95.6** | **84.4** | the best accuracy |
| [tree_4b_combo](tree_4b_combo/model.json) | Qwen/Qwen3-4B-Instruct-2507 @ cdbee75 | 94.5 | 82.7 | the fastest and cheapest serving (vLLM) |

Both were trained with every option listed in the question: serve them with `--options-in-question`.

To keep a new run: copy its adapter folder here and write a `model.json` like the two above (the Git LFS rule picks up
the `.safetensors` file):

```bash
cp -r runs/mine_rlcd/adapter weights/mine_rlcd
```

Pull the files after cloning with `git lfs pull`.
