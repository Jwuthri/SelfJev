#!/usr/bin/env bash
# Optional argument: wait for this task's trainer PID. Missing train_meta prevents evaluation of an unfinished run.
set -euo pipefail
cd "$(dirname "$0")/.."
if [[ $# -gt 0 ]]; then
  while kill -0 "$1" 2>/dev/null; do sleep 15; done
fi
export PYTHONPATH=src OMP_NUM_THREADS=4
R=reports/latency_optimization_2026-09-24
P=.venv/bin/python
A=runs/tree_4b_compact_v2/adapter
test -s runs/tree_4b_compact_v2/train_meta.json
$P scripts/tree_latency_experiment.py eval --adapter "$A" --out "$R/compact_development.json"
$P scripts/tree_latency_experiment.py eval --adapter "$A" --data data/compact_challenge_v1.jsonl --out "$R/compact_fresh.json"
$P scripts/tree_latency_experiment.py eval --data data/compact_challenge_v1.jsonl --out "$R/r1_fresh.json"
$P scripts/tree_latency_experiment.py bench --adapter "$A" --out "$R/hf_compact_a10g.json"
$P scripts/tree_latency_experiment.py parity --adapter "$A" --out "$R/parity_compact_a10g.json"
$P -m personal_jev.vllm_tree merge --adapter "$A" --out runs/tree_4b_compact_v2/merged
/home/ubuntu/vllm-env/bin/python scripts/bench_tree_vllm.py --model-dir runs/tree_4b_compact_v2/merged \
  --out "$R/vllm_compact_a10g.json" --reference-parity "$R/parity_compact_a10g.json" \
  --reference-eval "$R/compact_development.json" --document-warm
/home/ubuntu/vllm-env/bin/python scripts/bench_tree_vllm.py --out "$R/vllm_extended_a10g.json" \
  --document-warm --skip-quality
date -u > "$R/phase2_complete.txt"
