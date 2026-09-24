"""LoRA training for the jina-reranker-v3.5 backend (jina.py), with train.py's data selection, losses and schedule.

Each micro-batch is a set of contexts, one per state (all of that state's questions in the batch, at most
`max_passages` passages per context), scored in one forward pass; the loss is train.grouped_loss over the passage
logits. Trained: LoRA on the attention projections, the model's projector (saved with the adapter as
modules_to_save) and the two head scalars (adapter/jina_head.json). Candidate and question order inside a context
is shuffled every step because passages attend to earlier passages.
"""
import json
import math
import random
import time
from collections import Counter
from pathlib import Path

import peft
import torch
import transformers
from peft import LoraConfig, get_peft_model

from .data import sha256_file
from .model import default_device, sync
from .schemas import parse_question
from .train import DEFAULTS as STOCK_DEFAULTS
from .train import grouped_loss, hardware, lora_targets, question_correct, select_data, shuffle_candidates
from .jina import JINA, Encoder, JinaModel, JinaScorer, format_config, load_core, passage_answers

DEFAULTS = STOCK_DEFAULTS | {
    "model_id": JINA[0], "revision": JINA[1], "out_dir": "runs/jina", "dtype": "bfloat16",
    "max_length": 8192, "max_batch_tokens": 16384, "grad_accum": 2, "epochs": 1, "lr": 2e-4, "head_lr": 1e-2, "warmup_ratio": 0.05,
    "eval_every": 50, "max_val_questions": 1200, "max_train_per_family": 1600, "query_tail": 1024, "max_passages": 32,
    "train_projector": True}


def encode_items(enc, examples, max_length):
    """-> (items, states, dropped). Item: one question with its passage ids ("ids", one list per candidate) and target;
    "state" indexes states. A question whose context alone (state + tail + its passages) exceeds max_length is dropped."""
    keys, per = {}, []
    for ex in examples:
        q = parse_question({"id": "q", **ex["question"]})
        per.append((ex, q, keys.setdefault(ex["state"], len(keys))))
    states = enc.user(list(keys))
    q_ids = enc.user([q.instruction for _, q, _ in per])
    a_ids = iter(enc.user([a for _, q, _ in per for a in passage_answers(q)]))
    items, dropped = [], Counter()
    for (ex, q, s), qi in zip(per, q_ids):
        passages = [enc.passage(qi, next(a_ids)) for _ in passage_answers(q)]
        n = len(passages)
        if len(states[s]) + min(len(states[s]), enc.query_tail) + sum(map(len, passages)) + enc.overhead(n) > max_length:
            dropped[ex["family"]] += 1
            continue
        cids = [c.id for c in q.candidates]
        target = {"binary": lambda t: t, "multiclass": cids.index, "multilabel": lambda t: [c in t for c in cids]}[q.type](ex["target"])
        items.append({"id": ex["id"], "family": ex["family"], "type": q.type, "state": s, "ids": passages, "target": target, "candidate_ids": cids})
    return items, states, dict(dropped)


def context_len(enc, state_ids, items):
    n = sum(len(it["ids"]) for it in items)
    return len(state_ids) + min(len(state_ids), enc.query_tail) + sum(len(p) for it in items for p in it["ids"]) + enc.overhead(n)


def chunks_by_state(items, enc, states, max_length, max_passages):
    """Contexts = (state index, [item indexes]) with <= max_passages passages and <= max_length tokens each."""
    groups = {}
    for i, it in enumerate(items):
        groups.setdefault(it["state"], []).append(i)
    out = []
    for s, idx in groups.items():
        cur, n = [], 0
        for i in idx:
            k = len(items[i]["ids"])
            if cur and (n + k > max_passages or context_len(enc, states[s], [items[j] for j in cur + [i]]) > max_length):
                out.append((s, cur))
                cur, n = [], 0
            cur, n = cur + [i], n + k
        out.append((s, cur))
    return out


def micro_batches(chunks, enc, states, items, max_batch_tokens, rng, bucket=256):
    """Contexts length-bucketed into micro-batches whose padded tokens stay under max_batch_tokens."""
    order = list(range(len(chunks)))
    rng.shuffle(order)
    size = {c: context_len(enc, states[chunks[c][0]], [items[i] for i in chunks[c][1]]) for c in order}
    out = []
    for b in range(0, len(order), bucket):
        cur, n, w = [], 0, 0
        for c in sorted(order[b:b + bucket], key=size.__getitem__):
            if cur and (n + 1) * max(w, size[c]) > max_batch_tokens:
                out.append(cur)
                cur, n, w = [], 0, 0
            cur, n, w = cur + [c], n + 1, max(w, size[c])
        if cur:
            out.append(cur)
    rng.shuffle(out)
    return out


def build(enc, states, items, chunk, rng=None):
    """-> (context, ordered items). rng: shuffle question order and candidate order (training)."""
    s, idx = chunk
    ordered = [items[i] for i in idx]
    if rng:
        rng.shuffle(ordered)
        ordered = [shuffle_candidates(it, rng) for it in ordered]
    return enc.context(states[s], [p for it in ordered for p in it["ids"]]), ordered


