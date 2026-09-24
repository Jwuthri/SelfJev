#!/usr/bin/env bash
# Learning-curve runs on one GPU, in sequence: train from configs/curve/NAME.json, then validation + test evals.
# Names tree_* use `pjev train-tree` + `--tree` evals. Special names: instruct_zero (prompt selection + zero-shot evals of Qwen3-4B-Instruct) and instruct_lora (LoRA on it).
# usage: CUDA_VISIBLE_DEVICES=0 scripts/run_curve.sh NAME [NAME...]     logs: runs/curve/NAME.log, results: reports/curve/NAME/
set -euo pipefail
cd "$(dirname "$0")/.."
export HF_HUB_OFFLINE=1
PJEV=".venv/bin/pjev"; PY=".venv/bin/python"
DATA=(data/hf.jsonl data/eval.jsonl)
INSTRUCT=(--model Qwen/Qwen3-4B-Instruct-2507 --revision cdbee75f17c01a7cc42f958dc650907174af0554)
R4B=(--model Qwen/Qwen3-Reranker-4B --revision 22e683669bc0f0bd69640a1354a6d0aebcfeede5)
mkdir -p runs/curve reports/curve
log() { echo "[$(date +%H:%M:%S)] $*"; }

evals() {  # tag [pjev model args...]
  local tag=$1; shift
  for split in validation test; do
    $PJEV eval --data "${DATA[@]}" --split $split --out reports/curve/$tag/$split --dtype bfloat16 "$@" > /dev/null
  done
  log "$tag: $(grep -m1 'question accuracy' reports/curve/$tag/test/report.md) (test)"
}

for NAME in "$@"; do
  {
    log "start $NAME on GPU ${CUDA_VISIBLE_DEVICES:-?}"
    if [[ $NAME == instruct_zero ]]; then
      $PY scripts/select_prompt.py "${DATA[@]}" "${INSTRUCT[@]}" --dtype bfloat16 --out reports/curve/instruct_prompt_selection > /dev/null
      PROMPT=$($PY -c "import json; print(json.load(open('reports/curve/instruct_prompt_selection/selected.json'))['selected'])")
      log "instruct prompt selected on validation: $PROMPT"
      evals instruct_zero "${INSTRUCT[@]}" --prompt "$PROMPT"
    elif [[ $NAME == instruct_lora ]]; then
      PROMPT=$($PY -c "import json; print(json.load(open('reports/curve/instruct_prompt_selection/selected.json'))['selected'])")
      $PJEV train configs/curve/instruct_lora.json --set prompt="\"$PROMPT\""
      evals instruct_lora "${INSTRUCT[@]}" --prompt "$PROMPT" --adapter runs/curve/instruct_lora/adapter
    elif [[ $NAME == tree_* ]]; then  # tree scorer ablations (configs/curve/tree_*.json, e.g. LoRA rank / MLP targets)
      $PJEV train-tree configs/curve/$NAME.json ${TRAIN_SET:+--set $TRAIN_SET}  # e.g. TRAIN_SET='max_batch_tokens=8192 grad_accum=4' on a 24 GB GPU (same effective batch)
      if [[ $NAME == *instruct* ]]; then M=("${INSTRUCT[@]}"); else M=("${R4B[@]}"); fi  # base model follows the run name
      evals $NAME --tree "${M[@]}" --adapter runs/curve/$NAME/adapter
      $PJEV eval --tree --data data/eval2.jsonl --split test --out reports/curve/$NAME/eval2 --dtype bfloat16 --max-length 16384 "${M[@]}" --adapter runs/curve/$NAME/adapter > /dev/null
      log "$NAME: $(grep -m1 'question accuracy' reports/curve/$NAME/eval2/report.md) (eval2)"
    else
      $PJEV train configs/curve/$NAME.json
      evals $NAME "${R4B[@]}" --prompt answer-v1 --adapter runs/curve/$NAME/adapter
    fi
    log "done $NAME"
  } > runs/curve/$NAME.log 2>&1
done
