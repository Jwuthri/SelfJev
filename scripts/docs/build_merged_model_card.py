"""Reuse the adapter card's visuals for an existing merged HF release.

First build the adapter card with build_model_card.py. Download SHA256SUMS from
the merged release, then run this script with --checksums PATH. No model loading
or network writes. Upload only the resulting README/assets/reproduce/SHA256SUMS.
"""

import argparse
import hashlib
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ADAPTER = ROOT / "weights/selfjev_4b"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checksums", required=True, type=Path)
    parser.add_argument("--out", type=Path, default=ROOT / "runs/hf-merged-card")
    args = parser.parse_args()
    card = (ADAPTER / "README.md").read_text()

    def replace(old, new):
        nonlocal card
        assert card.count(old) == 1, f"Adapter card changed; review replacement: {old[:70]}"
        card = card.replace(old, new, 1)

    replace("base_model_relation: adapter", "base_model_relation: finetune")
    replace("library_name: peft", "library_name: transformers")
    replace("  - lora\n", "  - merged\n")
    replace("# SelfJev-4B\n", "# SelfJev-4B — merged weights\n")
    replace(
        "This repository contains the **230 MB LoRA adapter**, not the entire model. The Qwen3.5-4B base weights download separately. "
        "The 4B model size refers to the backbone; the adapter stores the learned update.",
        "This repository contains the **complete merged checkpoint (approximately 9.3 GB of weights)**, tokenizer and configuration. "
        "The SelfJev LoRA is already incorporated into the pinned Qwen3.5-4B weights: no separate base or adapter download is needed. "
        "The original checkpoint layout, including unmodified vision weights, is retained; SelfJev is trained and evaluated for text.\n\n"
        "[Compact adapter release](https://huggingface.co/Jwuthrich/selfjev-4b) · "
        "[Merge provenance](merge_meta.json) · [Integrity checks](verification.json)",
    )
    replace(
        "## Results\n",
        "## Results\n\n"
        "**Reference results for the source adapter through TreeServer.** The same charts and evaluation evidence are shared "
        "with the adapter release. This merged artifact passed tensor-integrity checks and two synthetic GPU smoke cases; "
        "it has not been benchmarked separately through vLLM.\n",
    )
    start = card.index("On Linux with an NVIDIA GPU, Git and uv installed:")
    end = card.index("In another terminal, use the same secret:", start)
    card = (
        card[:start]
        + """Use a Linux NVIDIA GPU machine with a compatible vLLM Python environment, Git and pip.
Install SelfJev into that environment and download the merged checkpoint:

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/Jwuthri/SelfJev.git
cd SelfJev
# Run inside your vLLM environment; it must support Qwen3.5.
python -m pip install -e '.[serve]'
python - <<'PYTHON'
from huggingface_hub import snapshot_download
snapshot_download(
    "Jwuthrich/selfjev-4b-merged",
    local_dir="weights/selfjev_4b_merged",
    ignore_patterns=["assets/*", "reproduce/*"],
)
PYTHON

export SELFJEV_API_KEYS="replace-with-your-long-random-secret"
selfjev serve --engine vllm \\
  --model-dir weights/selfjev_4b_merged --host 127.0.0.1 --port 8000
```

This uses SelfJev's vLLM backend. The default TreeServer quickstart uses the
[separate adapter release](https://huggingface.co/Jwuthrich/selfjev-4b#quickstart).
A generic chat endpoint does not implement SelfJev's decision scoring.

"""
        + card[end:]
    )
    replace(
        "| Default serving | TreeServer, shared document and question computation |\n"
        "| Alternative serving | vLLM with a merged checkpoint and prefix caching |",
        "| Serving this merged checkpoint | SelfJev's vLLM backend with prefix caching |\n"
        "| Engine behind the reference scores | TreeServer, using the source adapter |",
    )
    replace(
        "The adapter download size does not describe inference memory: the full backbone and runtime state must fit too.",
        "The full backbone and runtime state must fit in memory; checkpoint file size alone does not determine runtime requirements.",
    )
    replace(
        "| `adapter_model.safetensors` | Trained LoRA weights |\n| `adapter_config.json` | PEFT configuration |",
        "| `model.safetensors-*.safetensors` | Two complete merged weight shards |\n"
        "| `model.safetensors.index.json` | Tensor-to-shard index |\n"
        "| `config.json`, tokenizer files | Architecture and tokenization configuration |\n"
        "| `merge_meta.json`, `verification.json` | Merge provenance, tensor checks and GPU smoke results |\n"
        "| `SHA256SUMS` | Artifact and model-card file hashes |",
    )
    replace("Adapter SHA-256:", "Source adapter SHA-256:")
    replace(
        "The adapter uses the Qwen base model linked above. No separate adapter license is declared in this repository. "
        "Independent project; not affiliated with TypeSafe or Qwen.",
        "The base model's [license](LICENSE) is retained. No separate license for the SelfJev fine-tuning contribution has been declared. "
        "Independent project; not affiliated with TypeSafe or Qwen.",
    )
    replace(
        "This builds figures from reports and the canonical `data/all.jsonl.gz`; it performs no model inference.",
        "This builds the shared figures and adapter card from reports and the canonical `data/all.jsonl.gz`; "
        "it performs no model inference. "
        "The [merged-card converter](reproduce/build_merged_model_card.py) reuses those files, updates serving details and refreshes "
        "the existing checksum manifest. Run it from `scripts/docs/` with `--checksums` pointing to this release's "
        "downloaded `SHA256SUMS`.",
    )

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "README.md").write_text(card)
    for folder in ("assets", "reproduce"):
        shutil.copytree(ADAPTER / folder, args.out / folder, dirs_exist_ok=True)
    shutil.copyfile(Path(__file__), args.out / "reproduce/build_merged_model_card.py")
    checksums = {}
    for line in args.checksums.read_text().splitlines():
        digest, name = line.split("  ", 1)
        assert len(digest) == 64 and name not in checksums
        checksums[name] = digest
    for path in sorted(args.out.rglob("*")):
        if path.is_file() and path.name != "SHA256SUMS":
            checksums[str(path.relative_to(args.out))] = hashlib.sha256(path.read_bytes()).hexdigest()
    (args.out / "SHA256SUMS").write_text("".join(f"{digest}  {name}\n" for name, digest in sorted(checksums.items())))
    print(f"Prepared {args.out}: shared figures, merged quickstart, artifact details, refreshed SHA256SUMS.")


if __name__ == "__main__":
    main()
