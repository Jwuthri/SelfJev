"""Build the pilot's paired quality/latency gate from saved reports only."""
import json
from pathlib import Path
import numpy as np
from compare_compact_quality import compare

ROOT=Path('reports/t5_round2b_2026-09-24')

def load(p):return json.loads(p.read_text())
def compact(row):return {k:v for k,v in row.items() if k!='decision_changes'}
def ratio(a,b):
    if len(a)!=len(b):raise ValueError('Latency sample counts differ')
    rng=np.random.default_rng(87191);a=np.array(a);b=np.array(b)
    ix=rng.integers(0,len(a),(10000,len(a)))
    dist=np.median(a[ix],axis=1)/np.median(b[ix],axis=1)
    return {'median_speedup':float(np.median(a)/np.median(b)),
            'paired_request_bootstrap_95_ci':np.quantile(dist,[.025,.975]).tolist(),
            'bootstrap_repeats':10000,'bootstrap_seed':87191}

def main():
    all_names=[p.parent.name for p in ROOT.glob('*/bench.json')]
    names=[n for n in all_names if (ROOT/n/'complete.json').exists() and all((ROOT/n/sp/'report.json').exists() for sp in ['test','eval2'])]
    incomplete=sorted(set(all_names)-set(names))
    benches={k:load(ROOT/k/'bench.json') for k in names}
    if len({x['request_sha256'] for x in benches.values()})!=1:raise ValueError('Request hashes differ')
    primary={k:next(r for r in b['rows'] if r['bucket']=='2048_16') for k,b in benches.items()}
    qualities={k:{sp:load(ROOT/k/sp/'report.json') for sp in ['test','eval2']} for k in names}
    # Fastest measured BF16 tree implementation is the main replacement control.
    # FP8 is an additional separately quality-checked optimization, not a weakened control.
    controls=['tree_r2b','tree_r2b_merged','tree_r2b_vllm']
    missing_controls=[k for k in controls if k not in names]
    if missing_controls:raise RuntimeError({'missing_primary_controls':missing_controls,'incomplete':incomplete})
    reference=min(controls,key=lambda k:primary[k]['p50_ms'])
    out={'primary_reference':reference,'primary_bucket':'2048_16','quality_limit_pp':1.,'speedup_target':2.,
         'note':'Development screen only: eval2 informed the research direction. CI describes this dataset/request corpus, not unseen domains or production traffic.',
         'backends':{},'gates':{},'incomplete_backends':incomplete}
    for name in names:
        out['backends'][name]={'accuracy':{sp:qualities[name][sp]['metrics']['question_accuracy'] for sp in qualities[name]},
            'p50_ms':primary[name]['p50_ms'],'p95_ms':primary[name]['p95_ms'],
            'adapter_sha256':qualities[name]['eval2']['meta'].get('adapter_sha256')}
        if name==reference:continue
        aa=qualities[reference]['eval2']['predictions'];bb=qualities[name]['eval2']['predictions']
        quality=compare(aa,bb);speed=ratio(primary[reference]['raw_ms'],primary[name]['raw_ms'])
        slices={}
        for f in sorted({r['family'] for r in aa}):
            slices[f]=compact(compare([r for r in aa if r['family']==f],[r for r in bb if r['family']==f]))
        hard_cases={}
        tags=sorted({t for r in aa for t in r.get('hard_cases',[])})
        for tag in tags:
            hard_cases[tag]=compact(compare([r for r in aa if tag in r.get('hard_cases',[])],[r for r in bb if tag in r.get('hard_cases',[])]))
        full={'reference':reference,'candidate':name,'quality':quality,'families':slices,'hard_cases':hard_cases,'speed':speed}
        (ROOT/f'comparison_{name}.json').write_text(json.dumps(full,indent=2))
        out['gates'][name]={'quality':compact(quality),'speed':speed,
            'quality_point_pass':quality['accuracy_delta']>=-.01,'speed_point_pass':speed['median_speedup']>=2.,
            'both_point_pass':quality['accuracy_delta']>=-.01 and speed['median_speedup']>=2.,
            'quality_ci_lower_bound_within_limit':quality['source_cluster_bootstrap_95_ci'][0]>=-.01}
    (ROOT/'acceptance.json').write_text(json.dumps(out,indent=2))
    lines=['# Matched T5 round-2b pilot: measured results','',f'Primary control: `{reference}` (fastest measured BF16 round-2b tree).',
        '', '| Backend | Development accuracy | Eval2 accuracy | 2K × 16 × 3 p50 | p95 | Speedup | Both point gates |',
        '|---|---:|---:|---:|---:|---:|---|']
    for k,b in sorted(out['backends'].items()):
        g=out['gates'].get(k,{})
        lines.append(f"| {k} | {100*b['accuracy']['test']:.2f}% | {100*b['accuracy']['eval2']:.2f}% | {b['p50_ms']:.1f} ms | {b['p95_ms']:.1f} ms | {g.get('speed',{}).get('median_speedup',1):.2f}× | {str(g.get('both_point_pass','control'))} |")
    lines+=['','Quality is whole-question accuracy, including multilabel exact match. Local resident-model times include tokenization but exclude network and loading. Same L40S and request bytes; 100 new document prefixes in the primary cell.','',
        'This corrected run adapts both native text stacks. The first pilot accidentally adapted only the decoder; its separate archive is excluded here. Historical R1 results use a different training recipe and are a reference, not a matched-data treatment.', '',
        'The 2× / 1-percentage-point criteria are an experiment target. These reused development datasets do not establish generalization to a fresh final set. See `acceptance.json` and per-backend comparison JSON for paired source-cluster confidence intervals and family results.']
    (ROOT/'results.md').write_text('\n'.join(lines)+'\n')
    print('\n'.join(lines))
if __name__=='__main__':main()
