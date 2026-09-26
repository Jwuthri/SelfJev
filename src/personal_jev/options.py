"""Every option listed in the question text ("all options"): each leaf still judges one candidate but now sees all the
alternatives. Adapters trained on data/ova/ (scripts/options_in_question.py) need the same transform on every request
(`pjev serve --options-in-question`). Options are listed in a fixed random order seeded by the given key.

pointers=True (data/ptr/, `--option-pointers`): the options are numbered once in the question, and each leaf only says
"option k". Every option is still judged at its own leaf, through the usual yes/no readout, but a leaf costs ~9 tokens
instead of repeating its whole description."""
import hashlib
import random

HEAD = {"multiclass": "Options (exactly one is correct):", "multilabel": "Options (any number can be correct, possibly none):"}


def with_options(q: dict, seed: str, pointers: bool = False) -> dict:
    """Question dict (type, instruction, candidates) -> the same question with its options in the instruction."""
    if q["type"] == "binary":
        return q
    opts = list(q["candidates"])
    random.Random(int(hashlib.sha256(seed.encode()).hexdigest()[:8], 16)).shuffle(opts)
    if not pointers:
        return q | {"instruction": f"{q['instruction']}\n{HEAD[q['type']]}\n" + "\n".join(f"- {c['description']}" for c in opts)}
    num = {c["id"]: k for k, c in enumerate(opts, 1)}
    return q | {"instruction": f"{q['instruction']}\n{HEAD[q['type']]}\n" + "\n".join(f"{k}. {c['description']}" for k, c in enumerate(opts, 1)),
                "candidates": [c | {"description": f"option {num[c['id']]}"} for c in q["candidates"]]}  # ids and order unchanged
