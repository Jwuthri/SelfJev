#!/usr/bin/env bash
# Round 3 on the Instruct base (user request 2026-09-24): shared-prefix tree + Qwen3-4B-Instruct-2507 + LoRA r64,
# configs/tree_4b_instruct_r3.json. The r2_*/r3_* hard-case families are exempt from the 1,600-per-family cap
# (the cap silently dropped ~2.7K of round 2's questions in r2b).
#   R3=0 TAG=tree_4b_instruct_r2x64 -> the same recipe without round 3: the control that isolates what round 3 adds.
#   On a 24 GB A10G: MBT=8192 GA=4 (same 32K-token effective batch).
# Evals: validation, old test (hf + eval test), eval2 (frozen; never tune on it).
set -euo pipefail
cd "$(dirname "$0")/.."
PJEV=".venv/bin/pjev"
TAG=${TAG:-tree_4b_instruct_r3}
I4B=(--model Qwen/Qwen3-4B-Instruct-2507 --revision cdbee75f17c01a7cc42f958dc650907174af0554 --dtype bfloat16)
log() { echo "[$(date +%H:%M:%S)] $TAG: $*"; }
SET=("out_dir=\"runs/$TAG\"" "max_batch_tokens=${MBT:-16384}" "grad_accum=${GA:-2}")
if [ "${R3:-1}" = 0 ]; then
  SET+=('train_files=["data/hf.jsonl", "data/synthetic.jsonl", "data/hardcases_nb.jsonl"]'
        'val_files=["data/hf.jsonl", "data/synthetic.jsonl", "data/eval.jsonl", "data/hardcases.jsonl"]')
fi
log "training"
$PJEV train-tree configs/tree_4b_instruct_r3.json --set "${SET[@]}"
log "evals"
$PJEV eval --tree --data data/hf.jsonl data/eval.jsonl --split validation --out reports/$TAG/validation "${I4B[@]}" --adapter runs/$TAG/adapter > /dev/null
$PJEV eval --tree --data data/hf.jsonl data/eval.jsonl --split test --out reports/$TAG/test "${I4B[@]}" --adapter runs/$TAG/adapter > /dev/null
$PJEV eval --tree --data data/eval2.jsonl --split test --out reports/$TAG/eval2 "${I4B[@]}" --max-length 16384 --adapter runs/$TAG/adapter > /dev/null
log "done: old test $(grep -m1 'question accuracy' reports/$TAG/test/report.md); eval2 $(grep -m1 'question accuracy' reports/$TAG/eval2/report.md)"
log "ALL DONE"
