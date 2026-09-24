"""Paired quality changes with bootstrap resampling of source records, not individual questions."""
import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np


def compare(reference, candidate, repeats=10000):
    a={r['id']:r for r in reference};b={r['id']:r for r in candidate}
    if a.keys()!=b.keys():
        raise ValueError('Evaluation IDs differ')
    groups=defaultdict(list)
    for i,r in a.items():
        if r['target']!=b[i]['target'] or r['candidate_ids']!=b[i]['candidate_ids']:
            raise ValueError(f'Target/candidate mismatch at {i}')
        groups[r.get('source_id') or i].append(i)
    delta=np.array([sum(int(b[i]['correct'])-int(a[i]['correct']) for i in ids) for ids in groups.values()])
    sizes=np.array([len(ids) for ids in groups.values()])
    rng=np.random.default_rng(8431);samples=[]
    for start in range(0,repeats,100):
        indexes=rng.integers(0,len(groups),(min(100,repeats-start),len(groups)))
        samples.extend((delta[indexes].sum(1)/sizes[indexes].sum(1)).tolist())
    changed=[{'id':i,'source_id':a[i]['source_id'],'family':a[i]['family'],
              'reference_selected':a[i]['selected'],'candidate_selected':b[i]['selected'],
              'reference_correct':a[i]['correct'],'candidate_correct':b[i]['correct']}
             for i in a if a[i]['selected']!=b[i]['selected']]
    return {'n':len(a),'sources':len(groups),
            'reference_accuracy':sum(r['correct'] for r in a.values())/len(a),
            'candidate_accuracy':sum(r['correct'] for r in b.values())/len(b),
            'accuracy_delta':float(delta.sum()/sizes.sum()),
            'source_cluster_bootstrap_95_ci':np.quantile(samples,[.025,.975]).tolist(),
            'bootstrap_repeats':repeats,'bootstrap_seed':8431,
            'candidate_only_correct':sum(b[i]['correct'] and not a[i]['correct'] for i in a),
            'reference_only_correct':sum(a[i]['correct'] and not b[i]['correct'] for i in a),
            'decision_changes':changed}


def main():
    p=argparse.ArgumentParser();p.add_argument('reference');p.add_argument('candidate');p.add_argument('--out',required=True)
    args=p.parse_args()
    a=json.loads(Path(args.reference).read_text());b=json.loads(Path(args.candidate).read_text())
    a=a.get('development',a);b=b.get('development',b)
    ap,bp=a['predictions'],b['predictions']
    result={'reference_file':args.reference,'candidate_file':args.candidate,'overall':compare(ap,bp),'slices':{}}
    selectors={'authored':lambda r:r['family'].startswith('eval_'),
               'public_seen_families':lambda r:r['family'].startswith('hf_'),
               'public_heldout_families':lambda r:r['family'].startswith('heldout_')}
    selectors|={f'family:{f}':lambda r,f=f:r['family']==f for f in sorted({r['family'] for r in ap})}
    for name,choose in selectors.items():
        x=[r for r in ap if choose(r)];y=[r for r in bp if choose(r)]
        if x:
            result['slices'][name]=compare(x,y)
    Path(args.out).write_text(json.dumps(result,indent=1))
    print({k:v for k,v in result['overall'].items() if k!='decision_changes'})


if __name__=='__main__':main()
