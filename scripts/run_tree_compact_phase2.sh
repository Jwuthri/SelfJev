#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONPATH=src OMP_NUM_THREADS=4
R=reports/latency_optimization_2026-09-24
P=.venv/bin/python
$P scripts/tree_latency_experiment.py teacher --config configs/tree_4b_compact_v2.json --out "$R/teacher_train.json"
$P -c 'from personal_jev.train_tree import train; train("configs/tree_4b_compact_v2.json")'
# The selected checkpoint is fixed by validation loss before development/fresh evaluation.
bash scripts/evaluate_tree_compact_phase2.sh
