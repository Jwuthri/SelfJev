#!/usr/bin/env bash
# The combined recipe (user request 2026-09-24): shared-prefix tree + Qwen3-4B-Instruct-2507 + LoRA r64
# (configs/tree_4b_instruct_r3.json, r2_*/r3_* uncapped) + every option listed in the question (data/ova/,
# scripts/options_in_question.py). Serving is measured separately (merged LoRA + vLLM).
#   R3=0 TAG=tree_4b_combo_r2  -> without round 3: compare with tree_4b_instruct_r2x64 (same recipe, no option lists)
#   default TAG=tree_4b_combo  -> with round 3:    compare with tree_4b_instruct_r3
# On a 24 GB A10G: MBT=8192 GA=4 (the same 32K-token effective batch). Evals on the transformed files.
set -euo pipefail
cd "$(dirname "$0")/.."
PJEV=".venv/bin/pjev"
TAG=${TAG:-tree_4b_combo}
I4B=(--model Qwen/Qwen3-4B-Instruct-2507 --revision cdbee75f17c01a7cc42f958dc650907174af0554 --dtype bfloat16)
log() { echo "[$(date +%H:%M:%S)] $TAG: $*"; }
TRAIN='"data/ova/hf.jsonl", "data/ova/synthetic.jsonl", "data/ova/hardcases_nb.jsonl"'
VAL='"data/ova/hf.jsonl", "data/ova/synthetic.jsonl", "data/ova/eval.jsonl", "data/ova/hardcases.jsonl"'
if [ "${R3:-1}" = 1 ]; then TRAIN="$TRAIN, \"data/ova/hardcases_r3.jsonl\""; VAL="$VAL, \"data/ova/hardcases_r3.jsonl\""; fi
log "training"
$PJEV train-tree configs/tree_4b_instruct_r3.json --set "out_dir=\"runs/$TAG\"" "max_batch_tokens=${MBT:-8192}" \
  "grad_accum=${GA:-4}" "train_files=[$TRAIN]" "val_files=[$VAL]"
log "evals"
for split in validation test; do
  $PJEV eval --tree --data data/ova/hf.jsonl data/ova/eval.jsonl --split $split --out reports/$TAG/$split "${I4B[@]}" --adapter runs/$TAG/adapter > /dev/null
done
$PJEV eval --tree --data data/ova/eval2.jsonl --split test --out reports/$TAG/eval2 "${I4B[@]}" --max-length 16384 --adapter runs/$TAG/adapter > /dev/null
log "done: old test $(grep -m1 'question accuracy' reports/$TAG/test/report.md); eval2 $(grep -m1 'question accuracy' reports/$TAG/eval2/report.md)"
log "ALL DONE"
