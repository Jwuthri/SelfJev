"""Training for the custom shared-state classifier (custom.py): the new modules first, then the backbone too.

Stage A (warm-up, `stage_a_steps`): backbone frozen and run without autograd; train the projections,
cross-attention blocks, norms and heads. Stage B: keep training them while adapting the shared backbone with
LoRA (default) or full fine-tuning, end to end through one loss. The state and candidate passes share the
backbone, so both send gradients to the same weights. backbone="frozen" never leaves Stage A (ablation).
init_from: start from another run's checkpoint (its new modules and feature standardization), e.g. a finished
frozen run as Stage A; stage_a_steps=0 then begins Stage B at once.

Loss = train.grouped_loss on the custom heads' raw logits: BCEWithLogits per binary/multilabel question (mean
over its own labels), CrossEntropy over each multiclass question's own candidates; every question weighs the
same. Micro-batches hold whole states with all their questions: each state is encoded once per micro-batch and
stays in the autograd graph. Nothing is cached across optimizer steps.
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
from safetensors.torch import load_file
from transformers import AutoModel, AutoTokenizer

from .custom import (ARCH, CustomScorer, SharedStateClassifier, candidate_texts, checkpoint_sha, count_params, format_config,
                     save_checkpoint, state_text)
from .data import sha256_file
from .model import MODEL_ID, MODEL_REVISION, default_device, sync
from .schemas import parse_question
from .train import grouped_loss, hardware, lora_targets, question_correct, select_data, shuffle_candidates

DEFAULTS = {
    "train_files": ["data/hf.jsonl"], "val_files": ["data/hf.jsonl"], "out_dir": "runs/custom", "seed": 13, "device": None,
    "dtype": "bfloat16", "max_state_length": 2048, "max_candidate_length": 256, "max_batch_tokens": 8192, "grad_accum": 2,
    "epochs": 1, "max_steps": None, "backbone": "lora", "stage_a_steps": 60, "lr_new": 1e-3, "lr_backbone": 2e-4,
    "warmup_steps": 20, "weight_decay": 0.01, "max_grad_norm": 1.0, "gradient_checkpointing": True, "eval_every": 50,
    "max_val_questions": 800, "max_train_questions": None, "max_train_per_family": None, "arch": {}, "standardize_sample": 512,
    "init_from": None, "select_by": "loss",  # checkpoint selection on validation: "loss" or "question_accuracy"
    "lora": {"r": 16, "alpha": 32, "dropout": 0.05, "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj"]},
}


def encode_items(tokenizer, examples, max_state, max_cand):
    """-> (items, state token lists, dropped). Items: one per question, candidate token ids in "ids" (as in train.py)
    and the index of its state; identical states share one entry. Overlength questions are dropped and counted."""
    tok = lambda xs: tokenizer(xs, add_special_tokens=False, split_special_tokens=True)["input_ids"]
    keys, texts, per_q = {}, [], []
    for ex in examples:
        q = parse_question({"id": "q", **ex["question"]})
        s = keys.setdefault(state_text(ex["state"]), len(keys))
        per_q.append((ex, q, s, len(texts)))
        texts += candidate_texts(q)
    cand_ids, states = tok(texts), tok(list(keys))
    items, dropped = [], Counter()
    for ex, q, s, k in per_q:
        ids = cand_ids[k:k + (len(q.candidates) or 1)]
        if len(states[s]) > max_state or max(map(len, ids)) > max_cand:
            dropped[ex["family"]] += 1
            continue
        cids = [c.id for c in q.candidates]
        target = {"binary": lambda t: t, "multiclass": cids.index, "multilabel": lambda t: [c in t for c in cids]}[q.type](ex["target"])
        items.append({"id": ex["id"], "family": ex["family"], "type": q.type, "state": s, "ids": ids, "target": target})
    return items, states, dict(dropped)


def micro_batches(items, states, max_batch_tokens, rng, bucket=256):
    """Whole states (with all their questions) per micro-batch, length-bucketed; padded backbone tokens
    (states + candidates) stay under max_batch_tokens unless one state alone exceeds it."""
    groups = {}
    for i, it in enumerate(items):
        groups.setdefault(it["state"], []).append(i)
    keys = list(groups)
    rng.shuffle(keys)
    out = []
    for c in range(0, len(keys), bucket):
        cur, ns, ls, nc, lc = [], 0, 0, 0, 0
        for k in sorted(keys[c:c + bucket], key=lambda k: len(states[k])):
            cl = [len(x) for i in groups[k] for x in items[i]["ids"]]
            n = (ns + 1, max(ls, len(states[k])), nc + len(cl), max(lc, *cl))
            if cur and n[0] * n[1] + n[2] * n[3] > max_batch_tokens:
                out.append(cur)
                cur, n = [], (1, len(states[k]), len(cl), max(cl))
            cur += groups[k]
            ns, ls, nc, lc = n
        if cur:
            out.append(cur)
    rng.shuffle(out)
    return out


def forward_items(model, items, states, max_batch_tokens):
    """Flat scores for the items' candidates, in item order; each distinct state is encoded once."""
    local, state_ids, cand_ids, owner, mc = {}, [], [], [], []
    for it in items:
        if it["state"] not in local:
            local[it["state"]] = len(state_ids)
            state_ids.append(states[it["state"]])
        cand_ids += it["ids"]
        owner += [local[it["state"]]] * len(it["ids"])
        mc += [it["type"] == "multiclass"] * len(it["ids"])
    return model(state_ids, cand_ids, owner, mc, max_batch_tokens)


