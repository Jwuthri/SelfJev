"""Recompute review evidence from local files. Does not call any API or alter source reports."""
import hashlib
import importlib.util
import json
import math
import random
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from personal_jev.data import load, sha256_file
from personal_jev.evaluate import evaluate_predictions
from personal_jev.train import select_data

ROOT = Path.cwd()
OUT = Path(__file__).resolve().parent
def close(a,b):
    if isinstance(a,dict): return a.keys()==b.keys() and all(close(a[k],b[k]) for k in a)
    if isinstance(a,list): return len(a)==len(b) and all(close(x,y) for x,y in zip(a,b))
    if isinstance(a,float) and isinstance(b,(float,int)): return math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-12)
    return a==b
names = ['baseline','lora_pilot','baseline_4b','lora_4b','baseline_8b','lora_8b','custom_frozen',
         'custom_distill_frozen','custom_distill_lora','custom_sim_frozen','custom_sim_lora']
paths = {n:Path('reports')/n/'test/report.json' for n in names}
paths |= {n:Path('reports/external/full')/p/'report.json' for n,p in [('jev','typesafe_jev-latest'),('astra','openai_gpt-6-astra')]}
reports = {n:json.loads(p.read_text()) for n,p in paths.items()}
gold = {e['id']:e for e in load(['data/hf.jsonl','data/eval.jsonl'],{'test'})}
audit = {'head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
         'git_status':subprocess.check_output(['git','status','--short'],text=True), 'tests':'78 passed, 3 warnings, 121.51 s',
         'reports':{},'calibrated':{}, 'data':{},'benchmarks':{}}
for name, rep in reports.items():
    rows=rep['predictions']; ids=[r['id'] for r in rows]
    assert len(ids)==len(set(ids))==len(gold) and set(ids)==set(gold)
    for r in rows:
        e=gold[r['id']]
        assert r['target']==e['target'] and r['type']==e['question']['type']
        assert r['candidate_ids']==[c['id'] for c in e['question'].get('candidates',[])]
        assert r['correct']==(set(r['target'])==set(r['selected']) if r['type']=='multilabel' else r['target']==r['selected'])
    metrics=evaluate_predictions(rows)
    assert close(metrics,rep['metrics']),name
    audit['reports'][name]={'path':str(paths[name]),'sha256':sha256_file(paths[name]),'meta':rep['meta'],'metrics':metrics,
      'slices':{prefix:{'n':len(rs),'accuracy':sum(r['correct'] for r in rs)/len(rs)} for prefix in ['eval_','hf_','heldout_'] if (rs:=[r for r in rows if r['family'].startswith(prefix)])},
      'by_family':{f: {'n':len(rs),'accuracy':sum(r['correct'] for r in rs)/len(rs)} for f in sorted({r['family'] for r in rows}) if (rs:=[r for r in rows if r['family']==f])},
      'binary_predicted_positive':sum(r['selected'] for r in rows if r['type']=='binary'),
      'multilabel_predicted_positive':sum(len(r['selected']) for r in rows if r['type']=='multilabel')}
    cal=Path('reports')/name/'test_calibrated/report.json'
    if cal.exists():
        cr=json.loads(cal.read_text())
        assert close(evaluate_predictions(cr['predictions']),cr['metrics']),str(cal)
        audit['calibrated'][name]={'path':str(cal),'metrics':cr['metrics'],'calibration':cr['meta']['calibration']}

all_ex=load(['data/hf.jsonl','data/eval.jsonl','data/synthetic.jsonl','data/dev.jsonl'])
norm=lambda s:re.sub(r'\s+',' ',s.strip().lower())
grouped=defaultdict(list)
for e in all_ex: grouped[norm(e['state'])].append(e)
cross=[v for v in grouped.values() if len({e['split'] for e in v})>1]
audit['cross_split_exact']=[{'ids':[e['id'] for e in v],'splits':sorted({e['split'] for e in v})} for v in cross]
audit['train_test_exact_groups']=sum(any(e['split']=='train' for e in v) and any(e['split']=='test' for e in v) for v in cross)
for p in ['data/hf.jsonl','data/eval.jsonl','data/synthetic.jsonl','data/distill.jsonl']:
    ex=load(p)
    audit['data'][p]={'sha256':sha256_file(p),'n':len(ex),'splits':dict(Counter(e['split'] for e in ex)),'types':dict(Counter(e['question']['type'] for e in ex))}
