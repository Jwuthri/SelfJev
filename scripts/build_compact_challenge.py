"""Frozen, programmatically labeled challenge. Never used for fitting or selection.

This tests narrow explicit-record reasoning, not general human-authored quality.
Each source contains independent questions and known evidence/absence contrasts.
"""
import json
import random
from pathlib import Path

from personal_jev.data import expand_source, load, sha256_file, write_jsonl

rng=random.Random(902413)
rows=[]
teams=['cedar','marble','orchid']
names=['Keira','Ronan','Imani','Basil','Petra','Lucian','Sora','Tamsin']
for i in range(120):
    person=rng.choice(names); amount=rng.choice([24,49,50,51,74,75,76,99]); cutoff=rng.choice([50,75])
    verified=bool(rng.randrange(2)); cancelled=bool(rng.randrange(2)); team=rng.choice(teams)
    manager=rng.choice(['approved','rejected','unmentioned'])
    state=(f'Record ZX-{19000+i} concerns {person}. The assigned team is {team}. '
           f'The claimed expense is {amount} credits. Identity verification is {"complete" if verified else "incomplete"}. '
           f'The delivery is explicitly {"cancelled" if cancelled else "not cancelled"}. '
           f'Policy: reimbursement is permitted if and only if identity verification is complete AND the expense is at most {cutoff} credits. ')
    if manager!='unmentioned': state+=f'The manager has {manager} the request. '
    state+='A separate record, ZX-18000, has 200 credits and belongs to team copper. Its facts do not apply to this record.'
    candidates=[{'id':t,'description':f'The assigned team is {t}.'} for t in teams]
    offered=rng.sample(teams,2)
    def binary(q,target,tags):return {'type':'binary','instruction':q,'target':target,'hard_cases':tags}
    qs=[binary(f'Does record ZX-{19000+i} explicitly say the delivery is cancelled?',cancelled,['negation']),
        binary(f'Under the stated policy, is reimbursement permitted for record ZX-{19000+i}?',verified and amount<=cutoff,['conditional_policy']),
        binary(f'Does the text explicitly confirm that the manager approved record ZX-{19000+i}?',manager=='approved',['missing_evidence']),
        {'type':'multiclass','instruction':f'Which team is assigned to record ZX-{19000+i}?','candidates':candidates,'target':team},
        {'type':'multiclass','instruction':f'Choose the assigned team for record ZX-{19000+i}; choose none if the assigned team is absent from the offered options.',
         'candidates':[c for c in candidates if c['id'] in offered]+[{'id':'none','description':'None of the offered team options is the assigned team.'}],
         'target':team if team in offered else 'none','hard_cases':['none_of_the_above']},
        {'type':'multilabel','instruction':f'Select all facts explicitly supported for record ZX-{19000+i}.',
         'candidates':[{'id':'verified','description':'Identity verification is complete.'},
                       {'id':'cancelled','description':'The delivery is cancelled.'},
                       {'id':'approved','description':'The manager has approved the request.'}],
         'target':[k for k,v in [('verified',verified),('cancelled',cancelled),('approved',manager=='approved')] if v]}]
    for j,q in enumerate(qs):
        q['id']=f'q{j}'
    rows.append({'source_id':f'compact-challenge-{i:03d}','family':'compact_fresh_rules','state':state,'questions':qs,
                 'split':'test','provenance':'programmatic:build_compact_challenge.py; seed=902413'})
path=Path('data/compact_challenge_v1.jsonl')
if path.exists(): raise SystemExit('Challenge already frozen; refusing to overwrite')
examples=[e for row in rows for e in expand_source(row)]
known={e['state'] for e in load(['data/hf.jsonl','data/synthetic.jsonl','data/eval.jsonl'])}
assert not known.intersection(e['state'] for e in examples)
write_jsonl(path,rows)
print(json.dumps({'path':str(path),'sha256':sha256_file(path),'sources':len(rows),'questions':len(examples)}))
