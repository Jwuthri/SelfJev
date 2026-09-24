#!/usr/bin/env bash
# Score our 4B models on the frozen eval2 test set (data/eval2.jsonl: test only, never train or tune on it).
# Outputs reports/<run>/eval2; then Jev on the same questions, from the Mac:
#   zsh -ic 'uv run python scripts/compare_external.py --data data/eval2.jsonl --ours tree_4b/eval2 --only jev --tag eval2 --budget 2'
# max-length 16384: eval2 states reach ~8K tokens, and nothing is ever truncated.
set -euo pipefail
cd "$(dirname "$0")/.."
PJEV=".venv/bin/pjev"
R4B=(--model Qwen/Qwen3-Reranker-4B --revision 22e683669bc0f0bd69640a1354a6d0aebcfeede5 --dtype bfloat16 --max-length 16384)
log() { echo "[$(date +%H:%M:%S)] eval2: $*"; }
for run in "${@:-tree_4b tree_4b_r2 tree_4b_r2b}"; do
  for r in $run; do
    log "$r"
    $PJEV eval --tree --data data/eval2.jsonl --split test --out reports/$r/eval2 "${R4B[@]}" --adapter runs/$r/adapter > /dev/null
  done
done
log "lora_4b (stock pairs, prompt answer-v1 as selected on validation)"
$PJEV eval --data data/eval2.jsonl --split test --out reports/lora_4b/eval2 "${R4B[@]}" --adapter runs/lora_4b/adapter --prompt answer-v1 > /dev/null
log "ALL DONE"
