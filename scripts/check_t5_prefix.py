"""Validate the additional native decoder prefix sharing before benchmarking it."""
import gc,json
from pathlib import Path
import torch
from personal_jev.t5_shared import T5SharedScorer
from personal_jev.benchmark import make_request
from personal_jev.schemas import parse_request
from personal_jev.data import load
from personal_jev.train import question_correct
from run_challenger import items,save
root=Path('reports/t5_round2b_2026-09-24')
sc=T5SharedScorer(dtype='float32',branch_batch=48)
r=parse_request(make_request(sc.tokenizer,1024,3,3))
es=[sc.entry(r.state,q) for q in r.questions]
with torch.no_grad():
    native=sc.t5_forward(es,share=False)
    shared=sc.shared_entries(es)
    sc.decoder_prefix=True;prefix=sc.shared_entries(es)
    independently=torch.cat([sc.shared_entries([e]) for e in es])
    one=es[0]|{'branches':[es[0]['branches'][0]],'n':1}
    full_lm=sc.base()(input_ids=torch.tensor([one['root']],device='cuda'),
        decoder_input_ids=torch.tensor(one['branches'],device='cuda'),use_cache=False,logits_to_keep=1).logits[0,-1]
    official=full_lm[sc.answer_ids[0]]-full_lm[sc.answer_ids[1]]
    direct=sc.t5_forward([one])[0]
result={'fp32':{'native_lm_head_max_abs':float((official-direct).abs()),'native_prefix_max_abs':float((native-prefix).abs().max()),
    'shared_prefix_max_abs':float((shared-prefix).abs().max()),
    'independent_prefix_max_abs':float((independently-prefix).abs().max())}}
save(root/'decoder_prefix_checks.json',result)
assert max(result['fp32'].values())<.005,result
del sc,native,shared,prefix,independently,full_lm,official,direct;gc.collect();torch.cuda.empty_cache()
sc=T5SharedScorer(adapter='runs/t5gemma2_r2b_full/adapter',merge=True,branch_batch=48)
data,dropped=items(sc,load(['runs/t5_round2b_inputs/validation.jsonl'],{'validation'})[:64]);assert not dropped
rows=[]
for it in data:
    sc.decoder_prefix=False;a=sc.shared_entries([it['entry']]).tolist()
    sc.decoder_prefix=True;b=sc.shared_entries([it['entry']]).tolist()
    def pred(scores):
        if it['type']=='binary':return scores[0]>=0
        if it['type']=='multiclass':return max(range(len(scores)),key=lambda i:scores[i])
        return [s>=0 for s in scores]
    rows.append({'id':it['id'],'max_abs_score_diff':max(abs(x-y) for x,y in zip(a,b)),
                 'decisions_equal':pred(a)==pred(b),'full_correct':question_correct(a,it),'prefix_correct':question_correct(b,it),
                 'full_scores':a,'prefix_scores':b})
result['trained_bf16_validation']={'n':len(rows),'decision_changes':sum(not r['decisions_equal'] for r in rows),
    'max_abs_score_diff':max(r['max_abs_score_diff'] for r in rows),'rows':rows}
save(root/'decoder_prefix_checks.json',result)
print('PREFIX_CHECKS',result['fp32'],{k:v for k,v in result['trained_bf16_validation'].items() if k!='rows'},flush=True)
