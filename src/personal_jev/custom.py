"""Custom shared-state classifier: Qwen3-Reranker-0.6B backbone + NEW candidate-to-state cross-attention + small heads.

  memory = LN(W_m · z(backbone(state)))                     [S, L, h]  each distinct state encoded once per call
  q      = W_c · z(backbone(task + question + answer))       [N, Lc, h] separate sequences, same backbone weights
  q      = q + Attn(LN(q), memory); q = q + FFN(LN(q))       x blocks   (NEW; candidates never attend to each other)
  score  = head(masked_mean(LN(q)))                          binary_head: binary + multilabel, choice_head: multiclass

The backbone is the reranker's transformer body with its stock causal mask, loaded without the vocabulary head:
no yes/no logits and no joint (state, candidate) sequence. z() is a fixed per-dimension standardization of its
last hidden states (mean/std fit once on training text, stored in the checkpoint): raw last-layer states share
one dominant direction (mean token cosine ~0.49), which drowns the token-specific signal the attention needs.
tied_init: the new modules are random, but W_c = W_m and, per block, Wq = Wk (random orthogonal) and Wo = Wv^T at
initialisation, so at step 0 each candidate token attends to the state tokens most similar to it in feature space
(a parameter-free MaxSim over these features already ranks candidates far above chance). Training unties them. Candidate tokens are packed per state
([S, all its candidates' tokens, h]), so K/V are projected once per state per block and a state is never copied
per candidate. Query rows are independent (cross-attention, per-token FFN/LN), so packing cannot mix candidates.
The new modules start untrained: without a trained checkpoint this is NOT a classifier.
"""
import hashlib
import json
import time
from collections import Counter
from pathlib import Path

import torch
import torch.nn.functional as F
from safetensors.torch import load_file, save_file
from torch import nn
from transformers import AutoModel, AutoTokenizer

from .data import sha256_file
from .model import MAX_CONTEXT, MODEL_ID, MODEL_REVISION, InputTooLong, default_device, length_batches
from .schemas import Question

FORMAT = "custom-v1"
STATE_TEMPLATE = "Document:\n{state}"
CANDIDATE_TEMPLATE = "Task: {type}\nQuestion: {instruction}\nProposed answer: {answer}"
BINARY_ANSWER = "Yes"  # binary p_yes = P(the Document supports answering the question "Yes")
# split_special_tokens: "<|im_end|>" typed inside a state is plain text, never a control token.
TOKENIZE = {"add_special_tokens": False, "split_special_tokens": True}
ARCH = {"h": 256, "heads": 8, "ffn": 1024, "blocks": 2, "head_width": 128, "dropout": 0.1, "pooling": "mean",
        "shared_head": False, "memory_norm": True, "standardize": True, "tied_init": True, "null_attention": True}


def format_config() -> dict:
    cfg = {"name": FORMAT, "state_template": STATE_TEMPLATE, "candidate_template": CANDIDATE_TEMPLATE,
           "binary_answer": BINARY_ANSWER, "tokenize": TOKENIZE, "padding": "right"}
    return cfg | {"sha": hashlib.sha256(json.dumps(cfg, sort_keys=True).encode()).hexdigest()[:12]}


def state_text(state: str) -> str:
    return STATE_TEMPLATE.format(state=state)


def candidate_texts(q: Question) -> list[str]:
    """One sequence per scored item: the question with its proposed answer, never the state."""
    answers = [BINARY_ANSWER] if q.type == "binary" else [c.description for c in q.candidates]
    return [CANDIDATE_TEMPLATE.format(type=q.type, instruction=q.instruction, answer=a) for a in answers]


