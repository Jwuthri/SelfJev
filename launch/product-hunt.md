# Product Hunt launch: SelfJev

Status: draft, 2026-09-28. Every number below comes from `README.md` / `reports/selfjev_4b_treeserver/`. Re-check them the day before launch.

## 1. Listing

**Name:** SelfJev

**Tagline** (60-character limit):

1. `Jev's decisions API, on your own GPU` (36)
2. `Self-hosted decisions model. Drop-in for Jev's API` (50)
3. `Typed yes/no, choice and score answers from your own GPU` (56)

**Description** (260-character limit):

> SelfJev is an open 4B decisions model you host yourself. Ask typed questions about any text (yes/no, pick one, pick any, score) and get calibrated probabilities. Jev-compatible: point TypeSafe's SDK at your server with two env vars. Fine-tune it on your data.

(259 characters, just under the limit)

**Links:** website `https://www.selfjev.dev/` (the Product Hunt link) · GitHub `https://github.com/Jwuthri/SelfJev` · PyPI `https://pypi.org/project/selfjev/` · model `https://huggingface.co/Jwuthrich/selfjev-4b`

**Topics:** Developer Tools · Artificial Intelligence · Open Source · GitHub

**Pricing:** Free (open source). Your only cost is your own GPU.

## 2. Maker's first comment

> Hi Product Hunt 👋 I'm Julien.
>
> I love decision models like TypeSafe's Jev. Instead of asking an LLM to *write* an answer and then parsing it, you ask a typed question ("Does the customer want a refund?", "Which team?") and get a calibrated probability back. They're cheap, fast and don't hallucinate formats.
>
> But some teams can't send their text to someone else's API: support tickets, medical notes, contracts. So I built **SelfJev**, an open decisions model you run on your own GPU.
>
> **What it does**
> 🧩 Four answer types: `Noul` (P(yes)), `Choice` (pick one), `Score` (ordered scale), `Multi` (pick any)
> 🔌 **Jev-compatible API.** Already use TypeSafe's Python SDK? Set `TYPESAFE_BASE_URL` and `TYPESAFE_API_KEY` to your server. No code change.
> 🌳 Reads the document **once** and shares that computation across every question and answer choice (a shared-prefix tree). Many questions about one text cost little more than one.
> 🎯 Fine-tune it on your own labels with `selfjev finetune`, or over HTTP with an OpenAI-shaped fine-tuning API.
> 🚀 `pip install "selfjev[serve]" && selfjev serve` on a 24 GB GPU, or `selfjev deploy aws up`.
>
> **How good is it?** On our evaluation suites, selfjev-4b scores 95.7% vs Jev's 97.2% on text decisions and 93.1% vs 92.5% on AI-response review. These are our own suites with AI-authored labels, not a universal ranking, and every report is in the repo. The evaluation set is public as Decision Bench on Hugging Face.
>
> **What it isn't:** a hosted service. There's no SelfJev cloud. You run it, your data stays with you.
>
> The code is Apache-2.0 and the whole research journal is public, including the dead ends. I'd love to hear which decisions you'd put on it, and where it gets them wrong.


## 3. Gallery (1270×760, in order)

1. **Hero:** `weights/selfjev_4b/assets/hero.png` with the line "Jev's decisions API, on your own GPU".
2. **Two env vars:** a code screenshot of the TypeSafe SDK snippet from `README.pypi.md`, section 2a, with the before/after `TYPESAFE_BASE_URL` highlighted. This is the strongest single image.
3. **Four answer types:** the refund / team / urgency / topics example with the JSON response beside it.
4. **How it works:** `weights/selfjev_4b/assets/prefix-tree.png`.
5. **Accuracy vs Jev:** `weights/selfjev_4b/assets/accuracy-size.png`, or a clean bar chart of the three suites.
6. **Fine-tune:** the `selfjev finetune` command plus a before/after score on a custom set, if you have one you can publish.

**Video:** reuse the 75-second end-to-end run on the website homepage (`website/public/video/`). Product Hunt takes a YouTube link, so upload it there. If you cut a 60s version, end on the two-variable switch from TypeSafe's SDK.

Avoid speed claims. `reports/latency/summary.md` shows Jev faster than our TreeServer in most cells, and serving on an L4 hasn't been measured.

## 4. Likely questions and honest answers

| Question | Answer |
|---|---|
| Why not just use Jev? | Use Jev if you can. SelfJev is for when the text can't leave your infrastructure, when you need to fine-tune on your own labels, or when volume makes a fixed GPU cheaper. |
| What does it cost to run? | A 24 GB GPU. AWS g6.xlarge (L4) is about $0.81/h on demand; g6e.xlarge (L40S, 48 GB) about $1.86/h, which also fits fine-tuning next to serving. |
| Is it as accurate as Jev? | Close on our suites (numbers above), and below Jev on text decisions. The labels are AI-authored and checked; a fresh independent holdout is still to do (README says so). |
| Can I run it on a Mac? | Tests yes, real serving no: it needs an NVIDIA GPU. |
| License? | Code Apache-2.0 (`pip install selfjev`). Weights: see the [model card](https://huggingface.co/Jwuthrich/selfjev-4b). |
| How long can the text be? | Up to 32K tokens of state + question by default (`--max-length`). |
| Why 4B? | It's the size that fit a 24 GB card with long documents. `docs/challengers.md` has what smaller models scored. |

## 5. Launch-day checklist

- [ ] Schedule for 12:01 am PT on a Tuesday–Thursday
- [ ] Hunter chosen (or self-hunt)
- [ ] Gallery + video uploaded, first comment pasted the moment it goes live
- [ ] Product Hunt badge on the website and the GitHub README
- [ ] Posts ready for X, LinkedIn, r/LocalLLaMA and Hacker News (Show HN: "SelfJev – an open, self-hosted decisions model with Jev's API")
- [ ] Be around all day to answer comments; the first 4 hours matter most

## 6. Short post

> Launching SelfJev on Product Hunt today 🚀
> An open 4B decisions model you run on your own GPU: typed yes/no, choice, score and multi-label answers with probabilities.
> Already on Jev? Point TypeSafe's SDK at your server with two env vars.
> pip install selfjev · Apache-2.0 → https://www.selfjev.dev/
