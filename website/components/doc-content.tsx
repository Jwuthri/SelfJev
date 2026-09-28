import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import Link from "next/link";
import { CodeBlock } from "./code-block";
export function DocContent({ text }: { text: string }) {
  return (
    <div className="prose">
      <Markdown
        remarkPlugins={[remarkGfm]}
        components={{
          pre: ({ children }) => <>{children}</>,
          code: ({ children, className }) =>
            className || String(children).includes("\n") ? (
              <CodeBlock
                code={String(children).replace(/\n$/, "")}
                label={className?.replace("language-", "") || "Code"}
                language={className?.replace("language-", "") || "text"}
              />
            ) : (
              <code>{children}</code>
            ),
          a: ({ href, children }) =>
            href?.startsWith("/") ? (
              <Link href={href}>{children}</Link>
            ) : (
              <a href={href}>{children}</a>
            ),
          h2: ({ children }) => (
            <h2
              id={String(children)
                .toLowerCase()
                .replace(/[^a-z0-9]+/g, "-")
                .replace(/-$/, "")}
            >
              {children}
            </h2>
          ),
          table: ({ children }) => (
            <div className="table-scroll">
              <table>{children}</table>
            </div>
          ),
        }}
      >
        {text}
      </Markdown>
    </div>
  );
}
