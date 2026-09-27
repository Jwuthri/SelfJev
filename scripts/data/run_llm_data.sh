#!/usr/bin/env bash
# LLM-evaluation data (score, judge, verify, guardrail, jailbreak; data/hardcases/BRIEF_llm.md). PAID: needs the user's OK.
#   bash scripts/run_llm_data.sh train   # ~11K questions from Luna/Gemini/Grok/DeepSeek, Astra batch judge -> data/hardcases_llm.jsonl
#   bash scripts/run_llm_data.sh test    # ~1.1K questions from eval2's writers, Astra + Claude Sonnet 5 judges (not Gemini 3.1 Pro: user, 2026-09-25) -> data/eval_llm.jsonl
# Budgets below are hard caps per writer; generation is balanced over use case x tier x length inside each writer's run.
# Resumable: rerunning continues ids and judges only unsubmitted sources. Keys via zsh -ic, never printed.
set -euo pipefail
cd "$(dirname "$0")/.."
LOG=reports/hardcases_llm; mkdir -p $LOG reports/eval_llm
gen() { zsh -ic "uv run python scripts/gen_hardcases.py --usecases $*"; }

if [ "${1:-}" = train ]; then
  gen train --model openai/gpt-6-luna        --max-questions 4500 --budget 4  > $LOG/gen_lu.log 2>&1 &
  gen train --model google/gemini-3.8-flash  --max-questions 3000 --budget 20 > $LOG/gen_gf.log 2>&1 &
  gen train --model x-ai/grok-4.7            --max-questions 2000 --budget 22 > $LOG/gen_gk.log 2>&1 &
  gen train --model deepseek/deepseek-v4-flash --max-questions 1500 --budget 1 > $LOG/gen_df.log 2>&1 &
  wait
  zsh -ic 'uv run python scripts/judge_hardcases.py --raw data/hardcases_llm/raw --review data/hardcases_llm/review' > $LOG/judge.log 2>&1
  guard="data/eval.jsonl data/eval2.jsonl"; [ -f data/eval_llm.jsonl ] && guard="$guard data/eval_llm.jsonl"
  uv run python scripts/build_hardcases.py --raw data/hardcases_llm/raw --review data/hardcases_llm/review \
    --out data/hardcases_llm.jsonl --guard $guard
elif [ "${1:-}" = test ]; then
  LOG=reports/eval_llm
  gen test --model anthropic/claude-opus-5.5 --max-questions 370 --budget 12 > $LOG/gen_opus.log 2>&1 &
  gen test --model moonshotai/kimi-k3        --max-questions 370 --budget 5  > $LOG/gen_kimi.log 2>&1 &
  gen test --model z-ai/glm-5.3              --max-questions 370 --budget 4  > $LOG/gen_glm.log 2>&1 &
  wait
  # one judge process per review dir at a time
  zsh -ic 'uv run python scripts/judge_hardcases.py --raw data/eval_llm/raw --review data/eval_llm/review --jev' > $LOG/judge_astra.log 2>&1
  zsh -ic 'uv run python scripts/judge_hardcases.py --raw data/eval_llm/raw --review data/eval_llm/review --sync-model anthropic/claude-sonnet-5' > $LOG/judge_sonnet.log 2>&1
  uv run python scripts/build_eval2.py --raw data/eval_llm/raw --review data/eval_llm/review --out data/eval_llm.jsonl \
    --guard data/hf.jsonl data/synthetic.jsonl data/eval.jsonl data/eval2.jsonl data/hardcases.jsonl data/hardcases_r3.jsonl
else
  echo "usage: $0 train|test"; exit 2
fi
