#!/usr/bin/env bash
# Round 2 for the shared-prefix tree scorer (tree.py / train_tree.py, recipe from the tree session): configs/tree_4b.json
# unchanged except the settings shared with the stock round 2 (scripts/run_4b_r2.sh) so the two stay comparable:
# + data/hardcases.jsonl in train and validation files, max_length 8192, max_val_questions 1400.
# Evaluated uncalibrated and calibrated on the same test ids (hf.jsonl + eval.jsonl test).
set -euo pipefail
cd "$(dirname "$0")/.."
PJEV=".venv/bin/pjev"
TAG=${TAG:-tree_4b_r2}
HARD_TRAIN=${HARD_TRAIN:-data/hardcases.jsonl}  # r2b: data/hardcases_nb.jsonl (scripts/rebalance_nota.py)
R4B=(--model Qwen/Qwen3-Reranker-4B --revision 22e683669bc0f0bd69640a1354a6d0aebcfeede5 --dtype bfloat16)
DATA=(data/hf.jsonl data/eval.jsonl)
log() { echo "[$(date +%H:%M:%S)] tree-r2: $*"; }

log "tree LoRA training (round 2)"
$PJEV train-tree configs/tree_4b.json --set \
  "train_files=[\"data/hf.jsonl\", \"data/synthetic.jsonl\", \"$HARD_TRAIN\"]" \
  'val_files=["data/hf.jsonl", "data/synthetic.jsonl", "data/eval.jsonl", "data/hardcases.jsonl"]' \
  "out_dir=\"runs/$TAG\"" max_length=8192 max_val_questions=1400
log "evals"
for split in validation calibration test; do
  $PJEV eval --tree --data "${DATA[@]}" --split $split --out reports/$TAG/$split "${R4B[@]}" --adapter runs/$TAG/adapter > /dev/null
done
$PJEV calibrate --fit reports/$TAG/calibration/report.json --thresholds reports/$TAG/validation/report.json --out calib/$TAG.json > /dev/null
$PJEV eval --tree --data "${DATA[@]}" --split test --out reports/$TAG/test_calibrated --calibration calib/$TAG.json "${R4B[@]}" --adapter runs/$TAG/adapter > /dev/null
log "done: $(grep -m1 'question accuracy' reports/$TAG/test/report.md)"
log "ALL DONE"
