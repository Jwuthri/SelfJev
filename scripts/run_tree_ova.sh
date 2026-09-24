#!/usr/bin/env bash
# Tree 4B with every option listed in the question ("all options at once", scripts/options_in_question.py): the r2b
# recipe (scripts/run_tree_r2.sh with data/hardcases_nb.jsonl) on the data/ova/ copies, so the only change is the
# question text. Evaluated like r2b on validation and the old test (hf + eval), then on eval2, all transformed.
# Distillation variant: TAG=tree_4b_ova_kd EXTRA_SET='teacher_weight=0.5 teacher_file="data/teacher/qwen38_27b_ova_train.json"'
set -euo pipefail
cd "$(dirname "$0")/.."
PJEV=".venv/bin/pjev"
TAG=${TAG:-tree_4b_ova}
R4B=(--model Qwen/Qwen3-Reranker-4B --revision 22e683669bc0f0bd69640a1354a6d0aebcfeede5 --dtype bfloat16)
log() { echo "[$(date +%H:%M:%S)] tree-ova: $*"; }
log "training"
$PJEV train-tree configs/tree_4b.json --set \
  'train_files=["data/ova/hf.jsonl", "data/ova/synthetic.jsonl", "data/ova/hardcases_nb.jsonl"]' \
  'val_files=["data/ova/hf.jsonl", "data/ova/synthetic.jsonl", "data/ova/eval.jsonl", "data/ova/hardcases.jsonl"]' \
  "out_dir=\"runs/$TAG\"" max_length=8192 max_val_questions=1400 ${EXTRA_SET:-}
log "evals"
for split in validation test; do
  $PJEV eval --tree --data data/ova/hf.jsonl data/ova/eval.jsonl --split $split --out reports/$TAG/$split "${R4B[@]}" --adapter runs/$TAG/adapter > /dev/null
done
$PJEV eval --tree --data data/ova/eval2.jsonl --split test --out reports/$TAG/eval2 "${R4B[@]}" --max-length 16384 --adapter runs/$TAG/adapter > /dev/null
log "done: test $(grep -m1 'question accuracy' reports/$TAG/test/report.md); eval2 $(grep -m1 'question accuracy' reports/$TAG/eval2/report.md)"
log "ALL DONE"
