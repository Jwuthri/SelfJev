#!/usr/bin/env bash
# Grow the combined dataset (data/all.jsonl.gz) with a batch written by
#   zsh -ic 'uv run python scripts/gen_hardcases.py --batch <name> --model <writer> --budget <usd> [mode flags]'
# Steps (see data/README.md "Grow it"):
#   bash scripts/grow_batch.sh <name> judge    # PAID, user OK first: blind GPT-6 Astra (OpenAI batch, ~$4 per 1K questions)
#   bash scripts/grow_batch.sh <name> build    # free: strict build + overlap guard vs every test set + moderation screen
#   bash scripts/grow_batch.sh <name> finish   # PAID, tiny (~$0.03 per 1K questions): Jev predictions + rebuild all.jsonl.gz
set -euo pipefail
cd "$(dirname "$0")/.."
name=${1:?batch name}; step=${2:?judge|build|finish}
dir=data/batches/$name
[ -d "$dir/raw" ] || { echo "no $dir/raw: write the batch first with gen_hardcases.py --batch $name"; exit 2; }
mkdir -p "reports/batches/$name"
case $step in
  judge)
    zsh -ic "uv run python scripts/judge_hardcases.py --raw $dir/raw --review $dir/review" ;;
  build)
    uv run python scripts/build_hardcases.py --strict --raw "$dir/raw" --review "$dir/review" --out "data/batches/$name.jsonl" \
      --guard data/eval.jsonl data/eval2.jsonl data/eval_llm.jsonl data/compact_challenge_v1.jsonl
    zsh -ic "uv run python scripts/moderate_texts.py $dir/raw --out reports/batches/$name/moderation.jsonl"
    uv run python - "$name" <<'EOF'
import json, sys
rows = [json.loads(l) for l in open(f"reports/batches/{sys.argv[1]}/moderation.jsonl")]
flag = [r["source_id"] for r in rows if r["flagged"] or max(r["scores"].values()) >= 0.3]
print(f"moderation: {len(flag)} of {len(rows)} texts to read before finishing: {flag[:40]}")
EOF
    [ -f "$dir/README.md" ] || echo "write a one-line description of the batch in $dir/README.md" ;;
  finish)
    zsh -ic "uv run python scripts/jev_predictions.py --call --budget 2"
    uv run python scripts/build_all.py ;;
  *) echo "step: judge|build|finish"; exit 2 ;;
esac
