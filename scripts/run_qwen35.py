"""Qwen3.5 (hybrid Gated DeltaNet + full attention) shared-document scorer: LoRA training and evals on one CUDA GPU.

Ported from the Codex challenger worktree (scripts/run_challenger.py) and pointed at the round-2 recipe of
tree_4b_instruct_r2x64: hf + synthetic + hardcases_nb, r2_* families exempt from the 1,600 cap, LoRA r64 / alpha 128.
Differences from that tree run, on purpose and recorded in train_meta.json:
- training scores every candidate as its own full sequence (the Qwen3.5 cache mutates recurrent state in place, so the
  shared-root backward pass of the tree is not available); inference shares the document by forking the native cache
  (challengers.ChallengerScorer.shared_entries), exact up to bf16 noise;
- training questions longer than --train-max-len tokens are dropped (default 2048, as in the Qwen3.5-2B challenger run),
  to keep the full-sequence cost inside the approved budget; evals read up to 32K tokens, nothing is truncated;
- LoRA targets are the attention projections of both layer kinds (q/k/v/o and in_proj_qkv/z/b/a, out_proj).

usage (on the GPU box):
  python scripts/run_qwen35.py qwen35_4b --stage train --tag _r2x64
  python scripts/run_qwen35.py qwen35_4b --stage eval  --tag _r2x64 --adapter runs/qwen35_4b_r2x64/adapter
  python scripts/run_qwen35.py qwen35    --stage eval  --tag _r1 --adapter runs/challengers/qwen35/adapter --sets eval2
"""
import argparse, gc, hashlib, json, math, random, statistics, time
from pathlib import Path

import torch

from personal_jev import benchmark, evaluate
from personal_jev.challengers import ChallengerScorer
from personal_jev.classify import classify
from personal_jev.data import sha256_file
from personal_jev.model import InputTooLong
from personal_jev.schemas import parse_question
from personal_jev.train import DEFAULTS, grouped_loss, question_correct, select_data

R2 = ["r2_simple", "r2_hard", "r2_very_hard"]
LINEAR = ["q_proj", "k_proj", "v_proj", "o_proj", "in_proj_qkv", "in_proj_z", "in_proj_b", "in_proj_a", "out_proj"]


def save(path, d):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(d, indent=1))


def items(sc, examples):
    out, dropped = [], []
    for ex in examples:
        q = parse_question({"id": "q", **ex["question"]})
        try:
            e = sc.entry(ex["state"], q)
        except InputTooLong:
            dropped.append(ex["id"]); continue
        ids = [c.id for c in q.candidates]
        target = ex["target"] if q.type == "binary" else ids.index(ex["target"]) if q.type == "multiclass" else [c in ex["target"] for c in ids]
        out.append(dict(entry=e, ids=list(range(e["n"])), target=target, type=q.type, id=ex["id"], family=ex["family"]))
    return out, dropped


def batches(its, budget, rng):
    """Micro-batches of whole questions; (pairs x longest pair) stays under budget, length-bucketed within 128."""
    order = list(range(len(its))); rng.shuffle(order); bs = []
    for start in range(0, len(order), 128):
        cur, width, n = [], 0, 0
        for i in sorted(order[start:start + 128], key=lambda i: its[i]["entry"]["length"]):
            pairs, w = its[i]["entry"]["n"], its[i]["entry"]["length"]
            if cur and ((n + pairs) * max(width, w) > budget or len(cur) >= 8):
                bs.append(cur); cur, n, width = [], 0, 0
            cur.append(i); n += pairs; width = max(width, w)
        if cur:
            bs.append(cur)
    rng.shuffle(bs)
    return bs


@torch.no_grad()
def validate(sc, data, budget):
    sc.model.eval(); loss = correct = 0
    for b in batches(data, budget, random.Random(0)):
        chunk = [data[i] for i in b]
        s = sc.forward_entries([x["entry"] for x in chunk]).float()
        loss += grouped_loss(s, chunk).item(); k = 0
        for it in chunk:
            n = len(it["ids"]); correct += question_correct(s[k:k + n].tolist(), it); k += n
    return dict(loss=loss / len(data), accuracy=correct / len(data), n=len(data))


