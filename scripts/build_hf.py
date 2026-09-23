"""Convert pinned public Hugging Face datasets into project JSONL -> data/hf.jsonl.

Train families contribute train (from the original train file) plus validation/calibration/test (from the
original eval file). Held-out families contribute test only, so they measure generalisation to task
families never seen in training. Label ids are the dataset's label names; the model sees descriptions from
data/hf/label_descriptions.json (train randomly uses the humanised name instead, 50/50, so the model does
not learn one wording per id). Public datasets may overlap with the base model's own training data.

usage: uv run python scripts/build_hf.py [--train-per-dataset 2400]
"""
import argparse
import functools
import json
import random
import sys
from pathlib import Path

import pyarrow.parquet as pq
from huggingface_hub import hf_hub_download

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from personal_jev.data import validate_example, write_jsonl  # noqa: E402

LABELS = json.loads((ROOT / "data/hf/labels.json").read_text())
DESC_PATH = ROOT / "data/hf/label_descriptions.json"
DESC = json.loads(DESC_PATH.read_text()) if DESC_PATH.exists() else {}
NOTA = {"id": "none", "description": "None of the above: the request matches none of the other options"}

# name: repo, pinned revision, license, role, family, {our split source: file}
SOURCES = {
    "banking77": ("mteb/banking77", "18072d2685ea682290f7b8924d94c62acc19c0b2", "CC-BY-4.0 (PolyAI)", "train", "hf_intent_banking77",
                  {"train": "data/train-00000-of-00001.parquet", "eval": "data/test-00000-of-00001.parquet"}),
    "go_emotions": ("google-research-datasets/go_emotions", "add492243ff905527e67aeb8b80c082af02207c3", "Apache-2.0", "train", "hf_emotions_multilabel",
                    {"train": "simplified/train-00000-of-00001.parquet", "eval": "simplified/validation-00000-of-00001.parquet",
                     "test": "simplified/test-00000-of-00001.parquet"}),
    "mnli": ("nyu-mll/glue", "bcdcba79d07bc864c1c254ccfcedcce55bcc9a8c", "MNLI: OANC / CC-BY-SA-3.0 mix", "train", "hf_nli",
             {"train": "mnli/validation_mismatched-00000-of-00001.parquet", "eval": "mnli/validation_matched-00000-of-00001.parquet"}),
    "ag_news": ("fancyzhx/ag_news", "eb185aade064a813bc0b7f42de02595523103ca4", "unspecified (academic use)", "train", "hf_topic_agnews",
                {"train": "data/train-00000-of-00001.parquet", "eval": "data/test-00000-of-00001.parquet"}),
    "tweet_eval_sentiment": ("cardiffnlp/tweet_eval", "b3a375baf0f409c77e6bc7aa35102b7b3534f8be", "unspecified (Twitter ToS)", "train", "hf_sentiment_tweets",
                             {"train": "sentiment/train-00000-of-00001.parquet", "eval": "sentiment/validation-00000-of-00001.parquet",
                              "test": "sentiment/test-00000-of-00001.parquet"}),
    "clinc_oos": ("clinc/clinc_oos", "155b9c710419136e17307b80d0a13e68cd46b4ec", "CC-BY-3.0", "heldout", "heldout_intent_clinc",
                  {"test": "plus/test-00000-of-00001.parquet"}),
    "dbpedia_14": ("fancyzhx/dbpedia_14", "9abd46cf7fc8b4c64290f26993c540b92aa145ac", "CC-BY-SA-3.0", "heldout", "heldout_topic_dbpedia",
                   {"test": "dbpedia_14/test-00000-of-00001.parquet"}),
    "trec_coarse": ("SetFit/TREC-QC", "0a34640b3cac3affef6f0abdfb81e3d0ecffcf92", "unspecified (research)", "heldout", "heldout_question_type_trec",
                    {"test": "test.jsonl"}),
    "emotion": ("dair-ai/emotion", "cab853a1dbdf4c42c2b3ef2173804746df8825fe", "unspecified (research)", "heldout", "heldout_emotion_multiclass",
                {"test": "split/test-00000-of-00001.parquet"}),
    "boolq": ("google/boolq", "35b264d03638db9f4ce671b711558bf7ff0f80d5", "CC-BY-SA-3.0", "heldout", "heldout_boolq",
              {"test": "data/validation-00000-of-00001.parquet"}),
    "sst2": ("stanfordnlp/sst2", "8d51e7e4887a4caaa95b3fbebbf53c0490b58bbb", "unspecified (research)", "heldout", "heldout_sentiment_sst2",
             {"test": "data/validation-00000-of-00001.parquet"}),
}

