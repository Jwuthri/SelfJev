#!/usr/bin/env bash
# On the GPU box (~/sj = repo subset): continue selfjev-4b-vision on runs/verdict_json_v1 (batches verdict_json_v1 +
# typed_decisions_train_v1 + text and image replay, scripts/data/build_verdict_mix.py), then score it the way the vision
# release was scored (data/ova files, test split) and on the two public benchmarks that motivated the data (diagnostic only).
# usage: verdict_json_box.sh [RUN]   RUN = runs/<RUN> mix name (default verdict_json_v1), reports go to reports/<RUN>.
set -uo pipefail
RUN=${1:-verdict_json_v1}; N=selfjev-${RUN//_/-}
export PATH=$HOME/.local/bin:$PATH
cd ~/sj
uv sync -q --extra gpu > ~/logs/uv_sync.log 2>&1 || { echo "FAIL uv sync"; tail -20 ~/logs/uv_sync.log; exit 1; }
uv pip install -q pyarrow
uv run python -c "from huggingface_hub import snapshot_download as s; from selfjev.engine.qwen35 import BASE; s(BASE[0], revision=BASE[1])"
R=runs/$RUN
A=$R/run/adapter
echo "=== train $(date +%T)"
HF_HUB_OFFLINE=1 uv run selfjev finetune --data $R/train.jsonl.gz --val $R/val.jsonl.gz --out $R/run --init weights/selfjev_4b_vision \
  --lr 5e-5 --soft-weight 0.5 --max-length 16384 --batch-tokens 16384 --grad-accum 2 --epochs 1 > ~/logs/train.log 2>&1 \
  || { echo "FAIL train"; tail -30 ~/logs/train.log; exit 1; }
echo "=== trained $(date +%T)"
for s in "eval2:data/ova/eval2.jsonl" "eval_llm:data/ova/eval_llm.jsonl" "images:data/ova/eval_images_v1.jsonl" "test:data/ova/hf.jsonl data/ova/eval.jsonl"; do
  n=${s%%:*}; d=${s#*:}
  # shellcheck disable=SC2086  # $d holds one or two paths
  HF_HUB_OFFLINE=1 uv run selfjev eval --data $d --split test --adapter $A --out reports/$RUN/$n > ~/logs/eval_$n.log 2>&1
  echo "EVAL $n $(python3 -c "import json; print(round(100*json.load(open('reports/$RUN/$n/report.json'))['metrics']['question_accuracy'], 2))" 2>&1)"
done
HF_HUB_OFFLINE=1 nohup uv run selfjev serve --adapter $A --port 8000 > ~/logs/serve.log 2>&1 &
until curl -sf -o /dev/null localhost:8000/v1/models; do kill -0 $! 2>/dev/null || { echo "FAIL serve"; exit 1; }; sleep 10; done
(cd scripts/eval && uv run python score_typed_decisions.py --url http://127.0.0.1:8000 --model selfjev-4b --name "$N" \
   --parquet ~/sj/data/td_test.parquet --out ~/sj/reports/competitors/typed_decisions --workers 4 2>&1 | tail -1)
source scripts/eval/competitors/lib.sh
jb "$N" 8000 selfjev-4b
for f in eval2 eval_llm; do
  uv run python scripts/eval/score_systemone.py --url http://127.0.0.1:8000 --model selfjev-4b --name "$N-api" \
    --data data/$f.jsonl --ours images_v1/$f --out reports/competitors/$f --workers 4 2>&1 | grep EVAL
done
echo DONE
