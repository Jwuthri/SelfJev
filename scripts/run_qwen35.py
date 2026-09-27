"""Qwen3.5 (hybrid Gated DeltaNet + full attention) shared-document scorer: LoRA training and evals on one CUDA GPU.

Ported from the Codex challenger worktree (its run_challenger.py) and pointed at the round-2 recipe of
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

from selfjev import benchmark, evaluate, qwen35_tree
from selfjev.challengers import ChallengerScorer
from selfjev.classify import classify
from selfjev.data import sha256_file
from selfjev.model import InputTooLong
from selfjev.schemas import parse_question
from selfjev.train import DEFAULTS, grouped_loss, question_correct, select_data, shuffle_candidates
from selfjev.train_tree import group_by_state, trees_for
from selfjev.train_tree import micro_batches as tree_batches

R2 = ["r2_simple", "r2_hard", "r2_very_hard"]
R3 = ["r3_simple", "r3_hard", "r3_very_hard"]
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


@torch.no_grad()
def validate_tree(sc, data, roots, budget):
    sc.model.eval(); loss = correct = 0
    for b in tree_batches(data, roots, budget, random.Random(0)):
        chunk = group_by_state([data[i] for i in b])
        s = qwen35_tree.score(sc, trees_for(chunk, roots)).float()
        loss += grouped_loss(s, chunk).item(); k = 0
        for it in chunk:
            n = len(it["ids"]); correct += question_correct(s[k:k + n].tolist(), it); k += n
    return dict(loss=loss / len(data), accuracy=correct / len(data), n=len(data))


def train(sc, args, out):
    from peft import LoraConfig, get_peft_model
    torch.manual_seed(13); rng = random.Random(13)
    d = args.data_dir  # data/ova: options in the question; rebuild the untracked training copies first (docs/reproduce.md)
    r3 = [f"{d}/hardcases_r3.jsonl"] if args.r3 else []
    cfg = DEFAULTS | dict(train_files=[f"{d}/hf.jsonl", f"{d}/synthetic.jsonl", f"{d}/hardcases_nb.jsonl"] + r3,
                          val_files=[f"{d}/hf.jsonl", f"{d}/synthetic.jsonl", f"{d}/eval.jsonl", f"{d}/hardcases.jsonl"] + r3,
                          max_train_per_family=1600, cap_exempt_families=R2 + (R3 if args.r3 else []), max_val_questions=1200,
                          max_train_questions=args.train_limit)
    train_ex, val_ex = select_data(cfg, rng)
    if args.tree:  # shared-prefix tree (selfjev.qwen35_tree): the text once per state, so long texts fit
        tr, roots, dropped = qwen35_tree.encode_items(sc, train_ex, args.train_max_len)
        va, vroots, vd = qwen35_tree.encode_items(sc, val_ex, args.train_max_len)
        dropped, vd = [f for f, n in dropped.items() for _ in range(n)], [f for f, n in vd.items() for _ in range(n)]
    else:
        before = sc.max_length; sc.max_length = args.train_max_len
        tr, dropped = items(sc, train_ex); va, vd = items(sc, val_ex); sc.max_length = before
    available = {n.rsplit(".", 1)[-1] for n, m in sc.model.named_modules() if isinstance(m, torch.nn.Linear)}
    targets = sorted(set(LINEAR) & available)
    sc.model = get_peft_model(sc.model, LoraConfig(r=args.lora_r, lora_alpha=2 * args.lora_r, lora_dropout=0.05,
                                                    target_modules=targets, bias="none"))
    if not args.tree:  # the tree checkpoints its own layers (qwen35_tree.score)
        sc.model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    params = [p for p in sc.model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(params, lr=2e-4, weight_decay=0.01)
    make_schedule = (lambda: tree_batches(tr, roots, args.batch_tokens, rng)) if args.tree else (lambda: batches(tr, args.batch_tokens, rng))
    schedule = make_schedule(); ga = args.grad_accum
    steps = math.ceil(len(schedule) / ga) * args.epochs
    warm = max(1, int(0.05 * steps))
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: min((s + 1) / warm, max(0.0, (steps - s) / max(1, steps - warm))))
    pair_tokens = (sum(len(roots[s]) for s in {it["state"] for it in tr}) + sum(len(it["q"]) + sum(map(len, it["ids"])) for it in tr)
                   if args.tree else sum(it["entry"]["n"] * it["entry"]["length"] for it in tr))  # tree: every state once
    meta = dict(model=sc.meta, config=cfg, recipe="tree_4b_instruct_r2x64 data and LoRA rank; " + ("shared-prefix tree training (qwen35_tree)" if args.tree else "full-sequence training"), tree=args.tree, data_dir=args.data_dir, round3=args.r3,
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
        v = validate_tree(sc, va, vroots, args.batch_tokens) if args.tree else validate(sc, va, args.batch_tokens)
        meta["log"].append(dict(step=step, validation=v, wall_s=time.perf_counter() - start)); print("VALIDATION", step, v, flush=True)
        sc.model.save_pretrained(out / "adapter_last")
        if v["loss"] < best:
            best = v["loss"]; sc.model.save_pretrained(out / "adapter"); meta["best"] = dict(step=step, **v)
        save(out / "train_progress.json", meta)

    checkpoint()
    for epoch in range(args.epochs):
        if epoch:
            schedule = make_schedule()
        for b0 in range(0, len(schedule), ga):
            chunks = schedule[b0:b0 + ga]; nq = sum(len(b) for b in chunks)
            sc.model.train(); total = 0.0; opt.zero_grad(set_to_none=True)
            for b in chunks:
                if args.tree:
                    its = group_by_state([shuffle_candidates(tr[i], rng) for i in b])
                    s = qwen35_tree.score(sc, trees_for(its, roots))
                else:
                    its = [tr[i] for i in b]; s = sc.forward_entries([x["entry"] for x in its])
                loss = grouped_loss(s.float(), its) / nq
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


def tree_check(sc, args):
    """The tree vs full sequences on real training questions (bf16, fla kernels): scores, LoRA gradients, then the
    time and peak memory of one training micro-batch at --batch-tokens and of one 8K-token text. Raises on mismatch."""
    from peft import LoraConfig, get_peft_model
    rows = [r for f in ("hardcases_r3.jsonl", "hf.jsonl") for r in map(json.loads, open(f"{args.data_dir}/{f}")) if r["split"] == "train"]
    random.Random(0).shuffle(rows)
    its, roots, _ = qwen35_tree.encode_items(sc, rows[:400], args.train_max_len)
    size = lambda it: len(it["ids"]) * (len(roots[it["state"]]) + len(it["q"]) + max(map(len, it["ids"])))  # noqa: E731
    small = [it for it in its if size(it) <= 6000][:16]  # full-sequence tokens per question
    parts = [group_by_state([small[i] for i in b]) for b in tree_batches(small, roots, args.batch_tokens, random.Random(0))]
    small = [it for c in parts for it in c]  # training-sized micro-batches, in the tree's item order
    sc.model = get_peft_model(sc.model, LoraConfig(r=8, lora_alpha=16, lora_dropout=0.0, target_modules=LINEAR, bias="none"))
    for n, w in sc.model.named_parameters():  # nonzero B so every LoRA matrix gets a gradient
        if "lora_B" in n:
            torch.nn.init.normal_(w, std=1e-3)
    ex = {r["id"]: r for r in rows}
    full = lambda chunk: torch.cat([sc.forward_entries([sc.entry(ex[it["id"]]["state"], parse_question({"id": "q", **ex[it["id"]]["question"]}))])
                                   for it in chunk])  # noqa: E731
    with torch.no_grad():
        a, b = torch.cat([qwen35_tree.score(sc, trees_for(c, roots)).float() for c in parts]), full(small).float()
    d = float((a - b).abs().max())
    print("CHECK tree vs full: scores", len(a), "max |diff|", round(d, 4), flush=True)
    sc.model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})  # for the reference's memory;
    sc.model.train()  # HF checkpoints only in train mode; LoRA dropout is 0 here. The tree checkpoints its own layers.
    entry = lambda it: sc.entry(ex[it["id"]]["state"], parse_question({"id": "q", **ex[it["id"]]["question"]}))  # noqa: E731
    by_branch = lambda it: torch.cat([sc.forward_entries([dict(e, branches=[br], n=1)]) for e in [entry(it)] for br in e["branches"]])  # noqa: E731
    grads = {}
    for kind in ("tree", "full", "full, one branch at a time"):  # the last one: the precision noise floor of the reference
        sc.model.zero_grad()
        for c in (parts if kind == "tree" else [[it] for it in small]):  # the loss is a sum over questions
            s = qwen35_tree.score(sc, trees_for(c, roots)) if kind == "tree" else full(c) if kind == "full" else by_branch(c[0])
            grouped_loss(s.float(), c).backward()
        grads[kind] = torch.cat([w.grad.flatten().float() for n, w in sc.model.named_parameters() if w.grad is not None])
    cos = {k: float(torch.nn.functional.cosine_similarity(g, grads["full"], dim=0)) for k, g in grads.items() if k != "full"}
    rel = {k: float((g - grads["full"]).norm() / grads["full"].norm()) for k, g in grads.items() if k != "full"}
    print("CHECK LoRA gradients vs full sequences (", args.dtype, "): cosine", {k: round(v, 5) for k, v in cos.items()},
          "rel", {k: round(v, 4) for k, v in rel.items()}, flush=True)
    if not torch.isfinite(a).all() or d > 0.5 or cos["tree"] < min(0.999, cos["full, one branch at a time"] - 0.005):
        raise SystemExit("the tree disagrees with full sequences beyond the reference's own precision noise")
    long = [it for it in its if len(roots[it["state"]]) > 6000][:1]
    for name, chunk in (("micro-batch", group_by_state([its[i] for i in tree_batches(its, roots, args.batch_tokens, random.Random(1))[0]])),
                        ("8K text", long)):
        if not chunk:
            continue
        sc.model.zero_grad(); torch.cuda.synchronize(); torch.cuda.reset_peak_memory_stats(); t = time.perf_counter()
        trees = trees_for(chunk, roots)
        grouped_loss(qwen35_tree.score(sc, trees).float(), chunk).backward(); torch.cuda.synchronize()
        print("CHECK", name, len(chunk), "questions", sum(len(t["ids"]) for t in trees), "tokens", round(time.perf_counter() - t, 2), "s fwd+bwd",
              round(torch.cuda.max_memory_allocated() / 2 ** 30, 1), "GB peak", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("name", choices=["qwen35", "qwen35_4b"])
    ap.add_argument("--stage", choices=["check", "check-tree", "train", "eval", "bench"], required=True)
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
    ap.add_argument("--data-dir", default="data", help="data/ova: options listed in the question (same files, transformed)")
    ap.add_argument("--r3", action="store_true", help="add data/<dir>/hardcases_r3.jsonl, r3_* families uncapped")
    ap.add_argument("--dtype", default="bfloat16", help="float32 for an exactness check-tree")
    ap.add_argument("--tree", action="store_true", help="train with the shared-prefix tree (selfjev.qwen35_tree; "
                    "--train-max-len then bounds root + question + longest leaf); with eval / bench: score with it")
    args = ap.parse_args()
    run = args.name + args.tag
    out, report = Path("runs") / run, Path("reports") / run
    if args.tree and args.stage in ("eval", "bench"):  # serve with the training tree (qwen35_tree.TreeServer), LoRA merged
        sc = qwen35_tree.TreeServer(args.adapter)
    else:
        sc = ChallengerScorer(args.name, adapter=args.adapter, dtype=args.dtype)
    if args.stage == "check":  # forked-cache inference vs full sequences, on the example request and a 1K-token one
        reqs = [json.load(open("examples/request.json")), benchmark.make_request(sc.tokenizer, 1024, 2, 3, "multiclass")]
        from selfjev.schemas import parse_request
        for raw in reqs:
            r = parse_request(raw); es = [sc.entry(r.state, q) for q in r.questions]
            with torch.no_grad():
                a, b = sc.shared_entries(es).float(), sc.forward_entries(es).float()
            d = float((a - b).abs().max()); print("CHECK shared vs full max |diff|", round(d, 4), "scores", [round(x, 3) for x in a.tolist()], flush=True)
            if not torch.isfinite(a).all() or d > 0.5:
                raise SystemExit(f"forked cache disagrees with full sequences: {d}")
    elif args.stage == "check-tree":
        tree_check(sc, args)
    elif args.stage == "train":
        train(sc, args, out)
    elif args.stage == "eval":
        for s in args.sets.split(","):
            d = args.data_dir
            files, splits = ([f"{d}/{s}.jsonl"], None) if s in ("eval2", "eval_llm") else ([f"{d}/hf.jsonl", f"{d}/eval.jsonl"], [s])
            r = evaluate.run(sc, files, splits, out_dir=report / s)
            print("EVAL", run, s, round(r["metrics"]["question_accuracy"], 4), flush=True)
    else:
        bench(sc, report)
    print("COMPLETE", run, args.stage, flush=True)