QUESTIONS = {
    "banking77": ["What is the customer asking about?", "Which of these best describes the customer's request?", "What does this bank customer want?"],
    "go_emotions": ["Which emotions does the writer express?", "Which of these feelings come through in the comment?", "What emotions does this text convey?"],
    "ag_news": ["What is the topic of this news article?", "Which section of a newspaper does this story belong to?", "What is this news story about?"],
    "tweet_eval_sentiment": ["What is the sentiment of this tweet?", "How does the author feel overall?", "What is the overall tone of the tweet?"],
    "mnli": ['Does the text support this statement: "{h}"', 'Based only on the text, is the following true: "{h}"', 'Is this claim backed up by the text: "{h}"'],
    "clinc_oos": ["What is the user asking the assistant to do?"],
    "dbpedia_14": ["What kind of entity does this article describe?"],
    "trec_coarse": ["What type of answer is this question looking for?"],
    "emotion": ["Which emotion does the writer express?"],
    "sst2": ["Is the sentiment of this review positive?"],
}


def rows(name, split_key):
    repo, rev, *_, files = SOURCES[name]
    path = hf_hub_download(repo, files[split_key], repo_type="dataset", revision=rev)
    return [json.loads(line) for line in open(path)] if path.endswith(".jsonl") else pq.read_table(path).to_pylist()


@functools.cache
def clinc_names():
    repo, rev, *_, files = SOURCES["clinc_oos"]
    meta = pq.read_schema(hf_hub_download(repo, files["test"], repo_type="dataset", revision=rev)).metadata
    return json.loads(meta[b"huggingface"])["info"]["features"]["intent"]["names"]


def label_text(name, label, rng, train):
    human = label.replace("_", " ").replace("/", " / ").strip()
    human = human[0].upper() + human[1:]
    desc = DESC.get(name, {}).get(label)
    return human if (train and rng.random() < 0.5) or not desc else desc


def cands(name, labels, rng, train):
    return [{"id": l.lower().replace(" ", "_").replace("/", "_"), "description": label_text(name, l, rng, train)} for l in labels]


