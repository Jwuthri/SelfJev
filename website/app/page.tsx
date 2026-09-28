import { ReleaseLinks } from "@/components/release-links";
import { HF_RELEASES } from "@/lib/releases";
import Link from "next/link";
import { ArchitectureTree } from "@/components/architecture-tree";
import {
  ArrowRight,
  ArrowUpRight,
  GitBranch,
  Fingerprint,
  Braces,
  Terminal,
} from "lucide-react";
import { DecisionTree } from "@/components/decision-tree";
import { Benchmarks } from "@/components/explorers";
import { HardwareExplorer } from "@/components/hardware-explorer";
import { CodeBlock } from "@/components/code-block";
import { DemoVideo } from "@/components/demo-video";
import { headlines, leaderboard, hardwareLatencyData, macLatencyData, JOURNAL, REPO } from "@/lib/evidence";
const BASE = process.env.NEXT_PUBLIC_BASE_PATH || "";
const sdk = `from selfjev import SelfJev, Noul, Choice

# Use the secret you set as SELFJEV_API_KEYS on your server.

client = SelfJev(
    base_url="http://localhost:8000",
    api_key="your-server-key",
)

result = client.system_one(
    state="I was charged twice. Please refund me.",
    questions={
        "refund": Noul("Does the customer want a refund?"),
        "team": Choice("Which team should handle this?", {
            "billing": "payments and refunds",
            "support": "technical support",
        }),
    },
)`;
export default function Home() {
  const h = headlines();
  const rows = leaderboard();
  const hardware = hardwareLatencyData();
  const mac = macLatencyData();
  const featured = rows.filter((r) => r.current || r.id === "~typesafe/jev-latest");
  return (
    <main id="main">
      <section className="hero wrap">
        <div className="hero-copy">
          <div className="eyebrow">
            <span className="orange-line" /> THE SELF-HOSTED DECISION MODEL{" "}
            <span className="version">v0.2</span>
          </div>
          <h1>
            Intelligence,
            <br />
            <span>decided.</span>
          </h1>
          <p className="hero-description">
            Turn context into decisions.
            <br />A small AI model that reads once, answers many,
            <br className="desktop-break" /> and runs on infrastructure you
            control.
          </p>
          <div className="hero-actions">
            <Link className="button primary" href="/docs/">
              Start building <ArrowUpRight size={17} />
            </Link>
            <Link className="text-link" href="/research/">
              Explore the research <ArrowRight size={16} />
            </Link>
          </div>
          <a className="hero-release-link" href={HF_RELEASES.merged}>
            Weights available on Hugging Face <ArrowUpRight size={14} />
          </a>
          <div className="hero-footnote">
            <span>Runs on one GPU</span>
            <i />
            <span>No text generation</span>
            <i />
            <span>Jev-compatible API</span>
          </div>
        </div>
        <DecisionTree />
      </section>
      <div className="metric-strip wrap">
        <a href={h.eval2.url}>
          <span className="metric-label">TEXT DECISIONS</span>
          <strong>
            {h.eval2.display}
            <small>%</small>
          </strong>
          <span>
            Matches expected answers in our tests <ArrowUpRight size={13} />
          </span>
        </a>
        <a href={h.llm.url}>
          <span className="metric-label">AI RESPONSE REVIEW</span>
          <strong>
            {h.llm.display}
            <small>%</small>
          </strong>
          <span>
            Checks quality, accuracy & safety <ArrowUpRight size={13} />
          </span>
        </a>
        <Link href="/#architecture">
          <span className="metric-label">READ YOUR TEXT ONCE</span>
          <strong>
            1<small> read</small>
          </strong>
          <span>
            Across every question in a request <ArrowRight size={13} />
          </span>
        </Link>
        <Link href="/docs/api/">
          <span className="metric-label">GENERATED TEXT</span>
          <strong>0</strong>
          <span>
            Answers your code can use <ArrowRight size={13} />
          </span>
        </Link>
      </div>
      <p className="metric-context wrap">Accuracy on our project’s test questions, not a guarantee for every use case. <Link href="/research/#test-guide">What did we test? ↗</Link></p>
      <section className="section wrap demo-section" id="watch">
        <div className="section-kicker">WATCH / ONE RECORDED RUN</div>
        <div className="section-heading">
          <h2>
            One command to a live API.
            <br />
            <span>Recorded end to end.</span>
          </h2>
          <p>
            A real run on one NVIDIA L40S: deploy, six answers from one read of the text, Jev’s API, clear errors,
            and two fine-tuning jobs over HTTP. 14 of 14 checks passed.
          </p>
        </div>
        <figure className="demo-video">
          <DemoVideo
            src={`${BASE}/video/selfjev-e2e.mp4`}
            poster={`${BASE}/video/selfjev-e2e-poster.jpg`}
            label="A recorded run of SelfJev: one-command deploy, typed answers, Jev compatibility, errors and fine-tuning over HTTP"
          />
          <figcaption>
            Every answer and number on screen comes from the run’s record; minutes-long steps are time-lapsed.{" "}
            <a href={`${REPO}/blob/master/reports/e2e/2026-09-28/report.md`}>
              Read the run’s report <ArrowUpRight size={13} />
            </a>
          </figcaption>
        </figure>
      </section>
      <section className="section wrap intro">
        <div className="section-kicker">01 / BUILT TO DECIDE</div>
        <div>
          <h2>
            Some things need an answer.
            <br />
            <span>Not another conversation.</span>
          </h2>
          <p className="section-description">
            Route a request. Check an agent’s work. Apply a policy. SelfJev
            turns your text and questions into structured decisions with
            probabilities—without waiting for a generated response.
          </p>
          <div className="feature-row">
            <article>
              <Braces />
              <h3>Four answer types.</h3>
              <p>
                Yes/no, pick one, rate a result, or select all that apply.
                Ready to use in your application.
              </p>
            </article>
            <article>
              <Fingerprint />
              <h3>Your data stays yours.</h3>
              <p>
                Run the model on your own GPU. Process sensitive text
                without sending it to an external model API.
              </p>
            </article>
            <article>
              <GitBranch />
              <h3>A familiar interface.</h3>
              <p>
                Already using Jev? Keep the same request format and point
                your application to your own server.
              </p>
            </article>
          </div>
        </div>
      </section>
      <section id="architecture" className="section architecture-section">
        <div className="wrap">
          <div className="section-kicker">02 / HOW IT WORKS</div>
          <div className="section-heading">
            <h2>
              One context.
              <br />
              <span>Every angle.</span>
            </h2>
            <p>
              A support message can raise several questions: what happened,
              who should handle it, and what to do next. SelfJev reads the
              message once and reuses that work for every answer.
            </p>
          </div>
          <ArchitectureTree />
          <div className="arch-notes">
            <p>
              <b>01. Give it context</b>A message, document, or AI response,
              together with the questions you need answered.
            </p>
            <p>
              <b>02. Ask several questions</b>Each question uses the same text,
              so the model avoids reading it from scratch each time.
            </p>
            <p>
              <b>03. Act on the answers</b>Get clear choices and probabilities
              to route, filter, or review in your own application.
            </p>
          </div>
        </div>
      </section>
      <section className="section wrap ownership-section" id="make-it-yours">
        <div className="section-kicker">YOUR MODEL / YOUR REQUIREMENTS</div>
        <div className="section-heading">
          <h2>Make room.<br /><span>Make it yours.</span></h2>
          <p>Your documents, your vocabulary, your edge cases. Control the context budget and adapt the model to the decisions that matter to you.</p>
        </div>
        <div className="ownership-grid">
          <article className="context-card">
            <span className="tree-overline">ROOM FOR LONGER CONTEXT</span>
            <h3>A bigger foundation.<br />A limit you control.</h3>
            <p>Jev allows 32K tokens for your text plus the longest question. SelfJev has a configurable limit, built on a model with a 262,144-token native context window.</p>
            <div className="context-scale" aria-label="Context specifications, not measured SelfJev capacity">
              <div><span>Jev · text + longest question</span><b>32K</b><i style={{width: "12.5%"}} /></div>
              <div><span>SelfJev · base-model capacity</span><b>262K</b><i style={{width: "100%"}} /></div>
            </div>
            <p className="ownership-detail">SelfJev defaults to 32,768 tokens; larger windows need sufficient memory and validation. The full base-model window has not been validated in our engine. Jev also allows 64K across a whole request.</p>
            <Link className="text-link" href="/docs/hardware/#context-length-and-concurrency-matter">Context & sizing <ArrowUpRight size={15}/></Link>
          </article>
          <article className="finetune-card">
            <span className="tree-overline">BUILT TO ADAPT</span>
            <h3>Your use case.<br />Your fine-tune.</h3>
            <p>Not getting the decisions you need? Fine-tune SelfJev on examples from your own workflow: your labels, your policies, your definition of a good answer.</p>
            <ol className="adapt-steps">
              <li><span>01</span><div><b>Show it what good looks like.</b><small>Pair real inputs with verified answers.</small></div></li>
              <li><span>02</span><div><b>Train a lightweight adapter.</b><small>Use the included supervised fine-tuning tools.</small></div></li>
              <li><span>03</span><div><b>Evaluate. Then deploy.</b><small>Check held-out examples and serve your model.</small></div></li>
            </ol>
            <Link className="text-link" href="/docs/finetuning/">Fine-tune for your use case <ArrowUpRight size={15}/></Link>
          </article>
        </div>
      </section>
      <section className="section wrap" id="benchmarks">
        <div className="section-kicker">03 / THE EVIDENCE</div>
        <div className="section-heading">
          <h2>
            Strong results.
            <br />
            <span>Receipts included.</span>
          </h2>
          <p>
            Can it choose the right answer from a piece of text? We tested
            yes/no decisions, choosing between options, and selecting every
            answer that applies.
          </p>
        </div>
        <Benchmarks rows={featured} compact />
        <div className="below-panel">
          <p>
            SelfJev approaches Jev’s accuracy on these tests and runs on your
            own infrastructure. The questions and expected answers were created
            and checked by AI; results on your own data may differ.
          </p>
          <Link className="text-link" href="/research/">
            How we tested it <ArrowRight size={16} />
          </Link>
        </div>
        <div className="research-insight">
          <span className="insight-index">↳</span>
          <div>
            <h3>The breakthrough was learning the right task.</h3>
            <p>
              Handling exceptions, weighing alternatives, and checking AI
              responses all needed targeted training. Improving those examples
              mattered more than simply making the model bigger.
            </p>
          </div>
          <a href={`${JOURNAL}/findings/`}>
            Read the findings <ArrowUpRight size={16} />
          </a>
        </div>
      </section>
      <section className="section speed-section" id="hardware">
        <div className="wrap speed-layout">
          <div>
            <div className="section-kicker">04 / THE SPEED STORY</div>
            <h2>
              Less repeated work.
              <br />
              <span>More decisions.</span>
            </h2>
            <p className="section-description">
              From a local Mac to a dedicated GPU. Explore measured response
              times, adjust your workload, and see what fits your infrastructure.
            </p>
            <div className="speed-callout">
              <strong>
                {Math.round(hardware.find((point) => point.tokens === 8 && point.questions === 1)!.h100)}
                <span>ms</span>
              </strong>
              <p>
                H100 · measured processing time
                <br />
                Very short input · one question
              </p>
            </div>
            <a className="text-link" href={`${JOURNAL}/speed/`}>
              How we measured speed <ArrowUpRight size={16} />
            </a>
          </div>
          <HardwareExplorer data={hardware} mac={mac} />
        </div>
      </section>
      <div className="wrap" id="downloads"><ReleaseLinks /></div>
      <section className="section wrap build-section">
        <div>
          <div className="section-kicker">05 / YOUR INFRASTRUCTURE</div>
          <h2>
            From a question
            <br />
            <span>to your first call.</span>
          </h2>
          <p className="section-description">
            A lightweight Python SDK. One GPU to serve. Docker and an AWS
            deployment command, with practical guides for Runpod and Google
            Cloud.
          </p>
          <div className="deploy-links">
            {[
              ["Quickstart", "/docs/"],
              ["Hardware & sizing", "/docs/hardware/"],
              ["AWS", "/docs/aws/"],
              ["Runpod", "/docs/runpod/"],
              ["Google Cloud", "/docs/gcp/"],
            ].map(([n, l]) => (
              <Link key={n} href={l}>
                {n}
                <ArrowUpRight size={15} />
              </Link>
            ))}
          </div>
        </div>
        <CodeBlock label="Python / your first decision" language="python" code={sdk} />
      </section>
      <section className="closing wrap">
        <span className="section-kicker">
          THE MODEL IS SMALL. THE NOTEBOOK IS OPEN.
        </span>
        <h2>
          Make the next decision
          <br />
          <span>on your terms.</span>
        </h2>
        <Link className="button primary" href="/docs/">
          <Terminal size={17} /> Self-host SelfJev <ArrowUpRight size={17} />
        </Link>
      </section>
    </main>
  );
}
