SelfJev is a decision scorer built from **Qwen3.5-4B + LoRA r64**. The model evaluates whether a proposed answer is supported by the supplied document. It reads the difference between its yes and no logits, rather than generating a response.

Images use the same shared root: Qwen3.5’s frozen vision encoder processes the photo once, then every question and option branches from it. Use the default tree engine (not vLLM); see [image inputs in the API](https://github.com/Jwuthri/SelfJev/blob/master/docs/api.md#request).

## Read once, branch many

[Explore the animated shared-prefix tree](/#architecture), or [open the static illustration](/images/selfjev-architecture.png).

The document is the shared root. Each question branches from it; each candidate branches from its question. A candidate can attend to its ancestors and itself, never to sibling branches. Positions continue from the parent.

For Qwen3.5’s recurrent layers, the engine executes the tree level by level, copying parent states for the children. Attention layers use the tree mask. This preserves deep interaction between context and the proposed answer while sharing the document work.

The current `TreeServer` runs the same tree structure used in training, forward only. Its correctness is checked against standalone sequences in tiny tests and against the previous engine on full GPU evaluations.

## The options matter

Every candidate is scored knowing all of its alternatives: the options are listed in the question before candidate branches split. A routing decision should distinguish “billing” from “technical support,” rather than judge “billing” in isolation from the choice set.

The server and CLI apply this option-list transformation automatically for the default model.

## From logits to decisions

The raw score is `z_yes − z_no`. Binary decisions use sigmoid. Choice decisions use softmax across candidates. Multilabel decisions apply sigmoid independently to each candidate. Ordered scores use the expected position in a choice distribution.

These are model probabilities. A separately fitted calibration file can alter them; they should not be treated as guaranteed confidence bounds.

## What the model learned from

The default adapter was trained from scratch on **79,943 non-test questions**, with texts up to 16K tokens, a new rank-64 LoRA, and one epoch. Its targets mix 50% verified labels with 50% stored Jev probabilities. Authored training targets were checked by a blind judge; Jev answers did not decide the authored labels.

LLM verification is not human ground truth. Public training data may also overlap base-model pretraining. The research pages preserve these limitations.

## Why not always vLLM?

vLLM is available for merged weights and can be effective for one question. In the measured Qwen3.5 configuration, recurrent-state cache boundaries caused repeated work for many candidate prompts. The native tree shares the document at the branch point explicitly.

Explore the [measured hardware configurations and response times](/docs/hardware/#compare-measured-gpu-response-times).

Read the [full architecture](https://jwuthri.github.io/SelfJev/tree_model/), [engine source](https://github.com/Jwuthri/SelfJev/blob/master/src/selfjev/engine/tree.py), and [model manifest](https://github.com/Jwuthri/SelfJev/blob/master/weights/selfjev_4b/model.json).
