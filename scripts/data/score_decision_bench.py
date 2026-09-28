"""Score final decisions against a complete, frozen SelfJev JSONL suite. No model dependencies."""

import argparse
import gzip
import json
from collections import defaultdict
from pathlib import Path


def read_rows(path):
    path = Path(path)
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.strip()]


def indexed(rows, name):
    result = {}
    for row in rows:
        key = row["id"]
        if key in result:
            raise ValueError(f"Duplicate {name} ID: {key}")
        result[key] = row
    if not result:
        raise ValueError(f"Empty {name}")
    return result


def score(examples, predictions):
    truth, pred = indexed(examples, "data"), indexed(predictions, "prediction")
    missing, extra = truth.keys() - pred.keys(), pred.keys() - truth.keys()
    if missing or extra:
        raise ValueError(f"ID coverage mismatch: {len(missing)} missing, {len(extra)} unexpected")
    slices = defaultdict(list)
    for key, row in truth.items():
        kind, target = row["question"]["type"], row["target"]
        selected = pred[key]["selected"]
        candidates = {c["id"] for c in row["question"].get("candidates", [])}
        if kind == "binary":
            valid = isinstance(selected, bool)
        elif kind == "multiclass":
            valid = isinstance(selected, str) and selected in candidates
        elif kind == "multilabel":
            valid = (
                isinstance(selected, list)
                and all(isinstance(x, str) and x in candidates for x in selected)
                and len(set(selected)) == len(selected)
            )
        else:
            raise ValueError(f"Unsupported question type: {kind}")
        if not valid:
            raise ValueError(f"Invalid {kind} prediction for {key}: {selected!r}")
        correct = set(selected) == set(target) if kind == "multilabel" else selected == target
        for group in ("overall", f"type/{kind}", f"family/{row['family']}"):
            slices[group].append(correct)
    return {
        key: {"questions": len(values), "correct": sum(values), "accuracy": sum(values) / len(values)}
        for key, values in sorted(slices.items())
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", required=True, help="selfjev/<suite>.jsonl.gz")
    parser.add_argument("--predictions", required=True, help="JSONL: id and selected (bool, candidate ID, or ID list)")
    args = parser.parse_args()
    print(json.dumps(score(read_rows(args.data), read_rows(args.predictions)), indent=2))


if __name__ == "__main__":
    main()