def convert(name, r, i, rng, train):
    """-> (state, question, target, hard_cases) or None to skip."""
    L, qs = LABELS.get(name), QUESTIONS.get(name, [""])
    qtext = rng.choice(qs) if train else qs[0]
    def mc(state, gold, others_k):
        pool = [l for l in L if l != gold]
        opts = rng.sample(pool, min(others_k, len(pool))) + [gold]
        rng.shuffle(opts)
        c = cands(name, opts, rng, train)
        return state, {"type": "multiclass", "instruction": qtext, "candidates": c}, c[opts.index(gold)]["id"], []
    if name == "banking77":
        return mc(r["text"], r["label_text"], 7)
    if name == "ag_news":
        return mc(r["text"], L[int(r["label"])], 3)
    if name == "tweet_eval_sentiment":
        return mc(r["text"], L[int(r["label"])], 2)
    if name == "dbpedia_14":
        return mc(f"{r['title'].strip()}: {r['content'].strip()}", L[int(r["label"])], 5)
    if name == "trec_coarse":
        return mc(r["text"], r["label_coarse_text"], 5)
    if name == "emotion":
        return mc(r["text"], L[int(r["label"])], 5)
    if name == "clinc_oos":
        gold = clinc_names()[int(r["intent"])]
        opts = rng.sample([l for l in L if l != gold], 6) + ([gold] if gold != "oos" else [])
        rng.shuffle(opts)
        c = cands(name, opts, rng, train) + [NOTA]
        return r["text"], {"type": "multiclass", "instruction": qtext, "candidates": c}, "none" if gold == "oos" else c[opts.index(gold)]["id"], ["nota"] if gold == "oos" else []
    if name == "go_emotions":
        pos = [L[int(j)] for j in r["labels"]]
        neg = rng.sample([l for l in L if l not in pos], max(2, 6 - len(pos)))
        opts = pos + neg
        rng.shuffle(opts)
        c = cands(name, opts, rng, train)
        return r["text"], {"type": "multilabel", "instruction": qtext, "candidates": c}, [c[opts.index(p)]["id"] for p in pos], \
            ["multi_positive"] if len(pos) > 1 else []
    if name == "mnli":
        if int(r["label"]) not in (0, 1, 2):
            return None
        tags = {0: [], 1: ["missing_evidence"], 2: ["contradiction"]}[int(r["label"])]
        return r["premise"], {"type": "binary", "instruction": qtext.format(h=r["hypothesis"].strip())}, int(r["label"]) == 0, tags
    if name == "boolq":
        q = r["question"].strip()
        return r["passage"], {"type": "binary", "instruction": q[0].upper() + q[1:] + "?"}, bool(r["answer"]), []
    if name == "sst2":
        return r["sentence"].strip(), {"type": "binary", "instruction": qtext}, int(r["label"]) == 1, []
    raise KeyError(name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train-per-dataset", type=int, default=2400)
    ap.add_argument("--eval-sizes", default="validation=150,calibration=150,test=300")
    ap.add_argument("--heldout-test", type=int, default=300)
    ap.add_argument("--out", default=str(ROOT / "data/hf.jsonl"))
    ap.add_argument("--seed", type=int, default=13)
    a = ap.parse_args()
    sizes = {k: int(v) for k, v in (kv.split("=") for kv in a.eval_sizes.split(","))}
    out = []
    for name, (repo, rev, lic, role, family, files) in SOURCES.items():
        rng = random.Random(f"{a.seed}:{name}")
        plan = []  # (our split, file key, n)
        if role == "train":
            plan.append(("train", "train", a.train_per_dataset))
            if "test" in files:  # dataset has its own val and test files
                plan += [("validation", "eval", sizes["validation"]), ("calibration", "eval", sizes["calibration"]), ("test", "test", sizes["test"])]
            else:
                plan += [(s, "eval", n) for s, n in sizes.items()]
        else:
            plan.append(("test", "test", a.heldout_test))
        used = {}
        for split, key, n in plan:
            data = rows(name, key)
            idx = [j for j in range(len(data)) if j not in used.setdefault(key, set())]
            rng.shuffle(idx)
            k = 0
            for j in idx:
                if k == n:
                    break
                conv = convert(name, data[j], j, rng, split == "train")
                if conv is None:
                    continue
                state, question, target, tags = conv
                if not state.strip():
                    continue
                used[key].add(j)
                ex = {"id": f"{name}-{key}-{j}", "source_id": f"{name}-{key}-{j}", "family": family, "split": split,
                      "provenance": f"hf:{repo}@{rev[:10]}:{files[key]}#{j} ({lic})", "state": state,
                      "question": question, "target": target, "hard_cases": tags}
                validate_example(ex)
                out.append(ex)
                k += 1
        print(f"{name:22s} {role:8s} " + " ".join(f"{s}={sum(1 for e in out if e['family'] == family and e['split'] == s)}"
                                                  for s in ("train", "validation", "calibration", "test")))
    write_jsonl(a.out, out)
    print(f"wrote {len(out)} examples -> {a.out}; label descriptions {'used' if DESC else 'MISSING (humanised names only)'}")


if __name__ == "__main__":
    main()
