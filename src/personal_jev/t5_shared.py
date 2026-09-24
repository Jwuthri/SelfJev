"""T5Gemma reader with bounded decoder batches and shared cross-KV storage.

Reuses the pretrained challenger implementation and its exact input/readout format.
The encoder and each layer's document projections run once per distinct document.
Cross-KV batch expansion is a view; native attention still materializes each layer's
merged self/cross tensors. This is bounded storage, not a specialized shared-KV kernel.
"""
import time
import copy
import torch
from transformers import DynamicCache, EncoderDecoderCache
from .challengers import ChallengerScorer, padded


def t5_text_lora_targets(model, module_names=('q_proj', 'k_proj', 'v_proj', 'o_proj')):
    """Require every requested attention projection in BOTH native text stacks.

    T5Gemma's encoder layers live under encoder.text_model, not encoder.layers.
    Resolve the actual modules, so a path drift fails rather than silently
    training only the decoder. The unused vision tower is intentionally excluded.
    """
    stacks = {'encoder': ('model.encoder.text_model.layers', model.model.encoder.text_model.layers),
              'decoder': ('model.decoder.layers', model.model.decoder.layers)}
    targets = []; coverage = {}
    for side, (prefix, layers) in stacks.items():
        names = [f'{prefix}.{i}.self_attn.{name}' for i in range(len(layers)) for name in module_names]
        if not names:
            raise ValueError(f'No {side} attention targets')
        for name in names:
            if not isinstance(model.get_submodule(name), torch.nn.Linear):
                raise TypeError(f'Expected native text projection: {name}')
        coverage[side] = {'layers': len(layers), 'modules': len(names)}
        targets.extend(names)
    return targets, coverage