def train(sc, args, out):
    from peft import LoraConfig, get_peft_model
    torch.manual_seed(13); rng = random.Random(13)
    cfg = DEFAULTS | dict(train_files=["data/hf.jsonl", "data/synthetic.jsonl", "data/hardcases_nb.jsonl"],
                          val_files=["data/hf.jsonl", "data/synthetic.jsonl", "data/eval.jsonl", "data/hardcases.jsonl"],
                          max_train_per_family=1600, cap_exempt_families=R2, max_val_questions=1200,
                          max_train_questions=args.train_limit)
    train_ex, val_ex = select_data(cfg, rng)
    before = sc.max_length; sc.max_length = args.train_max_len
    tr, dropped = items(sc, train_ex); va, vd = items(sc, val_ex); sc.max_length = before
    available = {n.rsplit(".", 1)[-1] for n, m in sc.model.named_modules() if isinstance(m, torch.nn.Linear)}
    targets = sorted(set(LINEAR) & available)
    sc.model = get_peft_model(sc.model, LoraConfig(r=args.lora_r, lora_alpha=2 * args.lora_r, lora_dropout=0.05,
                                                    target_modules=targets, bias="none"))
    sc.model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    params = [p for p in sc.model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(params, lr=2e-4, weight_decay=0.01)
    schedule = batches(tr, args.batch_tokens, rng); ga = args.grad_accum
    steps = math.ceil(len(schedule) / ga) * args.epochs
    warm = max(1, int(0.05 * steps))
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: min((s + 1) / warm, max(0.0, (steps - s) / max(1, steps - warm))))
    pair_tokens = sum(it["entry"]["n"] * it["entry"]["length"] for it in tr)
    meta = dict(model=sc.meta, config=cfg, recipe="tree_4b_instruct_r2x64 data and LoRA rank; full-sequence training",
                train_max_len=args.train_max_len, seed=13, epochs=args.epochs, lr=2e-4, weight_decay=0.01,
                batch_tokens=args.batch_tokens, grad_accum=ga, lora=dict(r=args.lora_r, alpha=2 * args.lora_r, targets=targets),
                trainable=sum(p.numel() for p in params), train_questions=len(tr), val_questions=len(va),
                train_pair_tokens=pair_tokens, dropped_train=len(dropped), dropped_val=len(vd),
                train_ids_sha=hashlib.sha256(json.dumps([i["id"] for i in tr]).encode()).hexdigest(),
                data={p: sha256_file(p) for p in set(cfg["train_files"] + cfg["val_files"])},
                versions=dict(torch=torch.__version__, gpu=torch.cuda.get_device_name()), log=[])
    save(out / "train_manifest.json", meta)
    print("TRAIN", {k: meta[k] for k in ["train_questions", "dropped_train", "trainable", "train_pair_tokens"]}, "steps", steps, flush=True)
    best, step, start = float("inf"), 0, time.perf_counter()

    def checkpoint():
        nonlocal best
        v = validate(sc, va, args.batch_tokens)
        meta["log"].append(dict(step=step, validation=v, wall_s=time.perf_counter() - start)); print("VALIDATION", step, v, flush=True)
        sc.model.save_pretrained(out / "adapter_last")
        if v["loss"] < best:
            best = v["loss"]; sc.model.save_pretrained(out / "adapter"); meta["best"] = dict(step=step, **v)
        save(out / "train_progress.json", meta)

    checkpoint()
    for epoch in range(args.epochs):
        if epoch:
            schedule = batches(tr, args.batch_tokens, rng)
        for b0 in range(0, len(schedule), ga):
            chunks = schedule[b0:b0 + ga]; nq = sum(len(b) for b in chunks)
            sc.model.train(); total = 0.0; opt.zero_grad(set_to_none=True)
            for b in chunks:
                its = [tr[i] for i in b]
                loss = grouped_loss(sc.forward_entries([x["entry"] for x in its]).float(), its) / nq
                if not torch.isfinite(loss):
                    raise FloatingPointError("nonfinite loss")
                loss.backward(); total += float(loss.detach())
            norm = torch.nn.utils.clip_grad_norm_(params, 1.0)
            if not torch.isfinite(norm):
                raise FloatingPointError("nonfinite gradients")
            if step == 0 and float(norm) == 0:
                raise RuntimeError("no adapter gradient")
            opt.step(); sched.step(); step += 1
            if step % 10 == 0:
                el = time.perf_counter() - start
                print("STEP", step, "/", steps, "loss", round(total, 4), "elapsed_s", round(el), "eta_s", round(el / step * (steps - step)), flush=True)
            if step % args.eval_every == 0 and step < steps:
                checkpoint()
    checkpoint(); meta["steps"] = step; meta["wall_s"] = time.perf_counter() - start
    save(out / "train_meta.json", meta)
    return meta


