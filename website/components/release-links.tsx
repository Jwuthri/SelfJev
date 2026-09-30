import { ArrowUpRight, Database, Download, GitBranch } from "lucide-react";
import { HF_RELEASES } from "@/lib/releases";

export function ReleaseLinks() {
  return <section className="release-panel" aria-label="Hugging Face releases">
    <div className="release-heading"><div><span className="tree-overline">AVAILABLE ON HUGGING FACE</span><h3>Get the weights. Explore the evidence.</h3></div><a href={HF_RELEASES.profile}>Jwuthrich <ArrowUpRight size={14}/></a></div>
    <div className="release-grid">
      <a href={HF_RELEASES.adapter}><GitBranch size={20}/><span className="release-kind">DEFAULT / VISION + TEXT</span><h4>SelfJev-4B <ArrowUpRight size={17}/></h4><p>The image-and-text adapter used by the native tree engine. Downloaded automatically by SelfJev.</p><span className="release-action">Get the model ↗</span></a>
      <a href={HF_RELEASES.merged}><Download size={20}/><span className="release-kind">MERGED WEIGHTS</span><h4>Ready for vLLM <ArrowUpRight size={17}/></h4><p>The complete vision release with tokenizer and configuration. vLLM serves text; images need the native engine.</p><span className="release-action">Get merged weights ↗</span></a>
      <a href={HF_RELEASES.dataset}><Database size={20}/><span className="release-kind">EVALUATION DATASET</span><h4>Decision Bench <ArrowUpRight size={17}/></h4><p>3,657 questions across text decisions, AI response review, and record reasoning.</p><span className="release-action">Explore the dataset ↗</span></a>
    </div>
    <div className="release-legacy">Looking for the previous model? <a href={HF_RELEASES.textOnly}>Text-only release <ArrowUpRight size={14}/></a></div>
  </section>;
}
