#!/usr/bin/env bash
# Full stock-backend pipeline for one Qwen3-Reranker size (used for 4B / 8B on a GPU box):
# validation-only prompt selection -> baseline evals + held-out calibration -> LoRA training -> tuned evals -> bench.
# usage: scripts/run_model.sh NAME MODEL_ID REVISION [DTYPE]    e.g. scripts/run_model.sh 4b Qwen/Qwen3-Reranker-4B 22e6836... bfloat16
set -euo pipefail
cd "$(dirname "$0")/.."
NAME=$1 MODEL=$2 REV=$3 DTYPE=${4:-bfloat16}
PJEV=".venv/bin/pjev"; PY=".venv/bin/python"
M=(--model "$MODEL" --revision "$REV" --dtype "$DTYPE")
DATA=(data/hf.jsonl data/eval.jsonl)
log() { echo "[$(date +%H:%M:%S)] $NAME: $*"; }

log "prompt selection (validation only)"
$PY scripts/select_prompt.py "${DATA[@]}" --model "$MODEL" --revision "$REV" --dtype "$DTYPE" --out "reports/$NAME/prompt_selection" > /dev/null
PROMPT=$($PY -c "import json; print(json.load(open('reports/$NAME/prompt_selection/selected.json'))['selected'])")
log "selected prompt $PROMPT"

evals() {  # tag [extra args...]
  local tag=$1; shift
  for split in validation calibration test; do
    $PJEV eval --data "${DATA[@]}" --split $split --out reports/$tag/$split --prompt "$PROMPT" "${M[@]}" "$@" > /dev/null
  done
  $PJEV calibrate --fit reports/$tag/calibration/report.json --thresholds reports/$tag/validation/report.json --out calib/$tag.json > /dev/null
  $PJEV eval --data "${DATA[@]}" --split test --out reports/$tag/test_calibrated --calibration calib/$tag.json --prompt "$PROMPT" "${M[@]}" "$@" > /dev/null
  $PJEV eval --data data/synthetic.jsonl --split test --out reports/$tag/synthetic_test --prompt "$PROMPT" "${M[@]}" "$@" > /dev/null
  log "$tag evals done: $(grep -m1 'question accuracy' reports/$tag/test/report.md)"
}

log "baseline evals"; evals baseline_$NAME
log "LoRA training"
$PJEV train configs/lora_pilot.json --set model_id="\"$MODEL\"" revision="\"$REV\"" prompt="\"$PROMPT\"" dtype="\"$DTYPE\"" \
  out_dir="\"runs/lora_$NAME\"" max_batch_tokens=16384 grad_accum=2
log "tuned evals"; evals lora_$NAME --adapter runs/lora_$NAME/adapter
log "bench"
$PJEV bench "${M[@]}" --lengths 512,2048,8192 --questions 1,4,16 --repeats 10 --out reports/bench/${NAME}_base_$DTYPE > /dev/null
$PJEV bench "${M[@]}" --adapter runs/lora_$NAME/adapter --lengths 512,2048,8192 --questions 1,4,16 --repeats 10 --out reports/bench/${NAME}_lora_$DTYPE > /dev/null
log "ALL DONE"
