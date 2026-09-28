import { ReleaseLinks } from "@/components/release-links";
import { HF_RELEASES } from "@/lib/releases";
import type { Metadata } from "next";
import { ArrowUpRight } from "lucide-react";
import { Benchmarks } from "@/components/explorers";
import { leaderboard, JOURNAL } from "@/lib/evidence";
export const metadata: Metadata = { title: "Research & evidence" };
const experiments = [
  ["01", "Start with search models", "Finding relevant text isn’t the same as deciding.", "We began with models built to rank search results. Training them on decisions helped, but moving to a larger version brought little improvement. The task needed more than a bigger model.", "stock_model"],
  ["02", "Try a shortcut", "The question and the text need to meet.", "We tried reading the text and question separately, then combining what the model learned. It reduced repeated work, but missed too much detail. How a question relates to the text matters.", "custom_model"],
  ["03", "Reuse the reading", "Read once. Look at it from every angle.", "We kept the rich interaction between question and text, while sharing the work of reading the document. This became the foundation of SelfJev’s architecture.", "tree_model"],
  ["04", "Try smaller alternatives", "Smaller wasn’t always better.", "We tested compact models, including Jina and an adapted T5Gemma. In those experiments, efficiency came with lower decision accuracy. These results describe our versions and training, not every use of those models.", "challengers"],
  ["05", "Make the choices clearer", "Teach it to weigh the alternatives.", "A stronger starting model, all possible answers shown together, and training on longer texts improved the recipe. The model could learn what makes one choice fit better than another.", "tree_model"],
  ["06", "Train for the actual work", "Better examples. Better decisions.", "The current model learns from nearly 80,000 questions, including difficult cases and AI response review. It combines checked training answers with Jev’s probability estimates to learn how to weigh the choices.", "findings"],
];
export default function Research() {
  const rows = leaderboard();
  const selected = rows.filter((r) => r.current || r.id === "~typesafe/jev-latest");
  return (
    <main id="main" className="wrap research-page">
      <div className="page-intro">
        <div className="eyebrow">THE OPEN NOTEBOOK / RESEARCH</div>
        <h1>Show your work.</h1>
        <p>What can it do? How well does it work?<br />The results, and the experiments behind them.</p>
      </div>
      <div className="research-summary">
        <span><b>{rows.length}</b> recorded experiments</span>
        <span><b>3</b> ways to test decisions</span>
        <span><b>1</b> current model</span>
      </div>
      <section className="test-guide" id="test-guide">
        <div className="section-kicker">WHAT THE SCORES MEAN</div>
        <h2>Test the work<br /><span>you need it to do.</span></h2>
        <div className="test-cards">
          <article><span className="eyebrow">01 / TEXT DECISIONS</span><h3>Read. Understand. Choose.</h3><p>Can it answer questions about a piece of text, including exceptions and several possible answers?</p><small>1,991 questions · yes/no, pick one, select all</small></article>
          <article><span className="eyebrow">02 / AI RESPONSE REVIEW</span><h3>Check the AI’s work.</h3><p>Can it judge answer quality, check supporting evidence, apply a policy, or spot an attempt to bypass instructions?</p><small>946 questions · quality, accuracy & safety</small></article>
          <article><span className="eyebrow">03 / BROADER TEXT TASKS</span><h3>Go beyond one use case.</h3><p>Can it recognize intent, topics, sentiment, and other text patterns? These tasks helped guide development.</p><small>3,471 questions · development progress only</small></article>
        </div>
      </section>
      <div className="research-dataset-note">
        <p><b>Run the evaluation yourself.</b> Decision Bench publishes Text Decisions, AI Response Review, and a separate 720-question Record Reasoning suite. The broader development benchmark above is not included.</p>
        <a className="text-link" href={HF_RELEASES.dataset}>Dataset, scoring tools & methodology <ArrowUpRight size={15}/></a>
      </div>
      <ReleaseLinks />
      <Benchmarks rows={selected} />
      <div className="methodology">
        <h3>A useful signal, with a clear scope.</h3>
        <p>Each score is the percentage of answers that match the expected result on that test. Jev still leads on text decisions. SelfJev brings comparable results on these questions to a model you can run yourself.</p>
        <p>Our two focused tests were written and checked by AI, whose answers can still be wrong. They help us assess progress; they do not guarantee the same accuracy on your data. We have not tested every model on Hugging Face.</p>
        <details className="evidence-details">
          <summary>Test sources, methodology & limitations</summary>
          <p>“Text decisions” is the project’s <code>eval2</code> test; “AI response review” is <code>eval_llm</code>. Both use fixed questions kept out of training, with expected answers checked by two AI judges. They have informed the research direction, so a fresh final test is still needed. “Broader text tasks” combines the public and authored datasets in our development benchmark, reused for many decisions.</p>
          <p>For questions with multiple correct choices, every choice must match. Results are single runs; repeating a training recipe moved scores by roughly a percentage point. Earlier experiments differ in training data, objectives, and serving software, so the table does not isolate the effect of architecture alone. Missing results are omitted, not treated as zero.</p>
          <p>The current SelfJev uses TreeServer. Its original evaluation used different serving software with the same trained model; both are preserved in the full experiment archive.</p>
          <a href={`${JOURNAL}/experiments/`}>Full methodology and paired comparisons <ArrowUpRight size={15} /></a>
        </details>
      </div>
      <details className="evidence-details experiment-archive">
        <summary>Explore all {rows.length} experiments <span>Model names, run IDs & source reports</span></summary>
        <Benchmarks rows={rows} archive />
      </details>
      <section className="section">
        <div className="section-kicker">WHAT WE LEARNED</div>
        <h2>The route was<br /><span>anything but straight.</span></h2>
        <div className="timeline">
          {experiments.map(([n, title, subtitle, body, link]) => (
            <article key={n}>
              <span className="timeline-number">{n}</span>
              <div><span className="eyebrow">{title}</span><h3>{subtitle}</h3><p>{body}</p><a href={`${JOURNAL}/${link}/`}>Read the experiment <ArrowUpRight size={14} /></a></div>
            </article>
          ))}
        </div>
      </section>
      <section className="research-bottom">
        <div><h3>The dead ends are part of the result.</h3><p>Larger models and more training data did not always help. We keep the failures alongside the wins, so the reasoning behind the current design stays visible.</p></div>
        <a className="button outline" href={`${JOURNAL}/dead_ends/`}>What didn’t work <ArrowUpRight size={16} /></a>
      </section>
    </main>
  );
}
