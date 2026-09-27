#!/usr/bin/env bash
# The selfjev-4b recipe, run ON a GPU box with 48 GB (an L40S: g6e.2xlarge) from ~/SelfJev:
#   nohup bash scripts/train/selfjev_4b.sh RUN > train.log 2>&1 < /dev/null &
# Needs runs/jev_all/{train,val}.jsonl.gz from scripts/train/jev_soft_targets.py (every non-test question of
# data/all.jsonl.gz, target 0.5 x label + 0.5 x Jev's probabilities). Steps:
#   1. preflight: weights/selfjev_4b on 400 eval2 questions must agree with its stored report (>= 97% of decisions)
#   2. selfjev finetune: a new LoRA r64 on Qwen3.5-4B, lr 2e-4, 1 epoch, texts up to 16K tokens -> runs/RUN
#   3. eval2, the dev benchmark (hf + eval test rows) and eval_llm for the best and the last checkpoint -> reports/RUN[_last]/
# Box: scripts/aws/aws_launch.sh; sync src scripts pyproject.toml uv.lock README.md weights/selfjev_4b data/ova runs/jev_all
# and the preflight's baseline report. ≈ 10 h on an L40S for 84K questions.
set -uo pipefail
RUN=${1:?run name}
BASELINE=reports/qwen35_4b_tree_scratch_jevall_/eval2/report.json  # selfjev-4b's eval2 report
cd ~/SelfJev && mkdir -p runs reports
export PATH="$HOME/.local/bin:$PATH" PYTHONUNBUFFERED=1 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
log() { echo "[$(date +%H:%M:%S)] $RUN: $*"; }
command -v uv > /dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
uv sync --quiet --extra gpu && log "env ready"
PY=.venv/bin/python
$PY -c "import fla" || { log "FAILED: flash-linear-attention missing"; exit 1; }
$PY -c "from huggingface_hub import snapshot_download; snapshot_download('Qwen/Qwen3.5-4B', revision='851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a')" > /dev/null && log "model downloaded"

log "preflight"
$PY -m selfjev.cli eval --adapter weights/selfjev_4b --data data/ova/eval2.jsonl --limit 400 --out runs/preflight > runs/preflight.log 2>&1 \
  || { log "PREFLIGHT FAILED"; tail -30 runs/preflight.log; exit 1; }
$PY - runs/preflight/report.json $BASELINE <<'EOF' || { log "PREFLIGHT MISMATCH: not training"; exit 1; }
import json, sys
new, old = (json.load(open(p))["predictions"] for p in sys.argv[1:3])
old = {p["id"]: p for p in old}
agree = sum(p["selected"] == old[p["id"]]["selected"] for p in new) / len(new)
dp = sorted(max(abs(a - b) for a, b in zip(p["probabilities"], old[p["id"]]["probabilities"], strict=True)) for p in new)
print(f"preflight: {len(new)} eval2 questions, decisions agree {agree:.1%}, max |dp| median {dp[len(dp) // 2]:.4f}, p99 {dp[int(len(dp) * 0.99)]:.4f}")
sys.exit(agree < 0.97)
EOF

log "train"
$PY -m selfjev.cli finetune --data runs/jev_all/train.jsonl.gz --val runs/jev_all/val.jsonl.gz --lr 2e-4 --soft-weight 0.5 \
  --max-length 16384 --batch-tokens 16384 --grad-accum 2 --out runs/$RUN > runs/$RUN.log 2>&1 || { log "TRAIN FAILED"; tail -30 runs/$RUN.log; exit 1; }

for ad in adapter adapter_last; do
  [[ $ad == adapter_last ]] && cmp -s runs/$RUN/adapter/adapter_model.safetensors runs/$RUN/adapter_last/adapter_model.safetensors && continue
  R=reports/$RUN${ad#adapter}
  for set in "eval2 --data data/ova/eval2.jsonl" "test --data data/ova/hf.jsonl data/ova/eval.jsonl --split test" "eval_llm --data data/ova/eval_llm.jsonl"; do
    read -r name args <<< "$set"
    # shellcheck disable=SC2086
    $PY -m selfjev.cli eval --adapter runs/$RUN/$ad --out $R/$name $args > /dev/null 2>> runs/$RUN.eval.log && log "EVAL $R/$name done" || log "EVAL $R/$name FAILED"
  done
done
log "ALL DONE"