@torch.no_grad()
def score_items(model, enc, states, items, cfg, progress=None):
    model.core.eval()
    chunks = chunks_by_state(items, enc, states, cfg["max_length"], cfg["max_passages"])
    out, batches = [None] * len(items), micro_batches(chunks, enc, states, items, cfg["max_batch_tokens"], random.Random(0))
    for bi, b in enumerate(batches):
        built = [build(enc, states, items, chunks[c]) for c in b]
        s, k = model.logits([ctx for ctx, _ in built]).tolist(), 0
        for (_, ordered), c in zip(built, b):
            for i, it in zip(chunks[c][1], ordered):
                out[i], k = s[k:k + len(it["ids"])], k + len(it["ids"])
        if progress and ((bi + 1) % 10 == 0 or bi + 1 == len(batches)):
            progress(bi + 1, len(batches))
    return out


def validate(model, enc, states, items, cfg):
    scores = score_items(model, enc, states, items, cfg)
    loss = grouped_loss(torch.tensor([v for s in scores for v in s]), items).item() / len(items)
    by = Counter((it["type"], question_correct(s, it)) for s, it in zip(scores, items))
    acc = {t: by[t, True] / (by[t, True] + by[t, False]) for t in ("binary", "multiclass", "multilabel") if by[t, True] + by[t, False]}
    return {"loss": loss, "question_accuracy": sum(v for (t, ok), v in by.items() if ok) / len(items), "accuracy_by_type_at_T1_t0.5": acc}, scores


