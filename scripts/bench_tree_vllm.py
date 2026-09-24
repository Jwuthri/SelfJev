"""Cold-prefix/warm-prefix vLLM timings plus raw-score and full quality checks."""
import argparse
import json
import random
import statistics
import time
from pathlib import Path

from personal_jev.benchmark import make_request
from personal_jev.classify import classify
from personal_jev.data import load
from personal_jev.evaluate import breakdowns, evaluate_predictions, predict
from personal_jev.schemas import parse_request
from personal_jev.vllm_tree import VllmTreeScorer
from tree_latency_experiment import OUT, flatten, metadata, save


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--model-dir',default='runs/tree_4b/merged')
    ap.add_argument('--out',default=str(OUT/'vllm_a10g.json'));ap.add_argument('--repeats',type=int,default=10)
    ap.add_argument('--reference-parity',default=str(OUT/'parity_a10g.json'))
    ap.add_argument('--reference-eval',default=str(OUT/'r1_merged_development.json'))
    ap.add_argument('--document-warm',action='store_true',help='Also time new branches after pre-filling only the document root')
    ap.add_argument('--skip-quality',action='store_true',help='Timing extension only; quality remains in the original report')
    a=ap.parse_args()
    sc=VllmTreeScorer(a.model_dir)
    report={'meta':metadata(sc),'rows':[], 'protocol':{
        'cold_prefix':'Clear all prefix cache entries before the measured request',
        'warm_prefix':'Repeat the entire identical request, including questions and candidates',
        'warm_document':'Clear cache; prefill only root tokens; measure full request with new branches',
        'reference_parity':a.reference_parity,'reference_eval':a.reference_eval}}
    examples=load(['data/hf.jsonl','data/eval.jsonl'],{'validation'})
    random.Random(8431).shuffle(examples)
    reqs=[{'state':e['state'],'questions':[{'id':'q',**e['question']}]} for e in examples[:96]]
    reqs += [make_request(sc.tokenizer,n,q,3) for n in (8,512,2048,8192) for q in (1,16)]
    ref_data=json.loads(Path(a.reference_parity).read_text())
    assert ref_data['meta']['scorer']['prompt_sha']==sc.meta['prompt_sha'], 'Parity reference format mismatch'
    refs=ref_data['requests']
    assert len(reqs)==len(refs)
    diffs=[]
    for i,(req,ref) in enumerate(zip(reqs,refs)):
        r=classify(sc,req);s=flatten(r)
        assert len(s)==len(ref['optimized'])
        ds=[abs(x-y) for x,y in zip(s,ref['optimized'])]
        diffs.append({'i':i,'scores':s,'reference':ref['optimized'],'max_abs_diff':max(ds),'stats':r['meta']})
    report['parity']={'requests':diffs,'max_abs_diff':max(d['max_abs_diff'] for d in diffs)}
    save(a.out,report);print({'parity_max':report['parity']['max_abs_diff']},flush=True)
    if report['parity']['max_abs_diff'] > 1.0:
        raise RuntimeError('Raw-score mismatch is too large: inspect activation/head/token formatting before benchmarking')
    for n in (8,512,2048,8192):
        for nq in (1,4,16):
            req=make_request(sc.tokenizer,n,nq,3)
            trees,_=sc.trees([parse_request(req)])
            roots=[{'prompt_token_ids':t['ids'][:t['root']]} for t in trees]
            for _ in range(2):classify(sc,req)
            runs=[]
            for rep in range(a.repeats):
                # Explicit reset avoids relying on a nonce to invalidate all exact-prefix reuse.
                assert sc.llm.reset_prefix_cache()
                for mode in ('cold_prefix','warm_prefix'):
                    t=time.perf_counter();r=classify(sc,req)
                    runs.append({'rep':rep,'mode':mode,'wall_ms':1000*(time.perf_counter()-t),
                                 'stats':r['meta'],'scores':flatten(r)})
                if a.document_warm:
                    assert sc.llm.reset_prefix_cache()
                    t_prefill=time.perf_counter()
                    root_outputs=sc.llm.classify(roots,pooling_params=sc.params,use_tqdm=False)
                    root_prefill_ms=1000*(time.perf_counter()-t_prefill)
                    t=time.perf_counter();r=classify(sc,req)
                    runs.append({'rep':rep,'mode':'warm_document','wall_ms':1000*(time.perf_counter()-t),
                                 'root_prefill_ms':root_prefill_ms,
                                 'root_prefill_cached_tokens':[getattr(o,'num_cached_tokens',None) for o in root_outputs],
                                 'stats':r['meta'],'scores':flatten(r)})
            row={'state_tokens':n,'questions':nq,'candidates':3,'runs':runs,
                 **{mode+'_median_ms':statistics.median(r['wall_ms'] for r in runs if r['mode']==mode)
                    for mode in ('cold_prefix','warm_prefix',*(['warm_document'] if a.document_warm else []))}}
            report['rows'].append(row);save(a.out,report)
            print({k:v for k,v in row.items() if k!='runs'},flush=True)
    if a.skip_quality:
        report['quality_note']='Not repeated for this timing extension; use the prior matched quality report'
        save(a.out,report)
        return
    preds=[]
    ex=load(['data/hf.jsonl','data/eval.jsonl'],{'test'})
    for k in range(0,len(ex),128):
        p,_=predict(sc,ex[k:k+128]);preds.extend(p)
    report['development']={'metrics':evaluate_predictions(preds),'breakdowns':breakdowns(preds),'predictions':preds}
    ref_data=json.loads(Path(a.reference_eval).read_text())
    assert ref_data['meta']['scorer']['prompt_sha']==sc.meta['prompt_sha'], 'Quality reference format mismatch'
    ref=ref_data['predictions']
    byid={r['id']:r for r in ref}
    report['development']['reference_decision_flips']=[r['id'] for r in preds if r['selected']!=byid[r['id']]['selected']]
    save(a.out,report)
    print({'development_accuracy':report['development']['metrics']['question_accuracy'],
           'decision_flips':len(report['development']['reference_decision_flips'])},flush=True)


if __name__=='__main__':main()
