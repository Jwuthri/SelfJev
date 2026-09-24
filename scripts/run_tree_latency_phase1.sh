#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONPATH=src OMP_NUM_THREADS=4
R=reports/latency_optimization_2026-09-24
P=.venv/bin/python
$P scripts/tree_latency_experiment.py parity --out "$R/parity_a10g.json"
$P scripts/tree_latency_experiment.py bench --original --out "$R/hf_original_a10g.json"
$P scripts/tree_latency_experiment.py bench --profile --out "$R/hf_optimized_a10g.json"
$P scripts/tree_latency_experiment.py eval --out "$R/r1_merged_development.json"
$P scripts/tree_latency_experiment.py eval --unmerged --out "$R/r1_unmerged_development.json"
$P -m personal_jev.vllm_tree merge --adapter runs/tree_4b/adapter --out runs/tree_4b/merged
date -u > "$R/hf_phase1_complete.txt"