def train(config_path=None, **overrides):
    cfg = DEFAULTS | (json.loads(Path(config_path).read_text()) if config_path else {}) | overrides
    cfg["lora"] = DEFAULTS["lora"] | cfg.get("lora", {})
    out = Path(cfg["out_dir"])
    out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(cfg["seed"])
    torch.manual_seed(cfg["seed"])
    t_start, device = time.perf_counter(), cfg["device"] or default_device()

    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(cfg["model_id"], revision=cfg["revision"], trust_remote_code=True)
    enc = Encoder(tok, cfg["query_tail"])
    core = load_core(cfg["model_id"], cfg["revision"], cfg["dtype"])
    linear, lc = lora_targets(core, cfg["lora"]["target_modules"]), cfg["lora"]
    lm = get_peft_model(core, LoraConfig(r=lc["r"], lora_alpha=lc["alpha"], lora_dropout=lc["dropout"], target_modules=lc["target_modules"],
                                         bias="none", modules_to_save=["projector"] if cfg["train_projector"] else None))
    if cfg["gradient_checkpointing"]:
        lm.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
        lm.enable_input_require_grads()
    lm.to(device)
    model = JinaModel(lm.get_base_model(), tok.pad_token_id)
    trainable, total = lm.get_nb_trainable_parameters()
    print(f"{cfg['model_id']} jina listwise scorer, LoRA on {lc['target_modules']} (linear: {linear}), projector trained: "
          f"{cfg['train_projector']}; trainable {trainable:,} / {total:,} + 2 head scalars", flush=True)

    train_ex, val_ex = select_data(cfg, rng)
    train_items, train_states, dropped_train = encode_items(enc, train_ex, cfg["max_length"])
    val_items, val_states, dropped_val = encode_items(enc, val_ex, cfg["max_length"])
    (out / "selected_examples.json").write_text(json.dumps({"train": [it["id"] for it in train_items], "validation": [it["id"] for it in val_items]}))
    chunks = chunks_by_state(train_items, enc, train_states, cfg["max_length"], cfg["max_passages"])
    per_epoch = math.ceil(len(micro_batches(chunks, enc, train_states, train_items, cfg["max_batch_tokens"], random.Random(0))) / cfg["grad_accum"])
    total_steps = cfg["max_steps"] or per_epoch * cfg["epochs"]
    warmup = max(1, round(cfg["warmup_ratio"] * total_steps))
    params = [p for p in lm.parameters() if p.requires_grad]
    opt = torch.optim.AdamW([{"params": params, "lr": cfg["lr"]}, {"params": [model.scale, model.bias], "lr": cfg["head_lr"], "weight_decay": 0.0}],
                            weight_decay=cfg["weight_decay"])
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: min((s + 1) / warmup, max(0.0, (total_steps - s) / max(1, total_steps - warmup))))
    print(f"train questions {len(train_items)} over {len(train_states)} states / {len(chunks)} contexts (dropped {dropped_train}), "
          f"val {len(val_items)}; {total_steps} optimizer steps ({per_epoch}/epoch), warmup {warmup}", flush=True)

    # head init: the untrained model's median validation cosine maps to logit 0
    with torch.no_grad():
        model.scale.fill_(10.0)
        model.bias.zero_()
        v0 = [x for s in score_items(model, enc, val_states, val_items[:200], cfg) for x in s]
        model.bias.fill_(-float(torch.tensor(v0).median()))
    print(f"head init: scale {float(model.scale):.2f} bias {float(model.bias):.3f}", flush=True)

    def save():
        lm.save_pretrained(out / "adapter", save_embedding_layers=False)
        (out / "adapter/jina_head.json").write_text(json.dumps(model.head() | {"format_sha": enc.format["sha"], "query_tail": cfg["query_tail"]}, indent=2))

    log, best, ref, step, seen = [], {"step": -1, "loss": math.inf}, None, 0, 0
    reload_items = val_items[:64]

    def evaluate(tag):
        nonlocal best, ref
        v, _ = validate(model, enc, val_states, val_items, cfg)
        log.append({"step": step, "stage": tag, "val": v, "head": model.head()})
        print(f"step {step} ({tag}) val {v} head {model.head()}", flush=True)
        if v["loss"] < best["loss"]:
            best = {"step": step, **v}
            save()
            ref = [x for s in score_items(model, enc, val_states, reload_items, cfg) for x in s]

    evaluate("init (zero-initialized LoRA, head from median cosine)")
    window, t_last, done = [], time.perf_counter(), False
    for epoch in range(cfg["epochs"] if not cfg["max_steps"] else 10**9):
        batches = micro_batches(chunks, enc, train_states, train_items, cfg["max_batch_tokens"], rng)
        for g in range(0, len(batches), cfg["grad_accum"]):
            group = batches[g:g + cfg["grad_accum"]]
            nq = sum(len(chunks[c][1]) for b in group for c in b)
            lm.train()
            step_loss = 0.0
            for b in group:
                built = [build(enc, train_states, train_items, chunks[c], rng) for c in b]
                scores = model.logits([ctx for ctx, _ in built])
                loss = grouped_loss(scores, [it for _, ordered in built for it in ordered]) / nq
                loss.backward()
                step_loss += loss.item()
            if not all(p.grad is not None and torch.isfinite(p.grad).all() for p in params):
                raise FloatingPointError(f"missing or non-finite gradients at step {step}")
            gnorm = torch.nn.utils.clip_grad_norm_(params + [model.scale, model.bias], cfg["max_grad_norm"]).item()
            opt.step()
            sched.step()
            opt.zero_grad(set_to_none=True)
            step, seen = step + 1, seen + nq
            window.append(step_loss)
            if step % 10 == 0:
                sync(device)
                dt, t_last = time.perf_counter() - t_last, time.perf_counter()
                print(f"step {step}/{total_steps} epoch {epoch} loss {sum(window) / len(window):.4f} gnorm {gnorm:.3f} "
                      f"lr {sched.get_last_lr()[0]:.2e} {10 / dt:.2f} steps/s", flush=True)
                log.append({"step": step, "train_loss": sum(window) / len(window), "grad_norm": gnorm, "questions_seen": seen})
                window = []
            if step % cfg["eval_every"] == 0 or step == total_steps:
                evaluate("train")
            if step == total_steps:
                done = True
                break
        if done:
            break
    if log[-1].get("step") != step or "val" not in log[-1]:
        evaluate("end of data")

    del lm, model, core
    torch.cuda.empty_cache() if device == "cuda" else None
    re = JinaScorer(cfg["model_id"], cfg["revision"], adapter=out / "adapter", device=device, dtype=cfg["dtype"], max_length=cfg["max_length"])
    re_cfg = cfg | {"max_passages": cfg["max_passages"]}
    again = [x for s in score_items(re.model, re.enc, val_states, reload_items, re_cfg) for x in s]
    meta = {"config": cfg, "base": {"model": cfg["model_id"], "revision": cfg["revision"]}, "format": enc.format,
            "lora": lc | {"trainable_params": trainable, "total_params": total, "linear_modules_available": linear, "modules_to_save": ["projector"] if cfg["train_projector"] else []},
            "data": {"train_files": [{"path": p, "sha256": sha256_file(p)} for p in cfg["train_files"]],
                     "val_files": [{"path": p, "sha256": sha256_file(p)} for p in cfg["val_files"]],
                     "train_questions": len(train_items), "train_states": len(train_states), "train_contexts": len(chunks), "val_questions": len(val_items),
                     "train_by_family": dict(Counter(it["family"] for it in train_items)), "dropped_overlength": {"train": dropped_train, "val": dropped_val}},
            "best": best, "steps": step, "log": log, "head": re.model.head(),
            "reload_check": {"questions": len(reload_items), "max_abs_score_diff": max(abs(a - b) for a, b in zip(ref, again))},
            "hardware": hardware(device), "wall_s": time.perf_counter() - t_start,
            "versions": {"torch": torch.__version__, "transformers": transformers.__version__, "peft": peft.__version__},
            "adapter_sha256": sha256_file(out / "adapter/adapter_model.safetensors")}
    (out / "train_meta.json").write_text(json.dumps(meta, indent=1))
    print(f"best step {best['step']} val loss {best['loss']:.4f}; reload max |diff| {meta['reload_check']['max_abs_score_diff']:.2e}; "
          f"saved {out / 'adapter'}", flush=True)
    return meta
