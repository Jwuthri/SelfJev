#!/usr/bin/env bash
# Runs ON the GPU box, from ~/SelfJev: `bash scripts/jev_soft_box.sh rlcd|sft|cost|scratch`, on runs/jev_all
# (scripts/jev_soft_targets.py: every non-test training question of data/all.jsonl.gz,
# target 0.5 x label + 0.5 x Jev, options listed in the question). rlcd / sft: RLCD or a plain fine-tune from
# weights/qwen35_4b_tree, lr 2e-5 (RLCD KL 0.2); cost: RLCD with a 5x cost per confident mistake from sft's result;
# scratch: a new LoRA r64 on the base model, lr 2e-4 (qwen35_4b_tree's recipe), plus eval_llm for the baselines
# qwen35_4b_tree and sft. Then eval2, dev benchmark and eval_llm for the best and the last adapter.
# Reports: reports/qwen35_4b_tree_<mode>_jevall_[_last]/. Launch: nohup bash scripts/jev_soft_box.sh rlcd > jev.log 2>&1 < /dev/null &
set -uo pipefail
MODE=$1; RUN=qwen35_4b_tree_${MODE}_jevall
cd ~/SelfJev && mkdir -p runs reports
export PATH="$HOME/.local/bin:$PATH" PYTHONUNBUFFERED=1 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
log() { echo "[$(date +%H:%M:%S)] jev-$MODE: $*"; }
command -v uv > /dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
uv sync --quiet && uv pip install --quiet --python .venv/bin/python flash-linear-attention einops && log "env ready"
PY=.venv/bin/python
$PY -c "import fla" || { log "FAILED: flash-linear-attention missing"; exit 1; }
$PY -c "from huggingface_hub import snapshot_download; snapshot_download('Qwen/Qwen3.5-4B', revision='851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a')" > /dev/null && log "model downloaded"
INIT="--init weights/qwen35_4b_tree"; LR=2e-5; SETS=eval2,test,eval_llm; EXTRA=""
case $MODE in
  rlcd) CMD="rlcd --beta 0.2" ;;
  sft) CMD=finetune ;;
  cost) CMD="rlcd --beta 0.2 --reward log=1,brier=1,spherical=1,confident_miss=5"; INIT="--init runs/qwen35_4b_tree_sft_jevall/adapter_last" ;;
  scratch) CMD=finetune; INIT=""; LR=2e-4; EXTRA="--max-length 16384 --batch-tokens 16384 --grad-accum 2" ;;  # texts to 16K, same 32K tokens per step
  *) log "unknown mode $MODE"; exit 1 ;;
esac
log "train $RUN"
$PY -m selfjev.cli $CMD --data runs/jev_all/train.jsonl.gz --val runs/jev_all/val.jsonl.gz $INIT \
  --lr $LR --soft-weight 0.5 $EXTRA --out runs/$RUN > runs/$RUN.log 2>&1 || { log "TRAIN FAILED"; tail -30 runs/$RUN.log; exit 1; }
for ad in adapter adapter_last; do
  [[ $ad == adapter ]] && $PY -c "import json, sys; sys.exit(json.load(open('runs/$RUN/train_meta.json'))['best']['step'] != 0)" \
    && { log "best checkpoint is step 0 (the start): skipped"; continue; }
  [[ $ad == adapter_last ]] && cmp -s runs/$RUN/adapter/adapter_model.safetensors runs/$RUN/adapter_last/adapter_model.safetensors && continue
  log "eval $ad"; $PY scripts/run_qwen35.py qwen35_4b --stage eval --tag _tree_${MODE}_jevall_${ad#adapter} --adapter runs/$RUN/$ad \
    --data-dir data/ova --sets $SETS 2>&1 | grep -E "EVAL|Error|error"
done
if [[ $MODE == scratch ]]; then  # eval_llm was never scored for these: the best model and the Jev-target fine-tune
  for b in "_tree weights/qwen35_4b_tree" "_tree_sft_jevall__last runs/qwen35_4b_tree_sft_jevall/adapter_last"; do
    set -- $b; log "eval_llm baseline $2"
    $PY scripts/run_qwen35.py qwen35_4b --stage eval --tag $1 --adapter $2 --data-dir data/ova --sets eval_llm 2>&1 | grep -E "EVAL|Error|error"
  done
fi
log "ALL DONE"
