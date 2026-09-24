"""Reproducible phase-one latency/parity, teacher targets, and phase-two evaluation.

Run from the repository root with PYTHONPATH=src. Artifacts include every timed
repetition and score; no provider APIs or generated labels are used.
"""
import argparse
import datetime
import gc
import importlib.util
import json
import random
import statistics
import time
from pathlib import Path

import torch

from personal_jev.benchmark import make_request
from personal_jev.classify import classify, classify_many
from personal_jev.data import load, sha256_file
from personal_jev.evaluate import breakdowns, evaluate_predictions, predict
from personal_jev.schemas import parse_request
from personal_jev.train import hardware, select_data
from personal_jev.train_tree import DEFAULTS, encode_items, score_items
from personal_jev.tree import RERANKER_4B, Encoder, TreeModel, TreeScorer, leaf_paths

OUT = Path("reports/latency_optimization_2026-09-24")


def save(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=1))


def old_model(lm, pad):
    spec = importlib.util.spec_from_file_location("personal_jev._tree_original", OUT / "baseline_source/tree.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.TreeModel(lm, pad)


def scorer(a):
    return TreeScorer(*RERANKER_4B, adapter=a.adapter, dtype="bfloat16", merge=not getattr(a, "unmerged", False),
                      max_batch_tokens=8192, max_batch_size=16)


def metadata(sc):
    import peft, transformers
    gpu=torch.cuda.get_device_properties(0)
    return {"scorer":sc.meta, "created_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "hardware":hardware("cuda") | {"gpu_name":gpu.name,"gpu_memory_bytes":gpu.total_memory,
                                       "gpu_compute_capability":[gpu.major,gpu.minor]}, "versions":{
        "torch":torch.__version__,"transformers":transformers.__version__,"peft":peft.__version__},
        "code_sha256":{str(p):sha256_file(p) for p in Path("src/personal_jev").glob("*.py")}}


def flatten(result):
    return [q["score"] if q["type"] == "binary" else c["score"]
            for q in result["questions"] for c in ([None] if q["type"] == "binary" else q["candidates"])]


def bench(a):
    sc = scorer(a)
    if a.original:
        sc.model = old_model(sc.model.lm, sc.tokenizer.pad_token_id)
    report = {"meta":metadata(sc),"original_mask":a.original,"repeats":a.repeats,"rows":[]}
    # Resident model, no persistent document KV cache in this HF path.
    for n in (8, 512, 2048, 8192):
        for nq in (1, 4, 16):
            req = make_request(sc.tokenizer,n,nq,3)
            for _ in range(2): classify(sc,req)
            runs=[]
            for rep in range(a.repeats):
                torch.cuda.synchronize()
                t=time.perf_counter(); r=classify(sc,req); torch.cuda.synchronize()
                runs.append({"rep":rep,"wall_ms":1000*(time.perf_counter()-t),"stats":r["meta"],"scores":flatten(r)})
            row={"state_tokens":n,"questions":nq,"candidates":3,"runs":runs,
                 "median_ms":statistics.median(r["wall_ms"] for r in runs)}
            report["rows"].append(row);save(a.out,report)
            print(json.dumps({k:v for k,v in row.items() if k!='runs'}),flush=True)
    if a.profile and not a.original:
        req=make_request(sc.tokenizer,2048,16,3)
        with torch.profiler.profile(activities=[torch.profiler.ProfilerActivity.CPU,torch.profiler.ProfilerActivity.CUDA],
                                    record_shapes=True,profile_memory=True) as p:
            classify(sc,req)
            torch.cuda.synchronize()
        p.export_chrome_trace(str(Path(a.out).with_suffix('.trace.json')))
        Path(a.out).with_suffix('.profile.txt').write_text(p.key_averages().table(sort_by="self_cuda_time_total",row_limit=50))


def parity(a):
    sc=scorer(a)
    original=old_model(sc.model.lm,sc.tokenizer.pad_token_id)
    examples=load(["data/hf.jsonl","data/eval.jsonl"],{"validation"})
    rng=random.Random(8431);rng.shuffle(examples)
    reqs=[{"state":e["state"],"questions":[{"id":"q",**e["question"]}]} for e in examples[:96]]
    reqs += [make_request(sc.tokenizer,n,q,3) for n in (8,512,2048,8192) for q in (1,16)]
    records=[]
    with torch.inference_mode():
        for i, req in enumerate(reqs):
            trees,_=sc.trees([parse_request(req)])
            before=original.cached(trees).tolist();after=sc.model.cached(trees).tolist()
            records.append({"i":i,"original":before,"optimized":after,"max_abs_diff":max(abs(x-y) for x,y in zip(before,after))})
    result={"meta":metadata(sc),"requests":records,"max_abs_diff":max(r["max_abs_diff"] for r in records)}
    save(a.out,result)
    print({"parity_max_abs_diff":result["max_abs_diff"],"requests":len(records)},flush=True)
    assert result["max_abs_diff"] <= 1e-5


def teacher(a):
    cfg=DEFAULTS|json.loads(Path(a.config).read_text())
    sc=scorer(a)
    examples,_=select_data(cfg,random.Random(cfg["seed"]))
    # Filter using the student's actual path lengths, then use old-format teacher paths.
    student_items,_,_=encode_items(Encoder(sc.tokenizer,RERANKER_4B[0],cfg["format_name"]),examples,cfg["max_length"])
    keep={it["id"] for it in student_items};examples=[e for e in examples if e["id"] in keep]
    items,roots,dropped=encode_items(sc.enc,examples,32768)
    assert not dropped
    scores=score_items(sc.model,items,roots,8192,progress=lambda done,total: print(f'teacher batch {done}/{total}',flush=True))
    save(a.out,{"meta":metadata(sc),"splits":["train"],"student_format":cfg["format_name"],
                "data":{p:sha256_file(p) for p in cfg["train_files"]},"scores":{
                    it["id"]:{"scores":s,"candidate_ids":it["candidate_ids"]} for it,s in zip(items,scores)}})
    print({"teacher_questions":len(items)},flush=True)


def evaluate(a):
    sc=scorer(a)
    ex=load(a.data,{a.split})
    t=time.perf_counter()
    preds,stats=predict(sc,ex)
    result={"meta":metadata(sc),"split":a.split,"files":{p:sha256_file(p) for p in a.data},
            "metrics":evaluate_predictions(preds),"breakdowns":breakdowns(preds),"predictions":preds,
            "stats":stats,"wall_s":time.perf_counter()-t}
    save(a.out,result)
    print({"out":a.out,"n":len(preds),"accuracy":result["metrics"]["question_accuracy"]},flush=True)


if __name__ == '__main__':
    ap=argparse.ArgumentParser();ap.add_argument('action',choices=['bench','parity','teacher','eval'])
    ap.add_argument('--adapter',default='runs/tree_4b/adapter');ap.add_argument('--out',required=True)
    ap.add_argument('--original',action='store_true');ap.add_argument('--unmerged',action='store_true')
    ap.add_argument('--repeats',type=int,default=10);ap.add_argument('--profile',action='store_true')
    ap.add_argument('--config');ap.add_argument('--data',nargs='+',default=['data/hf.jsonl','data/eval.jsonl'])
    ap.add_argument('--split',default='test')
    a=ap.parse_args();globals()[{'eval':'evaluate'}.get(a.action,a.action)](a)