def bench(sc, out, repeats=10):
    rows = []
    for n, q, c, kind in [(512, 1, 3, "multiclass"), (512, 16, 3, "multiclass"), (2048, 1, 3, "multiclass"),
                          (2048, 16, 3, "multiclass"), (2048, 16, 1, "binary"), (8192, 1, 3, "multiclass"), (8192, 16, 3, "multiclass")]:
        req = benchmark.make_request(sc.tokenizer, n, q, c, kind)
        try:
            classify(sc, req); torch.cuda.synchronize(); torch.cuda.reset_peak_memory_stats(); times = []
            for _ in range(repeats):
                t = time.perf_counter(); classify(sc, req); torch.cuda.synchronize(); times.append(1e3 * (time.perf_counter() - t))
            row = dict(state_tokens=n, questions=q, candidates=c, type=kind, e2e_ms_p50=statistics.median(times),
                       peak_mb=torch.cuda.max_memory_allocated() / 2 ** 20, raw_ms=times)
        except torch.OutOfMemoryError:
            gc.collect(); torch.cuda.empty_cache(); row = dict(state_tokens=n, questions=q, candidates=c, status="OOM")
        rows.append(row); print("BENCH", n, q, c, row.get("e2e_ms_p50", row.get("status")), flush=True)
        save(out / "bench.json", dict(meta=sc.meta, gpu=torch.cuda.get_device_name(), rows=rows))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("name", choices=["qwen35", "qwen35_4b"])
    ap.add_argument("--stage", choices=["check", "train", "eval", "bench"], required=True)
    ap.add_argument("--tag", default="")
    ap.add_argument("--adapter")
    ap.add_argument("--lora-r", type=int, default=64)
    ap.add_argument("--batch-tokens", type=int, default=8192)
    ap.add_argument("--grad-accum", type=int, default=4)
    ap.add_argument("--train-max-len", type=int, default=2048)
    ap.add_argument("--eval-every", type=int, default=150)
    ap.add_argument("--epochs", type=int, default=1)
    ap.add_argument("--train-limit", type=int)
    ap.add_argument("--sets", default="test,eval2")
    args = ap.parse_args()
    run = args.name + args.tag
    out, report = Path("runs") / run, Path("reports") / run
    sc = ChallengerScorer(args.name, adapter=args.adapter)
    if args.stage == "check":  # forked-cache inference vs full sequences, on the example request and a 1K-token one
        reqs = [json.load(open("examples/request.json")), benchmark.make_request(sc.tokenizer, 1024, 2, 3, "multiclass")]
        from personal_jev.schemas import parse_request
        for raw in reqs:
            r = parse_request(raw); es = [sc.entry(r.state, q) for q in r.questions]
            with torch.no_grad():
                a, b = sc.shared_entries(es).float(), sc.forward_entries(es).float()
            d = float((a - b).abs().max()); print("CHECK shared vs full max |diff|", round(d, 4), "scores", [round(x, 3) for x in a.tolist()], flush=True)
            if not torch.isfinite(a).all() or d > 0.5:
                raise SystemExit(f"forked cache disagrees with full sequences: {d}")
    elif args.stage == "train":
        train(sc, args, out)
    elif args.stage == "eval":
        for s in args.sets.split(","):
            files, splits = (["data/eval2.jsonl"], None) if s == "eval2" else (["data/hf.jsonl", "data/eval.jsonl"], [s])
            r = evaluate.run(sc, files, splits, out_dir=report / s)
            print("EVAL", run, s, round(r["metrics"]["question_accuracy"], 4), flush=True)
    else:
        bench(sc, report)
    print("COMPLETE", run, args.stage, flush=True)