class CrossAttention(nn.Module):
    """Candidate tokens (queries) attend to state tokens (keys/values). Learns Wq, Wk, Wv and Wo. null=True adds one
    learnable key/value slot (as nn.MultiheadAttention's add_bias_kv): somewhere to attend when nothing in the state
    matches, so "no evidence" is expressible instead of forcing a weighted average of state tokens."""

    def __init__(self, h, heads, dropout, null=False):
        super().__init__()
        self.heads, self.dropout = heads, dropout
        self.q, self.k, self.v, self.o = (nn.Linear(h, h) for _ in range(4))
        self.null = nn.Parameter(torch.zeros(2, h)) if null else None  # [key, value] in memory space

    def forward(self, x, memory, memory_pad):
        split = lambda t: t.unflatten(-1, (self.heads, -1)).transpose(1, 2)  # [S, n, h] -> [S, heads, n, h / heads]
        if self.null is not None:
            memory = torch.cat([self.null[None, :1].expand(len(memory), 1, -1), memory], 1)
            memory_pad = F.pad(memory_pad, (1, 0), value=False)
        q, k, v = split(self.q(x)), split(self.k(memory)), split(self.v(memory))  # K/V: once per state per block
        if self.null is not None:  # the null value is learned directly, not through Wv
            v = torch.cat([split(self.null[None, 1:].expand(len(memory), 1, -1)), v[:, :, 1:]], 2)
        mask, p = ~memory_pad[:, None, None, :], self.dropout if self.training else 0.0
        step = max(1, 2**27 // (k.shape[0] * self.heads * k.shape[2]))  # bound the [S, heads, Q, L] score matrix
        out = torch.cat([F.scaled_dot_product_attention(q[:, :, i:i + step], k, v, attn_mask=mask, dropout_p=p)
                         for i in range(0, q.shape[2], step)], dim=2)  # query rows are independent: chunking is exact
        return self.o(out.transpose(1, 2).flatten(2))


class Block(nn.Module):
    def __init__(self, h, heads, ffn, dropout, null=False):
        super().__init__()
        self.norm_q, self.norm_ffn = nn.LayerNorm(h), nn.LayerNorm(h)
        self.attn = CrossAttention(h, heads, dropout, null)
        self.ffn = nn.Sequential(nn.Linear(h, ffn), nn.GELU(), nn.Linear(ffn, h))
        self.drop = nn.Dropout(dropout)

    def forward(self, q, memory, memory_pad):
        q = q + self.drop(self.attn(self.norm_q(q), memory, memory_pad))
        return q + self.drop(self.ffn(self.norm_ffn(q)))


def _head(h, width):
    head = nn.Sequential(nn.Linear(h, width), nn.GELU(), nn.Linear(width, 1))
    nn.init.zeros_(head[2].weight)  # untrained model starts at logit 0: p = 0.5, uniform softmax
    nn.init.zeros_(head[2].bias)
    return head


class SharedStateClassifier(nn.Module):
    def __init__(self, backbone, pad_id, arch=None):
        super().__init__()
        self.arch = a = ARCH | (arch or {})
        if a["pooling"] != "mean":
            raise ValueError("only masked mean pooling is implemented")
        d, h = backbone.config.hidden_size, a["h"]
        self.backbone, self.pad_id = backbone, pad_id
        self.backbone_grad = False  # False: backbone runs without autograd (frozen / Stage A / inference)
        self.memory_proj = nn.Sequential(nn.Linear(d, h), nn.LayerNorm(h) if a["memory_norm"] else nn.Identity())
        self.candidate_proj = nn.Linear(d, h)
        self.blocks = nn.ModuleList(Block(h, a["heads"], a["ffn"], a["dropout"], a["null_attention"]) for _ in range(a["blocks"]))
        self.norm_out = nn.LayerNorm(h)
        self.binary_head = _head(h, a["head_width"])
        self.choice_head = None if a["shared_head"] else _head(h, a["head_width"])
        if a["tied_init"]:
            self._tie_init()
        self.counts = Counter()  # backbone/interaction work, for instrumentation and benchmarks
        for kind in ("state", "candidate"):  # identity until fit_standardization(); saved with the checkpoint
            self.register_buffer(f"{kind}_mean", torch.zeros(d))
            self.register_buffer(f"{kind}_std", torch.ones(d))

    @torch.no_grad()
    def _tie_init(self):
        self.candidate_proj.weight.copy_(self.memory_proj[0].weight)
        for lin in (self.candidate_proj, self.memory_proj[0]):
            lin.bias.zero_()
        for blk in self.blocks:
            qk, v = (nn.init.orthogonal_(torch.empty_like(blk.attn.q.weight)) for _ in range(2))
            for lin, w in ((blk.attn.q, qk), (blk.attn.k, qk), (blk.attn.v, v), (blk.attn.o, v.T)):
                lin.weight.copy_(w)
                lin.bias.zero_()

    def new_parameters(self):
        return [p for n, p in self.named_parameters() if not n.startswith("backbone.")]

    def hidden(self, ids, kind):
        """Right-padded backbone pass -> (last hidden states [B, W, d] fp32, real-token mask [B, W]). Real tokens get
        positions 0..len-1 exactly as unbatched, and the causal mask keeps them from seeing the padding after them."""
        n, width = len(ids), max(map(len, ids))
        x = torch.full((n, width), self.pad_id, dtype=torch.long)
        m = torch.zeros((n, width), dtype=torch.long)
        for r, t in enumerate(ids):
            x[r, :len(t)] = torch.tensor(t)
            m[r, :len(t)] = 1
        dev = self.norm_out.weight.device
        with torch.set_grad_enabled(torch.is_grad_enabled() and self.backbone_grad):
            out = self.backbone(input_ids=x.to(dev), attention_mask=m.to(dev), use_cache=False).last_hidden_state
        self.counts.update({f"{kind}_calls": 1, f"{kind}_sequences": n, f"{kind}_tokens": sum(map(len, ids)),
                            f"{kind}_padded_tokens": n * width})
        return (out.float() - getattr(self, f"{kind}_mean")) / getattr(self, f"{kind}_std"), m.bool().to(dev)

    @torch.no_grad()
    def fit_standardization(self, state_ids, cand_ids, max_batch_tokens=8192):
        """Per-dimension mean/std of the backbone's last hidden states over real tokens (float64 sums)."""
        if not self.arch["standardize"]:
            return {}
        info = {}
        for kind, ids in (("state", state_ids), ("candidate", cand_ids)):
            getattr(self, f"{kind}_mean").zero_()
            getattr(self, f"{kind}_std").fill_(1.0)
            s1, s2, n = 0.0, 0.0, 0
            for b in length_batches([len(x) for x in ids], max_batch_tokens):
                H, m = self.hidden([ids[i] for i in b], kind)
                x = H[m].cpu().double()
                s1, s2, n = s1 + x.sum(0), s2 + (x * x).sum(0), n + len(x)
            mean = s1 / n
            getattr(self, f"{kind}_mean").copy_(mean)
            getattr(self, f"{kind}_std").copy_((s2 / n - mean * mean).clamp_min(1e-8).sqrt())
            info[kind] = {"sequences": len(ids), "tokens": n}
        return info

    def memory(self, state_ids):
        """-> (memory [S, L, h], padding mask [S, L], True = padding). One backbone pass for all given states."""
        H, m = self.hidden(state_ids, "state")
        return self.memory_proj(H), ~m

    def candidate_tokens(self, cand_ids, max_batch_tokens=16384):
        """-> projected tokens of every candidate, flat [T, h], candidate-major in input order."""
        rows, offset = [], {}
        for b in length_batches([len(x) for x in cand_ids], max_batch_tokens):
            H, _ = self.hidden([cand_ids[i] for i in b], "candidate")
            base, width = sum(len(r) for r in rows), H.shape[1]
            rows.append(H.flatten(0, 1))
            offset |= {i: base + r * width for r, i in enumerate(b)}
        index = [offset[i] + t for i, x in enumerate(cand_ids) for t in range(len(x))]
        flat = torch.cat(rows)
        return self.candidate_proj(flat[torch.tensor(index, device=flat.device)])

    def interact(self, memory, memory_pad, q_tok, owner, lens, multiclass):
        """Pack candidate tokens per state, run the blocks, masked-mean-pool per candidate, apply the heads."""
        dev, S = q_tok.device, memory.shape[0]
        tok_state, tok_pos, tok_cand, fill = [], [], [], [0] * S
        for n, (s, k) in enumerate(zip(owner, lens)):
            tok_state += [s] * k
            tok_pos += range(fill[s], fill[s] + k)
            tok_cand += [n] * k
            fill[s] += k
        ts, tp = torch.tensor(tok_state, device=dev), torch.tensor(tok_pos, device=dev)
        q = q_tok.new_zeros(S, max(fill), q_tok.shape[-1])
        q[ts, tp] = q_tok  # padded query rows are never read back
        for block in self.blocks:
            q = block(q, memory, memory_pad)
        out = self.norm_out(q[ts, tp])
        pooled = out.new_zeros(len(lens), out.shape[-1]).index_add_(0, torch.tensor(tok_cand, device=dev), out)
        pooled = pooled / torch.tensor(lens, device=dev, dtype=out.dtype)[:, None]
        self.counts.update({"memory_rows": S, "query_tokens": len(tok_state)})
        scores = self.binary_head(pooled).squeeze(-1)
        if self.choice_head is None:
            return scores
        return torch.where(torch.tensor(multiclass, device=dev), self.choice_head(pooled).squeeze(-1), scores)

    def forward(self, state_ids, cand_ids, owner, multiclass, max_batch_tokens=16384):
        """state_ids: distinct states; candidate n belongs to state owner[n]; multiclass[n] picks choice_head."""
        memory, pad = self.memory(state_ids)
        q = self.candidate_tokens(cand_ids, max_batch_tokens)
        return self.interact(memory, pad, q, owner, [len(x) for x in cand_ids], multiclass)


def count_params(model: SharedStateClassifier) -> dict:
    new = model.new_parameters()
    bb = list(model.backbone.parameters())
    return {"new_modules": sum(p.numel() for p in new), "backbone": sum(p.numel() for p in bb),
            "backbone_trainable": sum(p.numel() for p in bb if p.requires_grad),
            "new_by_module": {n: sum(p.numel() for p in m.parameters()) for n, m in model.named_children() if n != "backbone"}}


def checkpoint_sha(path) -> str:
    """Hash of everything that determines the scores: weights, adapter and config (not the training log)."""
    path = Path(path)
    files = sorted(p for p in path.rglob("*") if p.is_file() and p.name not in ("train_meta.json", "README.md"))
    return hashlib.sha256("".join(f"{p.relative_to(path)}:{sha256_file(p)}\n" for p in files).encode()).hexdigest()


def save_checkpoint(model: SharedStateClassifier, path, config: dict) -> str:
    """Complete checkpoint: every new module, the adapter or full backbone, and the config needed to rebuild it."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    save_file({k: v.detach().cpu().contiguous() for k, v in model.state_dict().items() if not k.startswith("backbone.")},
              path / "modules.safetensors")
    if config["backbone_mode"] == "lora":
        model.backbone.save_pretrained(path / "adapter", save_embedding_layers=False)
    elif config["backbone_mode"] == "full":
        save_file({k: v.detach().cpu().contiguous() for k, v in model.backbone.state_dict().items()}, path / "backbone.safetensors")
    (path / "config.json").write_text(json.dumps(config | {"arch": model.arch, "format": format_config()}, indent=1))
    return checkpoint_sha(path)


class CustomScorer:
    """Scorer for classify / evaluate / calibrate / bench / serve. Pass `checkpoint` for a trained model; without it the
    new modules are random (tests only). `backbone` injects a module instead of loading the checkpoint (tests only)."""

    def __init__(self, checkpoint=None, device=None, dtype="float32", max_length=8192, max_candidate_length=512,
                 max_batch_tokens=16384, max_batch_size=64, arch=None, backbone=None, model_id=MODEL_ID, revision=MODEL_REVISION):
        if not 0 < max_length <= MAX_CONTEXT:
            raise ValueError(f"max_length must be in (0, {MAX_CONTEXT}]")
        cfg = json.loads((Path(checkpoint) / "config.json").read_text()) if checkpoint else {}
        if cfg and cfg["format"]["sha"] != format_config()["sha"]:
            raise ValueError(f"{checkpoint} was trained with formatting {cfg['format']}; this code formats as {format_config()}")
        model_id, revision = (cfg["base"]["model"], cfg["base"]["revision"]) if cfg else (model_id, revision)
        self.device, self.max_length, self.max_candidate_length = device or default_device(), max_length, max_candidate_length
        self.max_batch_tokens, self.max_batch_size = max_batch_tokens, max_batch_size
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
        if backbone is None:
            backbone = AutoModel.from_pretrained(model_id, revision=revision, dtype=getattr(torch, dtype))
        mode = cfg.get("backbone_mode", "frozen")
        if mode == "lora":
            from peft import PeftModel
            backbone = PeftModel.from_pretrained(backbone, Path(checkpoint) / "adapter")
        elif mode == "full":
            backbone.load_state_dict(load_file(Path(checkpoint) / "backbone.safetensors"))
        self.model = SharedStateClassifier(backbone, self.tokenizer.pad_token_id, cfg.get("arch", arch))
        if checkpoint:
            missing, unexpected = self.model.load_state_dict(load_file(Path(checkpoint) / "modules.safetensors"), strict=False)
            if unexpected or not all(k.startswith("backbone.") for k in missing):
                raise ValueError(f"{checkpoint}: incomplete module weights (missing {missing[:5]}, unexpected {unexpected[:5]})")
        self.model.to(self.device).eval().requires_grad_(False)
        sha = checkpoint_sha(checkpoint) if checkpoint else None
        self.meta = {"model": model_id, "revision": revision, "architecture": f"shared-state cross-attention ({FORMAT})",
                     "adapter": str(checkpoint) if checkpoint else None, "adapter_sha256": sha, "backbone_mode": mode,
                     "trained": bool(checkpoint), "prompt": FORMAT, "prompt_sha": format_config()["sha"], "arch": self.model.arch,
                     "device": self.device, "dtype": dtype, "max_length": max_length, "max_candidate_length": max_candidate_length,
                     "truncation": "none (overlength input raises InputTooLong)", "params": count_params(self.model)}

    def tokenize(self, texts):
        return self.tokenizer(texts, **TOKENIZE)["input_ids"] if texts else []

    @torch.inference_mode()
    def score_requests(self, reqs):
        """-> ([[scores of each question] of each request], stats). Identical states are encoded once per call."""
        t0 = time.perf_counter()
        states, first_req, cands, where = {}, {}, [], []
        for ri, r in enumerate(reqs):
            s = states.setdefault(state_text(r.state), len(states))
            first_req.setdefault(s, ri)
            for q in r.questions:
                for text, cid in zip(candidate_texts(q), [c.id for c in q.candidates] or [None]):
                    cands.append((s, text, q.type == "multiclass"))
                    where.append((ri, q.id, cid))
        state_ids, cand_ids = self.tokenize(list(states)), self.tokenize([c[1] for c in cands])
        if over := [(i, len(x)) for i, x in enumerate(state_ids) if len(x) > self.max_length]:
            raise InputTooLong(over, self.max_length, "; ".join(f"request {first_req[i]} state: {n} tokens" for i, n in over[:5]))
        if over := [(i, len(x)) for i, x in enumerate(cand_ids) if len(x) > self.max_candidate_length]:
            raise InputTooLong(over, self.max_candidate_length, "; ".join(
                f"request {where[i][0]} question '{where[i][1]}'" + (f" candidate '{where[i][2]}'" if where[i][2] else "")
                + f": {n} tokens" for i, n in over[:5]))
        t1 = time.perf_counter()
        by_state = [[] for _ in state_ids]
        for n, c in enumerate(cands):
            by_state[c[0]].append(n)
        scores, self.model.counts = [0.0] * len(cands), Counter()
        for chunk in length_batches([len(x) for x in state_ids], self.max_batch_tokens, self.max_batch_size):
            memory, pad = self.model.memory([state_ids[s] for s in chunk])
            local = {s: i for i, s in enumerate(chunk)}
            ns = [n for s in chunk for n in by_state[s]]
            q = self.model.candidate_tokens([cand_ids[n] for n in ns], self.max_batch_tokens)
            out = self.model.interact(memory, pad, q, [local[cands[n][0]] for n in ns], [len(cand_ids[n]) for n in ns],
                                      [cands[n][2] for n in ns])
            for n, v in zip(ns, out.tolist()):  # .tolist() waits for the device
                scores[n] = v
        t2 = time.perf_counter()
        c = self.model.counts
        stats = {"pairs": len(cands), "batches": c["state_calls"] + c["candidate_calls"],
                 "input_tokens": c["state_tokens"] + c["candidate_tokens"],
                 "padded_tokens": c["state_padded_tokens"] + c["candidate_padded_tokens"],
                 "max_pair_tokens": max(map(len, state_ids + cand_ids), default=0),
                 "state_sequences": c["state_sequences"], "state_tokens": c["state_tokens"],
                 "candidate_sequences": c["candidate_sequences"], "candidate_tokens": c["candidate_tokens"],
                 "memory_rows": c["memory_rows"], "tokenize_ms": 1e3 * (t1 - t0), "model_ms": 1e3 * (t2 - t1)}
        out, k = [], 0
        for r in reqs:
            out.append([])
            for q in r.questions:
                n = len(q.candidates) or 1
                out[-1].append(scores[k:k + n])
                k += n
        return out, stats
