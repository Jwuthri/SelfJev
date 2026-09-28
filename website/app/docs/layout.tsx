import { DocsLink } from "@/components/docs-link";
import { docPages } from "@/lib/docs";
export default function DocsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="docs-layout wrap">
      <aside className="docs-sidebar">
        <div className="docs-label">
          DOCUMENTATION <span>v0.2</span>
        </div>
        {["GET STARTED", "BUILD", "DEPLOY"].map((group) => (
          <div className="docs-group" key={group}>
            <h2>{group}</h2>
            {docPages
              .filter((p) => p.group === group)
              .map((p) => (
                <DocsLink
                  key={p.slug}
                  href={p.slug === "quickstart" ? "/docs/" : `/docs/${p.slug}/`}
                >
                  {p.title}
                </DocsLink>
              ))}
          </div>
        ))}
        <a className="notebook-link" href="https://jwuthri.github.io/SelfJev/">
          Research notebook ↗
        </a>
      </aside>
      {children}
    </div>
  );
}
