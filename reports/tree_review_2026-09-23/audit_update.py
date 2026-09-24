import json, hashlib, random
from pathlib import Path
from collections import Counter, defaultdict
import numpy as np
from math import comb
def exact_binomial_p(wins, total):
 return min(1.0, 2 * sum(comb(total, k) for k in range(min(wins, total-wins)+1)) / 2**total)
from personal_jev.data import load, sha256_file
from personal_jev.evaluate import evaluate_predictions
ROOT=Path.cwd();OUT=ROOT/'reports/tree_review_2026-09-23'
paths={n:f'reports/{n}/test/report.json' for n in ['lora_4b','tree_4b','tree_4b_instruct','lora_8b','curve/instruct_lora','tree_4b_r2']}
paths|={'jev':'reports/external/full/typesafe_jev-latest/report.json','astra':'reports/external/full/openai_gpt-6-astra/report.json'}
reports={n:json.loads(Path(p).read_text()) for n,p in paths.items()}
preds={n:{r['id']:r for r in d['predictions']} for n,d in reports.items()}
ids=list(preds['tree_4b']);data={e['id']:e for e in load(['data/hf.jsonl','data/eval.jsonl'],{'test'})}
assert len(ids)==3471 and set(ids)==set(data)
for n,ps in preds.items():
 assert set(ps)==set(ids)
 for k in ids:
  r=ps[k];b=preds['tree_4b'][k]
  assert all(r[a]==b[a] for a in ['target','type','candidate_ids'])
  ok=set(r['selected'])==set(r['target']) if r['type']=='multilabel' else r['selected']==r['target']
  assert bool(r['correct'])==ok
 metrics=evaluate_predictions(list(ps.values()))
 assert all(abs(metrics[t][m]-reports[n]['metrics'][t][m])<1e-12 for t,m in [('binary','auroc'),('multiclass','accuracy'),('multilabel','exact_match')])
summary={}
for n,d in reports.items():
 ps=preds[n];m=d['metrics'];slices={}
 for prefix in ['hf_','heldout_','eval_']:
  pp=[p for p in ps.values() if p['family'].startswith(prefix)];slices[prefix]={'n':len(pp),'correct':sum(p['correct'] for p in pp),'accuracy':sum(p['correct'] for p in pp)/len(pp)}
 summary[n]={'overall':m['question_accuracy'],'correct':sum(r['correct'] for r in ps.values()),'binary_acc':m['binary']['accuracy'],'binary_auroc':m['binary']['auroc'],'mc_acc':m['multiclass']['accuracy'],'ml_em':m['multilabel']['exact_match'],'ml_f1':m['multilabel']['micro_f1'],'binary_brier':m['binary']['brier'],'binary_ece':m['binary']['ece'],'slices':slices}
# Paired bootstrap resamples normalized-document groups, preserving questions from the same document.
groups=defaultdict(list)
for i,k in enumerate(ids):groups[' '.join(data[k]['state'].split()).lower()].append(i)
sizes=np.array([len(v) for v in groups.values()]);a=np.array([int(preds['tree_4b'][k]['correct']) for k in ids]);comparisons={}
for name in ['lora_4b','tree_4b_instruct','lora_8b','jev','astra','tree_4b_r2']:
 b=np.array([int(preds[name][k]['correct']) for k in ids]);diff=a-b
 wins=int(((a==1)&(b==0)).sum());losses=int(((a==0)&(b==1)).sum())
 gdiff=np.array([diff[v].sum() for v in groups.values()]);rng=np.random.default_rng(42);draws=[]
 for j in range(20):
  ix=rng.integers(0,len(sizes),size=(500,len(sizes)));draws.extend((gdiff[ix].sum(axis=1)/sizes[ix].sum(axis=1)).tolist())
 comparisons[name]={'tree_only':wins,'other_only':losses,'delta_pp':100*float(diff.mean()),'question_mcnemar_p':exact_binomial_p(wins,wins+losses),'document_bootstrap_95_pp':[100*float(x) for x in np.quantile(draws,[.025,.975])]}
