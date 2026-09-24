"""Actual-checkpoint equivalence before training; scores are not used for selection."""
import gc,json
from pathlib import Path
import torch
from personal_jev.t5_shared import T5SharedScorer
from personal_jev.schemas import parse_request
from personal_jev.benchmark import make_request
from personal_jev.data import load
from personal_jev.model import InputTooLong
from run_challenger import items,save
out=Path('reports/t5_round2b_2026-09-24')
sc=T5SharedScorer(dtype='float32',branch_batch=4)
rows=[]
for length in [64,1024]:
    req=parse_request(make_request(sc.tokenizer,length,3,3))
    es=[sc.entry(req.state,q) for q in req.questions]
    with torch.no_grad():
        native=sc.t5_forward(es,share=False);shared=sc.shared_entries(es)
        counts=dict(sc.last_counts);single=torch.cat([sc.shared_entries([e]) for e in es])
        reversed_scores=sc.shared_entries(es[::-1]).reshape(3,3).flip(0).flatten()
    row={'state_tokens':length,'max_native_shared_diff':float((native-shared).abs().max()),
        'max_single_shared_diff':float((single-shared).abs().max()),
        'question_permutation_diff':float((reversed_scores-shared).abs().max()),'counts':counts}
    rows.append(row);print(row,flush=True)
    assert max(row[k] for k in ['max_native_shared_diff','max_single_shared_diff','question_permutation_diff'])<0.005
old=sc.max_length;sc.max_length=16
try:
    sc.entry(req.state,req.questions[0]);raise AssertionError('overlength accepted')
except InputTooLong:pass
sc.max_length=old
save(out/'actual_fp32_checks.json',{'rows':rows,'overlength_rejected':True})
selection=json.loads((out/'selection.json').read_text());checks={}
for split in ['train','validation']:
    ex=load([selection[split]['file']],{split});sc.max_length=16384
    encoded,dropped=items(sc,ex);assert not dropped,dropped
    checks[split]={'n':len(ex),'max_combined_tokens':max(e['entry']['length'] for e in encoded),'dropped':dropped}
save(out/'t5_eligibility.json',checks);print('ELIGIBILITY',checks,flush=True)
