#!/usr/bin/env bash
# Shared-prefix tree scorer on one CUDA GPU with the 4B backbones:
# tests -> untrained validation check of both backbones -> LoRA training -> evals + held-out calibration -> speed vs stock 4B.
set -uo pipefail
cd "$(dirname "$0")/.."
PJEV=".venv/bin/pjev"; DATA="data/hf.jsonl data/eval.jsonl"
R4B=(--model Qwen/Qwen3-Reranker-4B --revision 22e683669bc0f0bd69640a1354a6d0aebcfeede5 --dtype bfloat16)
I4B=(--model Qwen/Qwen3-4B-Instruct-2507 --revision cdbee75f17c01a7cc42f958dc650907174af0554 --dtype bfloat16)
log() { echo "[$(date +%H:%M:%S)] $*"; }
evals() {  # name [model args...]
  local name=$1; shift
  for split in validation calibration test; do
    $PJEV eval --tree --data $DATA --split $split --out reports/$name/$split "$@" > /dev/null
  done
  $PJEV calibrate --fit reports/$name/calibration/report.json --thresholds reports/$name/validation/report.json --out calib/$name.json > /dev/null
  $PJEV eval --tree --data $DATA --split test --out reports/$name/test_calibrated --calibration calib/$name.json "$@" > /dev/null
  log "$name: $(grep -m1 'question accuracy' reports/$name/test/report.md)"
}
log "pytest"; (.venv/bin/python -m pytest -q tests/test_tree.py 2>&1 | tail -2) || true
for pair in "reranker_4b R4B" "instruct_4b I4B"; do
  set -- $pair; declare -n M=$2
  $PJEV eval --tree --data $DATA --split validation --out reports/tree_zeroshot_$1/validation "${M[@]}" > /dev/null
  log "untrained tree $1 (validation): $(grep -m1 'question accuracy' reports/tree_zeroshot_$1/validation/report.md)"
done
log "train tree_4b"; $PJEV train-tree configs/tree_4b.json > runs/tree_4b.log 2>&1
evals tree_4b "${R4B[@]}" --adapter runs/tree_4b/adapter
log "train tree_4b_instruct"; $PJEV train-tree configs/tree_4b_instruct.json > runs/tree_4b_instruct.log 2>&1
evals tree_4b_instruct "${I4B[@]}" --adapter runs/tree_4b_instruct/adapter
log "benchmarks (bf16, same GPU)"
$PJEV bench --tree "${R4B[@]}" --adapter runs/tree_4b/adapter --repeats 10 --out reports/bench/gpu_tree_4b_bf16 > /dev/null
$PJEV bench "${R4B[@]}" --adapter runs/lora_4b/adapter --repeats 10 --out reports/bench/gpu_stock_lora_4b_bf16 > /dev/null
.venv/bin/python -c "from personal_jev.benchmark import run; run(tree=True, model_id='Qwen/Qwen3-Reranker-4B', revision='22e683669bc0f0bd69640a1354a6d0aebcfeede5', adapter='runs/tree_4b/adapter', dtype='bfloat16', grid=[(16384, 1, 1, 'binary'), (32000, 1, 1, 'binary'), (16384, 16, 3, 'multiclass'), (32000, 16, 3, 'multiclass')], repeats=3, out_dir='reports/bench/gpu_tree_4b_long_bf16')" > /dev/null || log "tree long-context bench failed"
.venv/bin/python -c "from personal_jev.benchmark import run; run(model_id='Qwen/Qwen3-Reranker-4B', revision='22e683669bc0f0bd69640a1354a6d0aebcfeede5', adapter='runs/lora_4b/adapter', dtype='bfloat16', grid=[(16384, 1, 1, 'binary'), (16384, 16, 3, 'multiclass')], repeats=2, out_dir='reports/bench/gpu_stock_lora_4b_long_bf16')" > /dev/null || log "stock long-context bench failed"
log "ALL DONE"