class T5SharedScorer(ChallengerScorer):
    def __init__(self, adapter=None, device='cuda', dtype='bfloat16', max_length=32768,
                 branch_batch=16, merge=False, decoder_prefix=False):
        if branch_batch < 1:
            raise ValueError('branch_batch must be positive')
        super().__init__('t5gemma2', adapter=adapter, device=device, dtype=dtype,
                         max_length=max_length, branch_batch=branch_batch, t5_share_kv=True)
        if merge and adapter:
            self.model = self.model.merge_and_unload()
        self.meta.update(architecture='pretrained T5Gemma encoder/decoder; shared document cross-KV views',
                         cache_storage='one cross-KV per layer/document; bounded expanded decoder views',
                         merged=bool(merge and adapter))
        self.last_counts = {}
        self.decoder_prefix = decoder_prefix
        self.meta["shared_decoder_prefix"] = decoder_prefix

    @torch.inference_mode()
    def shared_entries(self, entries):
        if getattr(self, "decoder_prefix", False):
            return self.prefix_shared_entries(entries)
        groups = {}; offset = 0
        for entry in entries:
            for branch in entry['branches']:
                groups.setdefault(tuple(entry['root']), []).append((offset, branch))
                offset += 1
        if not offset:
            return torch.empty(0, device=self.device)
        results = [None] * offset
        model = self.base().model
        counts = dict(encoder_calls=0, cross_projection_pairs=0, decoder_batches=0,
                      max_branch_rows=0, cross_kv_storage_bytes=0)
        for root, branches in groups.items():
            ids = torch.tensor([root], device=self.device)
            em = torch.ones_like(ids)
            enc = model.encoder(input_ids=ids, attention_mask=em).last_hidden_state
            counts['encoder_calls'] += 1
            projected = []
            for layer in model.decoder.layers:
                attn = layer.self_attn
                shape = (*enc.shape[:-1], -1, attn.head_dim)
                k = attn.k_norm(attn.k_proj(enc).view(shape).transpose(1, 2))
                v = attn.v_proj(enc).view(shape).transpose(1, 2)
                projected.append((k, v))
                counts['cross_projection_pairs'] += 1
            counts['cross_kv_storage_bytes'] = max(counts['cross_kv_storage_bytes'],
                sum(t.numel() * t.element_size() for pair in projected for t in pair))
            for start in range(0, len(branches), self.branch_batch):
                chunk = branches[start:start + self.branch_batch]
                rows = len(chunk)
                di, dm = padded([b for _, b in chunk], self.pad, self.device)
                cache = EncoderDecoderCache(DynamicCache(config=model.decoder.config), DynamicCache())
                for i, (k, v) in enumerate(projected):
                    cache.cross_attention_cache.update(k.expand(rows, -1, -1, -1),
                                                       v.expand(rows, -1, -1, -1), i)
                    cache.is_updated[i] = True
                h = model.decoder(input_ids=di, attention_mask=dm,
                    encoder_hidden_states=enc.expand(rows, -1, -1),
                    encoder_attention_mask=em.expand(rows, -1),
                    past_key_values=cache, use_cache=True).last_hidden_state
                values = self.readout(h[torch.arange(rows, device=self.device), dm.sum(1) - 1])
                for (i, _), value in zip(chunk, values):
                    results[i] = value
                counts['decoder_batches'] += 1
                counts['max_branch_rows'] = max(counts['max_branch_rows'], rows)
                del cache, h
        self.last_counts = counts
        return torch.stack(results)

    @torch.inference_mode()
    def prefix_shared_entries(self, entries):
        """Share the document and native decoder common-prefix cache independently.

        Copy only the small decoder self-cache before a branch mutates it. Cross
        keys/values remain views of the read-only root cache, including when the
        self-cache uses native sliding-window bookkeeping.
        """
        groups = {}; offset = 0
        for e in entries:
            for branch in e['branches']:
                groups.setdefault(tuple(e['root']), []).append((offset, branch)); offset += 1
        if not offset:
            self.last_counts = {}
            return torch.empty(0, device=self.device)
        results = [None] * offset; model = self.base().model
        counts = dict(encoder_calls=0, cross_projection_pairs=0, decoder_batches=0,
                      max_branch_rows=0, cross_kv_storage_bytes=0, shared_decoder_tokens=0)
        for root, branches in groups.items():
            ids = torch.tensor([root], device=self.device); em = torch.ones_like(ids)
            enc = model.encoder(input_ids=ids, attention_mask=em).last_hidden_state
            counts['encoder_calls'] += 1
            common = 0
            for tokens in zip(*[b for _, b in branches]):
                if len(set(tokens)) != 1: break
                common += 1
            common = min(common, min(len(b) for _, b in branches) - 1)
            if common < 1:
                raise ValueError('Native decoder branches must share a start token and retain a scored suffix')
            prefix = torch.tensor([branches[0][1][:common]], device=self.device)
            root_cache = model.decoder(input_ids=prefix, attention_mask=torch.ones_like(prefix),
                encoder_hidden_states=enc, encoder_attention_mask=em, use_cache=True).past_key_values
            counts['decoder_batches'] += 1
            counts['shared_decoder_tokens'] += common
            counts['cross_projection_pairs'] += len(model.decoder.layers)
            counts['cross_kv_storage_bytes'] = max(counts['cross_kv_storage_bytes'],
                sum(t.numel() * t.element_size() for layer in root_cache.cross_attention_cache.layers
                    for t in (layer.keys, layer.values)))
            for start in range(0, len(branches), self.branch_batch):
                chunk = branches[start:start + self.branch_batch]; rows = len(chunk)
                di, dm = padded([b[common:] for _, b in chunk], self.pad, self.device)
                self_cache = copy.deepcopy(root_cache.self_attention_cache)
                self_cache.reorder_cache(torch.zeros(rows, device=self.device, dtype=torch.long))
                cache = EncoderDecoderCache(self_cache, DynamicCache())
                for i, layer in enumerate(root_cache.cross_attention_cache.layers):
                    cache.cross_attention_cache.update(layer.keys.expand(rows, -1, -1, -1),
                                                        layer.values.expand(rows, -1, -1, -1), i)
                    cache.is_updated[i] = True
                mask = torch.cat([torch.ones((rows, common), device=self.device, dtype=dm.dtype), dm], 1)
                h = model.decoder(input_ids=di, attention_mask=mask,
                    encoder_hidden_states=enc.expand(rows, -1, -1),
                    encoder_attention_mask=em.expand(rows, -1),
                    past_key_values=cache, use_cache=True).last_hidden_state
                values = self.readout(h[torch.arange(rows, device=self.device), dm.sum(1) - 1])
                for (i, _), value in zip(chunk, values): results[i] = value
                counts['decoder_batches'] += 1
                counts['max_branch_rows'] = max(counts['max_branch_rows'], rows)
                del cache, self_cache, h
            del root_cache, enc
        self.last_counts = counts
        return torch.stack(results)

    @torch.inference_mode()
    def score_requests(self, reqs):
        start = time.perf_counter()
        entries = [self.entry(r.state, q) for r in reqs for q in r.questions]
        prepared = time.perf_counter()
        scores = self.shared_entries(entries).tolist()
        k = 0; per = []
        for e in entries:
            per.append(scores[k:k + e['n']]); k += e['n']
        out = []; k = 0
        for r in reqs:
            out.append(per[k:k + len(r.questions)]); k += len(r.questions)
        unique = {tuple(e['root']) for e in entries}
        stats = dict(pairs=len(scores), batches=self.last_counts.get('decoder_batches', 0),
            input_tokens=sum(map(len, unique)) + sum(sum(map(len, e['branches'])) for e in entries),
            padded_tokens=None, state_sequences=self.last_counts.get('encoder_calls', 0),
            tokenize_ms=1000 * (prepared-start), model_ms=1000 * (time.perf_counter()-prepared),
            **self.last_counts)
        return out, stats
