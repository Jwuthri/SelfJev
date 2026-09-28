import Link from "next/link";
import { ArrowRight, ArrowUpRight } from "lucide-react";
import { docPages, docContent } from "@/lib/docs";
import { DocContent } from "./doc-content";
export function DocPage({ slug }: { slug: string }) {
  const page = docPages.find((p) => p.slug === slug)!;
  const content = docContent(slug);
  const next = docPages[(docPages.indexOf(page) + 1) % docPages.length];
  return (
    <main id="main" className="doc-article">
      <div className="eyebrow">{page.group} / SELFJEV</div>
      <h1>{page.title}</h1>
      <p className="doc-description">{page.description}</p>
      <DocContent text={content} />
      <div className="doc-end">
        <a
          href={`https://github.com/Jwuthri/SelfJev/blob/master/website/content/${slug}.md`}
        >
          View source <ArrowUpRight size={14} />
        </a>
        <Link
          href={next.slug === "quickstart" ? "/docs/" : `/docs/${next.slug}/`}
        >
          {next.title} <ArrowRight size={15} />
        </Link>
      </div>
    </main>
  );
}
