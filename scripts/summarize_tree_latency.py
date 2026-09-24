"""Generate an auditable progress/result summary from saved experiment artifacts."""
import json
from pathlib import Path

ROOT=Path('reports/latency_optimization_2026-09-24')


def read(name):
    p=ROOT/name
    return json.loads(p.read_text()) if p.exists() else None


def main():
    lines=['# Measured tree latency and compact-format results','',
           'This file is regenerated from saved JSON artifacts. Missing results are pending, not zero.',
           'Server-side timings use a resident model; vLLM cold-prefix calls explicitly clear the prefix cache. No network time is included.','']
    runs={n:read(f) for n,f in [('Original HF','hf_original_a10g.json'),('Optimized HF','hf_optimized_a10g.json'),
                               ('Compact HF','hf_compact_a10g.json')]}
    vllm=read('vllm_a10g.json')
    by={n:{(r['state_tokens'],r['questions']):r for r in (v or {}).get('rows',[])} for n,v in runs.items()}
    vb={(r['state_tokens'],r['questions']):r for r in (vllm or {}).get('rows',[])}
    lines+=['## A10G latency','', 'The vLLM columns here are the original phase-one R1 run. The extended table below compares R1 and compact using the same three cache modes.', '', '| Document tokens | Questions × 3 options | Original HF ms | Optimized HF ms | Compact HF ms | R1 vLLM cold ms | R1 vLLM identical-request ms |',
             '|---:|---:|---:|---:|---:|---:|---:|']
    keys=sorted(set().union(*(set(v) for v in by.values()),set(vb)))
    def fmt(x):return f'{x:.2f}' if x is not None else 'pending'
    for key in keys:
        vals=[by[n].get(key,{}).get('median_ms') for n in runs]
        vals += [vb.get(key,{}).get(m+'_median_ms') for m in ('cold_prefix','warm_prefix')]
        lines.append(f'| {key[0]} | {key[1]} | '+' | '.join(fmt(x) for x in vals)+' |')
    extended=read('vllm_extended_a10g.json');compact_vllm=read('vllm_compact_a10g.json')
    if extended or compact_vllm:
        lines+=['','## Matched extended vLLM benchmark','',
                'Document-warm excludes root-cache creation; each raw repetition also records that creation cost. Identical-request warm additionally reuses question/candidate prefixes.',
                '', '| Document tokens | Questions × 3 options | R1 cold ms | Compact cold ms | R1 document-warm ms | Compact document-warm ms | R1 identical-request ms | Compact identical-request ms |',
                '|---:|---:|---:|---:|---:|---:|---:|---:|']
        eb={(r['state_tokens'],r['questions']):r for r in (extended or {}).get('rows',[])}
        cb={(r['state_tokens'],r['questions']):r for r in (compact_vllm or {}).get('rows',[])}
        for key in sorted(eb.keys()|cb.keys()):
            vals=[d.get(key,{}).get(mode+'_median_ms') for mode in ('cold_prefix','warm_document','warm_prefix') for d in (eb,cb)]
            lines.append(f'| {key[0]} | {key[1]} | '+' | '.join(fmt(v) for v in vals)+' |')
    lines+=['','## Quality','', '| Run | Evaluation | Questions | Question accuracy | Binary AUROC |', '|---|---|---:|---:|---:|']
    specs=[('R1 unmerged','development','r1_unmerged_development.json'),('R1 merged','development','r1_merged_development.json'),
           ('Compact merged','development','compact_development.json'),('R1 merged','fresh rules','r1_fresh.json'),
           ('Compact merged','fresh rules','compact_fresh.json')]
    quality={}
    for name,kind,file in specs:
        v=read(file)
        if v:
            quality[name,kind]=v
            m=v['metrics'];auc=m.get('binary',{}).get('auroc')
            lines.append(f"| {name} | {kind} | {len(v['predictions'])} | {100*m['question_accuracy']:.3f}% | {f'{auc:.4f}' if auc is not None else '—'} |")
    for name,run in [('vLLM R1',vllm),('vLLM compact',compact_vllm)]:
        if run and 'development' in run:
            v=run['development'];auc=v['metrics'].get('binary',{}).get('auroc')
            lines.append(f"| {name} | development | {len(v['predictions'])} | {100*v['metrics']['question_accuracy']:.3f}% | {f'{auc:.4f}' if auc is not None else '—'} |")
    lines+=['','## Authored development cases','', '| Run | Questions | Accuracy |', '|---|---:|---:|']
    for name,kind,file in specs:
        v=read(file)
        if v and kind=='development':
            rows=[r for r in v['predictions'] if r['family'].startswith('eval_')]
            lines.append(f"| {name} | {len(rows)} | {100*sum(r['correct'] for r in rows)/len(rows):.3f}% |")
    ref=quality.get(('R1 merged','development'));new=quality.get(('Compact merged','development'))
    if ref and new:
        lines+=['','## Development quality by family','', '| Family | Questions | R1 accuracy | Compact accuracy | Change, points |', '|---|---:|---:|---:|---:|']
        for family,a in ref['breakdowns']['by_family'].items():
            b=new['breakdowns']['by_family'][family]
            n=sum(r['family']==family for r in ref['predictions'])
            lines.append(f"| {family} | {n} | {100*a['question_accuracy']:.2f}% | {100*b['question_accuracy']:.2f}% | {100*(b['question_accuracy']-a['question_accuracy']):+.2f} |")
        lines+=['','## Calibration and output types','', '| Metric | R1 merged | Compact merged |', '|---|---:|---:|']
        for label,t,k in [('Binary accuracy','binary','accuracy'),('Binary AUROC','binary','auroc'),('Binary ECE','binary','ece'),
                          ('Multiclass accuracy','multiclass','accuracy'),('Multiclass ECE','multiclass','ece_top_label'),
                          ('Multilabel exact match','multilabel','exact_match'),('Multilabel ECE','multilabel','ece')]:
            lines.append(f"| {label} | {ref['metrics'][t][k]:.4f} | {new['metrics'][t][k]:.4f} |")
    comparisons=[]
    for kind in ['development','fresh rules']:
        ref=quality.get(('R1 merged',kind));new=quality.get(('Compact merged',kind))
        if not ref or not new: continue
        a={r['id']:r for r in ref['predictions']};b={r['id']:r for r in new['predictions']}
        assert a.keys()==b.keys()
        changes=[{'id':i,'family':a[i]['family'],'reference_selected':a[i]['selected'],'new_selected':b[i]['selected'],
                  'reference_correct':a[i]['correct'],'new_correct':b[i]['correct']} for i in a if a[i]['selected']!=b[i]['selected']]
        gain=sum(not a[i]['correct'] and b[i]['correct'] for i in a);loss=sum(a[i]['correct'] and not b[i]['correct'] for i in a)
        comparisons.append({'evaluation':kind,'new_only_correct':gain,'reference_only_correct':loss,'changes':changes})
        lines+=['',f'{kind}: compact-only correct **{gain}**; reference-only correct **{loss}**.']
    (ROOT/'paired_changes.json').write_text(json.dumps(comparisons,indent=1))
    train=Path('runs/tree_4b_compact_v2/train_meta.json')
    if train.exists():
        t=json.loads(train.read_text())
        lines+=['','## Compact training','',
                f"Selected step **{t['best']['step']}** by validation loss **{t['best']['loss']:.5f}**. Training wall time {t['wall_s']/60:.1f} minutes; {t['data']['train_questions']:,} training questions.",
                '', '| Step | Validation loss | Validation accuracy |', '|---:|---:|---:|']
        for r in t['log']:
            if 'val' in r:lines.append(f"| {r['step']} | {r['val']['loss']:.5f} | {100*r['val']['question_accuracy']:.3f}% |")
        lines += ['',f"Adapter reload maximum score difference: `{t['reload_check']['max_abs_score_diff']}`."]
    lines+=['','## Interpretation boundaries','',
            '- The established benchmark has informed development; it is not a new untouched test.',
            '- The fresh challenge is programmatically labeled and narrow. It does not establish broad human-judgment quality.',
            '- A shorter token sequence is an architectural change and must be evaluated after adaptation.',
            '- Cold-prefix and warm-prefix latency answer different deployment questions.',
            '- Different Torch versions between HF and vLLM are recorded; this is a serving-stack comparison, not a kernel-only ablation.','']
    (ROOT/'results.md').write_text('\n'.join(lines))


if __name__=='__main__':main()