@torch.no_grad()
def score_items(model, items, states, max_batch_tokens):
    """Per-item score lists (eval mode, deterministic batching)."""
    model.eval()
    out = [None] * len(items)
    for b in micro_batches(items, states, max_batch_tokens, random.Random(0)):
        s, k = forward_items(model, [items[i] for i in b], states, max_batch_tokens).tolist(), 0
        for i in b:
            out[i], k = s[k:k + len(items[i]["ids"])], k + len(items[i]["ids"])
    return out


def validate(model, items, states, max_batch_tokens):
    scores = score_items(model, items, states, max_batch_tokens)
    loss = grouped_loss(torch.tensor([v for s in scores for v in s]), items).item() / len(items)
    by_type = Counter()
    for s, it in zip(scores, items):
        by_type[it["type"], question_correct(s, it)] += 1
    correct = sum(v for (t, ok), v in by_type.items() if ok)
    acc = {t: by_type[t, True] / (by_type[t, True] + by_type[t, False]) for t in ("binary", "multiclass", "multilabel")
           if by_type[t, True] + by_type[t, False]}
    return {"loss": loss, "question_accuracy": correct / len(items), "accuracy_by_type_at_T1_t0.5": acc}, scores


def build(cfg):
    """Backbone (+ zero-initialised LoRA, frozen until Stage B) and freshly initialised new modules."""
    if cfg["backbone"] not in ("lora", "full", "frozen"):
        raise ValueError("backbone must be lora | full | frozen")
    if cfg["backbone"] == "full" and cfg["dtype"] != "float32":
        raise ValueError("full fine-tuning keeps fp32 weights for AdamW; set dtype=float32")
    tok = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION)
    backbone = AutoModel.from_pretrained(MODEL_ID, revision=MODEL_REVISION, dtype=getattr(torch, cfg["dtype"]))
    linear = lora_targets(backbone, cfg["lora"]["target_modules"]) if cfg["backbone"] == "lora" else None
    if cfg["backbone"] == "lora":
        lc = cfg["lora"]
        backbone = get_peft_model(backbone, LoraConfig(r=lc["r"], lora_alpha=lc["alpha"], lora_dropout=lc["dropout"],
                                                       target_modules=lc["target_modules"], bias="none"))
    backbone.requires_grad_(False)
    model = SharedStateClassifier(backbone, tok.pad_token_id, cfg["arch"])
    return tok, model, linear


def backbone_params(model, mode):
    return [p for n, p in model.backbone.named_parameters() if mode == "full" or (mode == "lora" and "lora_" in n)]


def start_stage_b(model, cfg):
    for p in backbone_params(model, cfg["backbone"]):
        p.requires_grad_(True)
    model.backbone_grad = True
    if cfg["gradient_checkpointing"]:
        model.backbone.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})


