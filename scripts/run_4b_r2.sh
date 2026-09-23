#!/usr/bin/env bash
# Round 2 for the 4B: same model, prompt and hyperparameters as round 1 (runs/lora_4b), plus the verified hard-case
# training data. Evaluates on the same test set (hf.jsonl + eval.jsonl test) so the table stays comparable.
set -euo pipefail
cd "$(dirname "$0")/.."
PJEV=".venv/bin/pjev"
MODEL=Qwen/Qwen3-Reranker-4B REV=22e683669bc0f0bd69640a1354a6d0aebcfeede5 PROMPT=answer-v1 DTYPE=bfloat16 TAG=lora_4b_r2
M=(--model "$MODEL" --revision "$REV" --dtype "$DTYPE" --prompt "$PROMPT")
DATA=(data/hf.jsonl data/eval.jsonl)
log() { echo "[$(date +%H:%M:%S)] r2: $*"; }

log "LoRA training (round 2)"
$PJEV train configs/lora_pilot.json --set model_id="\"$MODEL\"" revision="\"$REV\"" prompt="\"$PROMPT\"" dtype="\"$DTYPE\"" \
  out_dir="\"runs/$TAG\"" max_batch_tokens=16384 grad_accum=2 \
  train_files='["data/hf.jsonl", "data/synthetic.jsonl", "data/hardcases.jsonl"]' \
  val_files='["data/hf.jsonl", "data/synthetic.jsonl", "data/eval.jsonl", "data/hardcases.jsonl"]' max_val_questions=1400
log "evals"
for split in validation calibration test; do
  $PJEV eval --data "${DATA[@]}" --split $split --out reports/$TAG/$split "${M[@]}" --adapter runs/$TAG/adapter > /dev/null
done
$PJEV calibrate --fit reports/$TAG/calibration/report.json --thresholds reports/$TAG/validation/report.json --out calib/$TAG.json > /dev/null
$PJEV eval --data "${DATA[@]}" --split test --out reports/$TAG/test_calibrated --calibration calib/$TAG.json "${M[@]}" --adapter runs/$TAG/adapter > /dev/null
$PJEV eval --data data/synthetic.jsonl --split test --out reports/$TAG/synthetic_test "${M[@]}" --adapter runs/$TAG/adapter > /dev/null
log "done: $(grep -m1 'question accuracy' reports/$TAG/test/report.md)"
log "ALL DONE"
