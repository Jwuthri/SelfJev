"""Reconstruct the historical R2b IDs with its tokenizer and immutable source hashes."""
import json, random
from pathlib import Path
from transformers import AutoTokenizer
from personal_jev.train import select_data
from personal_jev.train_tree import encode_items
from personal_jev.tree import Encoder
from personal_jev.data import sha256_file

out = Path('reports/t5_round2b_2026-09-24'); out.mkdir(parents=True, exist_ok=True)
meta = json.loads(Path('runs/tree_4b_r2b/train_meta.json').read_text()); cfg = meta['config']
for row in meta['data']['train_files'] + meta['data']['val_files']:
    if sha256_file(row['path']) != row['sha256']: raise ValueError(f"Changed R2b source: {row['path']}")
tr, va = select_data(cfg, random.Random(cfg['seed']))
enc = Encoder(AutoTokenizer.from_pretrained(cfg['model_id'], revision=cfg['revision']), cfg['model_id'])
manifest = {'reference_config':cfg,'reference_adapter_sha256':meta['adapter_sha256'],
            'source_files':meta['data'], 'selection_rule':'exact historical Qwen R2b tokenizer eligibility, not T5 eligibility'}
base = Path('runs/t5_round2b_inputs'); base.mkdir(exist_ok=True)
for label, examples, expected in [('train',tr,16375),('validation',va,1388)]:
    its, _, dropped = encode_items(enc, examples, cfg['max_length'])
    ids = [it['id'] for it in its]; keep = set(ids)
    assert len(ids) == expected, (label,len(ids),expected)
    selected = [ex for ex in examples if ex['id'] in keep]
    assert [ex['id'] for ex in selected] == ids
    p=base/f'{label}.jsonl'; p.write_text(''.join(json.dumps(ex)+'\n' for ex in selected))
    manifest[label] = {'ids':ids,'n':len(ids),'file':str(p),'sha256':sha256_file(p),'dropped_by_family':dropped}
(out/'selection.json').write_text(json.dumps(manifest,indent=2)+'\n')
print({k:manifest[k]['n'] for k in ('train','validation')},flush=True)