def train(config_path=None, **overrides):
    cfg = DEFAULTS | (json.loads(Path(config_path).read_text()) if config_path else {}) | overrides
    cfg["lora"], cfg["arch"] = DEFAULTS["lora"] | cfg.get("lora", {}), ARCH | cfg.get("arch", {})
    out, mode = Path(cfg["out_dir"]), cfg["backbone"]
    out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(cfg["seed"])
    torch.manual_seed(cfg["seed"])
    t_start = time.perf_counter()
    device = cfg["device"] or default_device()

    tok, model, linear = build(cfg)
    model.to(device)
    train_ex, val_ex = select_data(cfg, rng)
    train_items, train_states, dropped_train = encode_items(tok, train_ex, cfg["max_state_length"], cfg["max_candidate_length"])
    val_items, val_states, dropped_val = encode_items(tok, val_ex, cfg["max_state_length"], cfg["max_candidate_length"])
    if cfg["init_from"]:  # new modules + standardization buffers from an earlier run (e.g. a finished Stage A)
        missing, unexpected = model.load_state_dict(load_file(Path(cfg["init_from"]) / "modules.safetensors"), strict=False)
        if unexpected or not all(k.startswith("backbone.") for k in missing):
            raise ValueError(f"init_from {cfg['init_from']}: module mismatch {unexpected[:3]} {missing[:3]}")
        std_info = {"init_from": cfg["init_from"], "checkpoint_sha": checkpoint_sha(cfg["init_from"])}
    else:
        sample = random.Random(cfg["seed"]).sample(train_items, min(cfg["standardize_sample"], len(train_items)))
        std_info = model.fit_standardization([train_states[k] for k in sorted({it["state"] for it in sample})],
                                             [x for it in sample for x in it["ids"]], cfg["max_batch_tokens"])
    print(f"feature standardization: {std_info}", flush=True)
    per_epoch = math.ceil(len(micro_batches(train_items, train_states, cfg["max_batch_tokens"], random.Random(0))) / cfg["grad_accum"])
    total = cfg["max_steps"] or per_epoch * cfg["epochs"]
    stage_a = total if mode == "frozen" else min(cfg["stage_a_steps"], total)
    warm = max(1, cfg["warmup_steps"])
    decay = lambda s, start: min((s - start + 1) / warm, max(0.0, (total - s) / max(1, total - start - warm)))
    new_p, bb_p = model.new_parameters(), backbone_params(model, mode)
    groups = [{"params": new_p, "lr": cfg["lr_new"], "weight_decay": cfg["weight_decay"]}]
    lambdas = [lambda s: decay(s, 0)]
    if bb_p:  # frozen (requires_grad False, no grads) until Stage B; AdamW skips parameters without grads
        groups.append({"params": bb_p, "lr": cfg["lr_backbone"], "weight_decay": 0.0})
        lambdas.append(lambda s: 0.0 if s < stage_a else decay(s, stage_a))
    opt = torch.optim.AdamW(groups)
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambdas)
    params = count_params(model)
    params |= {"stage_a_trainable": sum(p.numel() for p in new_p), "stage_b_trainable": sum(p.numel() for p in new_p + bb_p)}
    print(f"backbone={mode}; new modules {params['new_modules']:,} params {params['new_by_module']}; backbone {params['backbone']:,}; "
          f"trainable stage A {params['stage_a_trainable']:,} / stage B {params['stage_b_trainable']:,}"
          + (f"; LoRA on {cfg['lora']['target_modules']} (linear modules: {linear})" if linear else ""), flush=True)
    print(f"train questions {len(train_items)} over {len(train_states)} states (dropped overlength {dropped_train}), "
          f"val {len(val_items)}; {total} optimizer steps ({per_epoch}/epoch), stage A {stage_a}", flush=True)

    ck_config = {"base": {"model": MODEL_ID, "revision": MODEL_REVISION}, "backbone_mode": mode,
                 "lora": cfg["lora"] if mode == "lora" else None, "train_dtype": cfg["dtype"],
                 "tokenizer": {"class": type(tok).__name__, "pad_token_id": tok.pad_token_id}}
    if cfg["select_by"] not in ("loss", "question_accuracy"):
        raise ValueError("select_by must be loss | question_accuracy")
    sign = 1 if cfg["select_by"] == "loss" else -1  # minimise loss, maximise accuracy
    log, best, ref, step, seen = [], {"step": -1, cfg["select_by"]: sign * math.inf}, None, 0, 0
    reload_items = val_items[:64]

    def evaluate(tag):
        nonlocal best, ref
        v, _ = validate(model, val_items, val_states, cfg["max_batch_tokens"])
        log.append({"step": step, "stage": tag, "val": v})
        print(f"step {step} ({tag}) val {v}", flush=True)
        if (step > 0 or cfg["init_from"]) and sign * v[cfg["select_by"]] < sign * best[cfg["select_by"]]:  # random step-0 heads: never saved
            best = {"step": step, "stage": tag, **v, "checkpoint_sha": save_checkpoint(model, out / "checkpoint", ck_config)}
            ref = [x for s in score_items(model, reload_items, val_states, cfg["max_batch_tokens"]) for x in s]

    evaluate("init" if cfg["init_from"] else "init (random new modules)")
    if stage_a == 0 and mode != "frozen":
        start_stage_b(model, cfg)
    window, t_last, done = [], time.perf_counter(), False
    for epoch in range(cfg["epochs"] if not cfg["max_steps"] else 10**9):
        batches = micro_batches(train_items, train_states, cfg["max_batch_tokens"], rng)
        for g in range(0, len(batches), cfg["grad_accum"]):
            stage = "A" if step < stage_a else "B"
            group, nq = batches[g:g + cfg["grad_accum"]], sum(len(b) for b in batches[g:g + cfg["grad_accum"]])
            model.train()
            model.backbone.train(stage == "B")  # Stage A: backbone in eval mode and without autograd
            step_loss = 0.0
            for b in group:
                items = [shuffle_candidates(train_items[i], rng) for i in b]
                loss = grouped_loss(forward_items(model, items, train_states, cfg["max_batch_tokens"]), items) / nq
                loss.backward()
                step_loss += loss.item()
            live = [p for p in new_p + (bb_p if stage == "B" else []) if p.requires_grad]
            if not all(p.grad is not None and torch.isfinite(p.grad).all() for p in live):
                raise FloatingPointError(f"missing or non-finite gradients at step {step} (stage {stage})")
            gnorm = torch.nn.utils.clip_grad_norm_(live, cfg["max_grad_norm"]).item()
            opt.step()
            sched.step()
            opt.zero_grad(set_to_none=True)
            step, seen = step + 1, seen + nq
            window.append(step_loss)
            if step % 10 == 0:
                sync(device)
                dt, t_last = time.perf_counter() - t_last, time.perf_counter()
                lrs = [f"{x:.2e}" for x in sched.get_last_lr()]
                print(f"step {step}/{total} stage {stage} epoch {epoch} loss {sum(window) / len(window):.4f} gnorm {gnorm:.3f} "
                      f"lr {lrs} {10 / dt:.2f} steps/s", flush=True)
                log.append({"step": step, "stage": stage, "train_loss": sum(window) / len(window), "grad_norm": gnorm, "questions_seen": seen})
                window = []
            if step == stage_a and mode != "frozen":
                evaluate("end of stage A")
                start_stage_b(model, cfg)
                print(f"stage B: {mode} backbone adaptation starts", flush=True)
            elif step % cfg["eval_every"] == 0 or step == total:
                evaluate(stage)
            if step == total:
                done = True
                break
        if done:
            break
    if log[-1].get("step") != step or "val" not in log[-1]:  # data ran out before `total`: validate the end
        evaluate("end of data")

    # Reload the complete checkpoint from disk (new modules + adapter/backbone + config) and compare scores
    # with the same weights in memory, same dtype and batching.
    reloaded = CustomScorer(out / "checkpoint", device=device, dtype=cfg["dtype"]).model
    again = [x for s in score_items(reloaded, reload_items, val_states, cfg["max_batch_tokens"]) for x in s]
    reload_diff = max(abs(a - b) for a, b in zip(ref, again))
    del reloaded
    meta = {
        "config": cfg, "base": ck_config["base"], "format": format_config(), "params": params, "standardization": std_info,
        "data": {"train_files": [{"path": p, "sha256": sha256_file(p)} for p in cfg["train_files"]],
                 "val_files": [{"path": p, "sha256": sha256_file(p)} for p in cfg["val_files"]],
                 "train_questions": len(train_items), "train_states": len(train_states), "val_questions": len(val_items),
                 "train_by_family": dict(Counter(it["family"] for it in train_items)),
                 "train_by_type": dict(Counter(it["type"] for it in train_items)),
                 "dropped_overlength": {"train": dropped_train, "val": dropped_val}},
        "best": best, "steps": step, "stage_a_steps": stage_a, "log": log,
        "reload_check": {"questions": len(reload_items), "max_abs_score_diff": reload_diff}, "hardware": hardware(device),
        "versions": {"torch": torch.__version__, "transformers": transformers.__version__, "peft": peft.__version__},
        "wall_s": time.perf_counter() - t_start}
    (out / "train_meta.json").write_text(json.dumps(meta, indent=1))
    (out / "checkpoint" / "train_meta.json").write_text(json.dumps(meta, indent=1))
    print(f"best step {best['step']} ({best.get('stage')}) by {cfg['select_by']}: val loss {best['loss']:.4f}, "
          f"question accuracy {best['question_accuracy']:.4f}; reload max |diff| {reload_diff:.2e}; "
          f"checkpoint {out / 'checkpoint'}", flush=True)
    return meta
