"""Read-only checkpoint ablation on validation data. Run from the repository root.

Capture the trained heads during the same forward pass as the complete model.
The residual score is exactly the learned-weight MaxSim contribution. No fitting,
threshold selection, or checkpoint modification; independent decoder decisions at T=1.
"""
import json
import random
import time
from pathlib import Path

import torch
from personal_jev.custom import CustomScorer, checkpoint_sha
from personal_jev.data import load, sha256_file
from personal_jev.evaluate import evaluate_predictions
from personal_jev.classify import decide
from personal_jev.schemas import parse_question
from personal_jev.train_custom import encode_items, micro_batches, forward_items

OUT = Path(__file__).resolve().parent
checkpoint = 'runs/custom_sim_lora/checkpoint'
start = time.time()
scorer = CustomScorer(checkpoint, device='mps', dtype='bfloat16')
model = scorer.model.eval()
examples = load(['data/hf.jsonl', 'data/eval.jsonl'], {'validation'})
items, states, dropped = encode_items(scorer.tokenizer, examples, 8192, 512)
assert not dropped
by_id = {e['id']: e for e in examples}
captured = {}
handles = [getattr(model, name).register_forward_hook(
    lambda module, args, output, name=name: captured.__setitem__(name, output.detach().flatten())
) for name in ('binary_head', 'choice_head')]
results = {k: [] for k in ('full', 'head_only', 'similarity_only')}
scores_saved = []
batches = micro_batches(items, states, 8192, random.Random(0))
with torch.inference_mode():
    for bi, batch in enumerate(batches):
        selected = [items[i] for i in batch]
        full = forward_items(model, selected, states, 8192)
        mc = torch.tensor([it['type'] == 'multiclass' for it in selected for _ in it['ids']], device=full.device)
        heads = torch.where(mc, captured['choice_head'][:len(full)], captured['binary_head'][:len(full)])
        components = {'full': full.tolist(), 'head_only': heads.tolist(), 'similarity_only': (full-heads).tolist()}
        k = 0
        for it in selected:
            ex = by_id[it['id']]
            q = parse_question({'id':'q', **ex['question']})
            n = len(it['ids'])
            raw = {name: vals[k:k+n] for name, vals in components.items()}
            scores_saved.append({'id': ex['id'], 'type': q.type, 'family': ex['family'], **raw})
            for name, vals in raw.items():
                dec = decide(q, vals)
                row = {'id':ex['id'], 'source_id':ex['source_id'], 'family':ex['family'], 'type':q.type,
                       'target':ex['target'], 'selected':dec['selected'], 'candidate_ids':[c.id for c in q.candidates],
                       'scores':vals, 'probabilities': [dec['p_yes']] if q.type=='binary' else [c['probability'] for c in dec['candidates']]}
                if q.type=='binary': row['p_yes'] = dec['p_yes']
                row['correct'] = set(row['selected']) == set(row['target']) if q.type=='multilabel' else row['selected']==row['target']
                results[name].append(row)
            k += n
        if bi % 10 == 0: print(f'batch {bi+1}/{len(batches)} ({time.time()-start:.1f}s)', flush=True)
for h in handles: h.remove()
report = {'meta': {'checkpoint':checkpoint,'sha256':checkpoint_sha(checkpoint), 'dtype':'bfloat16','device':'mps',
                   'split':'validation', 'n':len(examples),'sim_scale':model.sim_scale.tolist(),
                   'data_sha256':{p:sha256_file(p) for p in ['data/hf.jsonl','data/eval.jsonl']},'wall_s':time.time()-start,
                   'caveat':'Post-training component removal, not separately retrained architectures. No probability calibration.'},
          'metrics':{name:evaluate_predictions(rows) for name,rows in results.items()},
          'by_family':{name:{fam:evaluate_predictions([r for r in rows if r['family']==fam]) for fam in sorted({r['family'] for r in rows})} for name,rows in results.items()},
          'scores':sorted(scores_saved,key=lambda r:r['id'])}
(OUT/'component_ablation.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'meta':report['meta'],'metrics':report['metrics']},indent=2),flush=True)