by_family=[]
for f in reports['tree_4b']['by_family']:
 ks=[k for k in ids if preds['tree_4b'][k]['family']==f]
 vals={n:sum(preds[n][k]['correct'] for k in ks)/len(ks) for n in ['lora_4b','tree_4b','tree_4b_instruct','tree_4b_r2','jev']}
 by_family.append({'family':f,'n':len(ks),'net_vs_stock':sum(int(preds['tree_4b'][k]['correct'])-int(preds['lora_4b'][k]['correct']) for k in ks),**vals})
# Difference by output mode is valuable for locating the remaining failure.
by_type={}
for t in ['binary','multiclass','multilabel']:
 ks=[k for k in ids if preds['tree_4b'][k]['type']==t]
 by_type[t]={'n':len(ks),**{n:sum(preds[n][k]['correct'] for k in ks) for n in ['lora_4b','tree_4b','jev']}}
bench={}
for suffix in ['bf16','long_bf16']:
 tree=json.loads(Path(f'reports/bench/gpu_tree_4b_{suffix}/bench.json').read_text());stock=json.loads(Path(f'reports/bench/gpu_stock_lora_4b_{suffix}/bench.json').read_text())
 key=lambda r:(r['state_tokens'],r['questions'],r['candidates'],r['type'])
 ss={key(r):r for r in stock['rows']}
 bench[suffix]={'prompt_tree':tree['meta']['prompt'],'prompt_stock':stock['meta']['prompt'],'adapter_hashes_match_quality':tree['meta']['adapter_sha256']==reports['tree_4b']['meta']['adapter_sha256'] and stock['meta']['adapter_sha256']==reports['lora_4b']['meta']['adapter_sha256'],'rows':[]}
 for r in tree['rows']:
  s=ss.get(key(r));bench[suffix]['rows'].append({'shape':key(r),'tree_ms':r['e2e_ms_p50'],'stock_ms':s['e2e_ms_p50'] if s else None,'speedup':s['e2e_ms_p50']/r['e2e_ms_p50'] if s else None,'samples_tree':r['repeats'],'samples_stock':s['repeats'] if s else None})
cal=json.loads(Path('reports/tree_4b/test_calibrated/report.json').read_text())['metrics']
hard=load('data/hardcases.jsonl')
result={'reports':summary,'aligned_ids_targets_candidates':len(ids),'document_groups':len(groups),'comparisons':comparisons,'by_family':by_family,'correct_by_type':by_type,'bench':bench,'calibrated_tree':{k:cal[k] for k in ['question_accuracy']}|{t:{k:v for k,v in cal[t].items() if k in ['accuracy','exact_match','micro_f1','ece','brier']} for t in ['binary','multiclass','multilabel']},'hardcase_data':{'n':len(hard),'splits':dict(Counter(e['split'] for e in hard)),'types':dict(Counter(e['question']['type'] for e in hard))},'source_sha256':{p:sha256_file(p) for p in paths.values()}}
clinc=[k for k in ids if preds['tree_4b'][k]['family']=='heldout_intent_clinc']
closs=[k for k in clinc if preds['tree_4b'][k]['correct'] and not preds['tree_4b_r2'][k]['correct']]
cgain=[k for k in clinc if not preds['tree_4b'][k]['correct'] and preds['tree_4b_r2'][k]['correct']]
result['r2_clinc_diagnosis']={'n':len(clinc),'r1_only':len(closs),'r2_only':len(cgain),'r2_predictions_on_lost_questions':dict(Counter(preds['tree_4b_r2'][k]['selected'] for k in closs)),'lost_ids':closs,'by_run':{}}
for n in ['tree_4b','tree_4b_r2']:
 pp=[preds[n][k] for k in clinc];inscope=[r for r in pp if r['target']!='none']
 def best_non_none(r):
  return max((c for c in r['candidate_ids'] if c!='none'),key=lambda c:r['scores'][r['candidate_ids'].index(c)])
 result['r2_clinc_diagnosis']['by_run'][n]={'selected_none':sum(r['selected']=='none' for r in pp),'true_none':sum(r['target']=='none' for r in pp),'inscope_n':len(inscope),'best_non_none_correct_inscope':sum(best_non_none(r)==r['target'] for r in inscope),'none_gold_correct':sum(r['selected']=='none' and r['target']=='none' for r in pp)}
(OUT/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result['r2_clinc_diagnosis'],indent=2))
