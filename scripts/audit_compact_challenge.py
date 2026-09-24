"""Check frozen challenge labels against the serialized text; report pre-defined diagnostic slices."""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from personal_jev.data import expand_source, sha256_file

P=Path('reports/latency_optimization_2026-09-24')
DATA=Path('data/compact_challenge_v1.jsonl')


def main():
    records=[json.loads(line) for line in DATA.read_text().splitlines()]
    slices=defaultdict(list);counts=Counter();n=0
    for row in records:
        s=row['state']
        team=re.search(r'The assigned team is (\w+)\.',s)[1]
        amount=int(re.search(r'The claimed expense is (\d+) credits\.',s)[1])
        cutoff=int(re.search(r'expense is at most (\d+) credits\.',s)[1])
        verified=re.search(r'Identity verification is (complete|incomplete)\.',s)[1]=='complete'
        cancelled=re.search(r'The delivery is explicitly (not cancelled|cancelled)\.',s)[1]=='cancelled'
        manager=re.search(r'The manager has (approved|rejected) the request\.',s)
        manager=manager[1] if manager else 'unmentioned'
        examples=expand_source(row)
        for j,ex in enumerate(examples):
            offered=[c['id'] for c in ex['question'].get('candidates',[])]
            expected=[cancelled,verified and amount<=cutoff,manager=='approved',team,
                      team if team in offered else 'none',
                      [k for k,v in [('verified',verified),('cancelled',cancelled),('approved',manager=='approved')] if v]][j]
            assert ex['target']==expected,(ex['id'],ex['target'],expected)
            slices[f'question_{j}'].append(ex['id']);n+=1
            if j==0:slices[f'delivery:{"cancelled" if cancelled else "not_cancelled"}'].append(ex['id'])
            if j==1:
                slices[f'policy:verified={verified},within_limit={amount<=cutoff}'].append(ex['id'])
                if amount==cutoff:slices['policy:exact_boundary'].append(ex['id'])
            if j==2:slices[f'manager:{manager}'].append(ex['id'])
            if j==4:slices[f'rejection:{"none" if expected=="none" else "offered_team"}'].append(ex['id'])
        counts['manager:'+manager]+=1
        counts['policy_permitted' if verified and amount<=cutoff else 'policy_not_permitted']+=1
    result={'data_sha256':sha256_file(DATA),'sources':len(records),'questions_checked':n,
            'method':'Labels checked by parsing serialized state text independently of generator variables',
            'source_counts':dict(counts),'slices':{k:{'n':len(ids),'ids':ids} for k,ids in slices.items()}}
    # Models are evaluated only after checkpoint selection; these optional reads do not fit or select anything.
    for model,file in [('r1','r1_fresh.json'),('compact','compact_fresh.json')]:
        f=P/file
        if f.exists():
            pred={r['id']:r for r in json.loads(f.read_text())['predictions']}
            for name,ids in slices.items():
                result['slices'][name][model+'_accuracy']=sum(pred[i]['correct'] for i in ids)/len(ids)
    (P/'challenge_audit.json').write_text(json.dumps(result,indent=1))
    print({k:v for k,v in result.items() if k!='slices'})


if __name__=='__main__':main()
