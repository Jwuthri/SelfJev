# Helpers for the competitor jobs on the GPU box (sourced by each queue job). Layout: ~/sj = this repo subset,
# ~/logs = logs. Each competitor: setup_<name>.sh installs it in its own venv and starts its /v1/systemone server.
# ponytail: one GPU, one server at a time; teardown kills every GPU process.
export PATH=$HOME/.local/bin:$PATH
SJ=~/sj; OUT=reports/competitors

up() {  # up SETUP PORT -> 0 when a tiny request answers (the setup script waits for its own health check first)
  echo "=== setup $1 $(date +%T)"
  timeout 3000 bash "$SJ/scripts/eval/competitors/setup_$1.sh" > ~/logs/setup_$1.log 2>&1 || echo "setup $1 exited $?"
  python3 ~/sj/scripts/eval/competitors/smoke.py "$2" > ~/logs/smoke_$1.log 2>&1
  head -c 600 ~/logs/smoke_$1.log; echo
  grep -q '^200' ~/logs/smoke_$1.log || { echo "SETUP_FAIL $1"; tail -30 ~/logs/setup_$1.log; return 1; }
}

score() {  # score NAME PORT MODEL IMAGES(0|1) [EXTRA_JSON] [MAX_QUESTIONS] [IMAGE_STYLE raw|dict|messages]
  local name=$1 port=$2 model=$3 images=$4 extra=${5:-'{}'} maxq=${6:-64} style=${7:-raw} files="eval2 eval_llm"
  [ "$images" = 1 ] && files="$files eval_images_v1"
  cd $SJ
  for f in $files; do
    local o=$f; [ "$f" = eval_images_v1 ] && o=images_v1_images
    uv run python scripts/eval/score_systemone.py --url http://127.0.0.1:$port --model "$model" --name "$name" --extra "$extra" \
      --max-questions $maxq --image-style $style --data data/$f.jsonl --ours images_v1/$o --out $OUT/$f --workers 4 2>&1 | grep -E "EVAL|error|Traceback" | cut -c1-600 | tail -6
  done
  (cd scripts/eval && uv run python score_typed_decisions.py --url http://127.0.0.1:$port --model "$model" --name "$name" --extra "$extra" \
     --parquet $SJ/data/td_test.parquet --out $SJ/$OUT/typed_decisions --workers 4 2>&1 | tail -2 | cut -c1-600)
  jb "$name" "$port" "$model"
}

jb() {  # jb NAME PORT MODEL -> JevBench public-231 through its own runner (typesafe adapter, one question per request)
  local name=$1 port=$2 model=$3 run=$HOME/runs/jb_$1_$(date +%H%M%S)
  [ -d ~/jevbench ] || git clone -q https://github.com/fstandhartinger/jevbench ~/jevbench
  cd ~/jevbench && git checkout -q bb05a335bc809e61b20c0f745d25499a82b326fc && mkdir -p $run $SJ/$OUT/jevbench/$name
  python3 -m jevbench.cli run --adapter typesafe --endpoint http://127.0.0.1:$port --key-env '' --model "$model" \
    --tasks datasets/public/easy.jsonl,datasets/public/original.jsonl,datasets/public/hard.jsonl \
    --results $run/results.jsonl --raw-dir $run/raw --ledger $run/ledger.jsonl --reserve-usd 0 \
    --cost-basis no_billable_account_self_hosted --run-label "$name" --manifest $run/manifest.json > $run/run.log 2>&1
  cp $run/results.jsonl $run/manifest.json $run/run.log $SJ/$OUT/jevbench/$name/ 2>/dev/null
  PYTHONPATH=. python3 $SJ/scripts/eval/competitors/jb_tiers.py $run/results.jsonl > $SJ/$OUT/jevbench/$name/tiers.txt 2>&1
  sed "s/^/JB $name /" $SJ/$OUT/jevbench/$name/tiers.txt | head -4 | cut -c1-300
  cd $SJ
}

teardown() {
  ss -ltnp 2>/dev/null | grep -oP 'pid=\K[0-9]+' | sort -u | xargs -r kill 2>/dev/null  # CPU-side servers too (shims, proxies)
  nvidia-smi --query-compute-apps=pid --format=csv,noheader | xargs -r kill 2>/dev/null; sleep 8
  nvidia-smi --query-compute-apps=pid --format=csv,noheader | xargs -r kill -9 2>/dev/null; sleep 3
  echo "=== teardown $(date +%T), GPU used: $(nvidia-smi --query-gpu=memory.used --format=csv,noheader)"
}