cfg=json.loads(Path('runs/lora_pilot/train_meta.json').read_text())['config']
tr,va=select_data(cfg,random.Random(cfg['seed']))
b=[e for e in tr if e['question']['type']=='binary']; ml=[e for e in tr if e['question']['type']=='multilabel']
audit['selected_training']={'n':len(tr),'validation_n':len(va),'types':dict(Counter(e['question']['type'] for e in tr)),
 'binary_positive':sum(e['target'] for e in b),'binary_n':len(b),'multilabel_positive':sum(len(e['target']) for e in ml),
 'multilabel_labels':sum(len(e['question']['candidates']) for e in ml),'binary_by_family':{f:{'n':len(es),'positive':sum(e['target'] for e in es)} for f in sorted({e['family'] for e in b}) if (es:=[e for e in b if e['family']==f])}}
audit['paired']={}
for an,bn in [('baseline','lora_pilot'),('lora_pilot','lora_4b'),('lora_4b','lora_8b'),('lora_4b','jev'),('lora_8b','jev')]:
    a={r['id']:r['correct'] for r in reports[an]['predictions']};b={r['id']:r['correct'] for r in reports[bn]['predictions']}
    aa=sum(a[i] and not b[i] for i in a);bb=sum(b[i] and not a[i] for i in a);n=aa+bb
    audit['paired'][an+' vs '+bn]={'only_a':aa,'only_b':bb,'p_exact_question_level':min(1.,2*sum(math.comb(n,k) for k in range(min(aa,bb)+1))/2**n)}
for p in Path('reports/bench').glob('*/bench.json'):
    r=json.loads(p.read_text()); audit['benchmarks'][p.parent.name]={'meta':r['meta'],'rows':r['rows'],'sha256':sha256_file(p)}

# Reconstruct the exact cached external requests; compare parsed responses to published predictions.
spec=importlib.util.spec_from_file_location('external_review',ROOT/'scripts/compare_external.py')
ext=importlib.util.module_from_spec(spec);spec.loader.exec_module(ext)
groups={}
for e in load('reports/external/full/subset.jsonl'):
    groups.setdefault(e['source_id'],(e['state'],[]))[1].append(e)
audit['external_cache']={}
for name,kind,model,file in [('jev','jev','~typesafe/jev-latest','typesafe_jev-latest'),('astra','llm','openai/gpt-6-astra','openai_gpt-6-astra')]:
    cache={r['key']:r for r in map(json.loads,open(f'reports/external/cache/{file}.jsonl'))}
    old={r['id']:r for r in reports[name]['predictions']};stats=Counter();models=Counter();cost=0.;totals=[]
    for sid,(state,exs) in groups.items():
        body,keys=ext.jev_request(model,state,exs) if kind=='jev' else ext.llm_request(model,state,exs,'low')
        key=hashlib.sha256(json.dumps(body,sort_keys=True).encode()).hexdigest()[:16]
        if key not in cache: stats['missing_request_keys']+=1;continue
        resp=cache[key]['response'];models[resp.get('model','?')]+=1;cost+=ext.call_cost(resp)
        ans=resp['answers'] if kind=='jev' else json.loads(resp['choices'][0]['message']['content'])
        for ex,(eid,ks) in zip(exs,keys):
            parsed=ext.to_row(ex,old[eid],kind,[ans[k] for k in ks]);stats['questions_checked']+=1
            assert all(parsed[k]==old[eid][k] for k in ['selected','probabilities','correct']), (name,eid)
            for p in parsed['probabilities']:
                stats['invalid_parsed_probabilities']+=not math.isfinite(p) or not 0<=p<=1
            if ex['question']['type']=='multiclass':
                raw=ans[ks[0]]['probabilities'] if kind=='jev' else ans[ks[0]]
                cs=[c['id'] for c in ex['question']['candidates']]
                stats['missing_choice_probability_keys']+=sum(c not in raw for c in cs)
                vals=[raw.get(c,0) for c in cs]
                stats['all_zero_choice_vectors']+=sum(vals)==0
                stats['invalid_raw_choice_probabilities']+=sum(not math.isfinite(v) or not 0<=v<=1 for v in vals)
                stats['hard_choice_vectors']+=all(v in (0,1) for v in vals)
                if kind=='jev':stats['returned_choice_disagrees_with_scored_argmax']+=ans[ks[0]].get('choice')!=parsed['selected']
    audit['external_cache'][name]={'counts':dict(stats),'resolved_models':dict(models),'summed_matched_cached_call_cost_usd':cost}

audit['source_sha256']={str(p):sha256_file(p) for d in ['src/personal_jev','tests','scripts','configs'] for p in Path(d).rglob('*') if p.is_file() and p.suffix in ['.py','.sh','.json']}
audit['source_sha256']|={str(p):sha256_file(p) for p in [Path('README.md'),Path('docs/custom_model.md')]}
(OUT/'audit.json').write_text(json.dumps(audit,indent=2))
print(json.dumps({'reports_checked':len(reports),'selected_training':audit['selected_training'],'paired':audit['paired'],
                 'cross_split_groups':len(cross),'train_test_exact_groups':audit['train_test_exact_groups'],
                 'external_cache':audit['external_cache']},indent=2))
