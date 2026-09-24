"""Every option listed in the question text ("all options"): each leaf still judges one candidate but now sees all the
alternatives. Adapters trained on data/ova/ (scripts/options_in_question.py) need the same transform on every request
(`pjev serve --options-in-question`). Options are listed in a fixed random order seeded by the given key."""
import hashlib
import random

HEAD = {"multiclass": "Options (exactly one is correct):", "multilabel": "Options (any number can be correct, possibly none):"}


def with_options(q: dict, seed: str) -> dict:
    """Question dict (type, instruction, candidates) -> the same question with its options in the instruction."""
    if q["type"] == "binary":
        return q
    opts = list(q["candidates"])
    random.Random(int(hashlib.sha256(seed.encode()).hexdigest()[:8], 16)).shuffle(opts)
    return q | {"instruction": f"{q['instruction']}\n{HEAD[q['type']]}\n" + "\n".join(f"- {c['description']}" for c in opts)}
