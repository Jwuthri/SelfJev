import { ArrowUpRight, Database, Download, GitBranch } from "lucide-react";
import { HF_RELEASES } from "@/lib/releases";

export function ReleaseLinks() {
  return <section className="release-panel" aria-label="Hugging Face releases">
    <div className="release-heading"><div><span className="tree-overline">AVAILABLE ON HUGGING FACE</span><h3>Get the weights. Explore the evidence.</h3></div><a href={HF_RELEASES.profile}>Jwuthrich <ArrowUpRight size={14}/></a></div>
    <div className="release-grid">
      <a href={HF_RELEASES.merged}><Download size={20}/><span className="release-kind">FULL MODEL</span><h4>SelfJev-4B <ArrowUpRight size={17}/></h4><p>The complete merged weights, with tokenizer and model configuration.</p><span className="release-action">Get the model ↗</span></a>
      <a href={HF_RELEASES.adapter}><GitBranch size={20}/><span className="release-kind">LORA ADAPTER</span><h4>The adaptable version <ArrowUpRight size={17}/></h4><p>The trained adapter used by the native tree engine, with its model card.</p><span className="release-action">Get the adapter ↗</span></a>
      <a href={HF_RELEASES.dataset}><Database size={20}/><span className="release-kind">EVALUATION DATASET</span><h4>Decision Bench <ArrowUpRight size={17}/></h4><p>3,657 questions across text decisions, AI response review, and record reasoning.</p><span className="release-action">Explore the dataset ↗</span></a>
    </div>
  </section>;
}
