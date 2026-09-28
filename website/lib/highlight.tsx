import type { ReactNode } from "react";
import Prism from "prismjs";
import "prismjs/components/prism-bash";
import "prismjs/components/prism-json";
import "prismjs/components/prism-python";

// React owns the markup; Prism only tokenizes the original source.
Prism.manual = true;

function renderTokens(tokens: (string | Prism.Token)[], language: string): ReactNode {
  return tokens.map((token, index) => {
    if (typeof token === "string") return token;
    let content: ReactNode;
    // A JSON request body is otherwise one shell string. Only reinterpret
    // complete, valid JSON in single quotes (no shell interpolation).
    if (
      language === "bash" &&
      token.type === "string" &&
      typeof token.content === "string" &&
      /^'\s*[\[{]/.test(token.content) &&
      token.content.endsWith("'")
    ) {
      const json = token.content.slice(1, -1);
      try {
        JSON.parse(json);
        content = <>{"'"}{renderTokens(Prism.tokenize(json, Prism.languages.json), "json")}{"'"}</>;
      } catch {
        content = token.content;
      }
    } else {
      content = renderTokens(
        Array.isArray(token.content) ? token.content : [token.content],
        language,
      );
    }
    return <span key={index} className={`token ${token.type}`}>{content}</span>;
  });
}

export function highlightCode(code: string, language: string): ReactNode {
  const aliases: Record<string, string> = { sh: "bash", shell: "bash", py: "python", js: "javascript" };
  const normalized = language.toLowerCase();
  const name = aliases[normalized] || normalized;
  const grammar = Object.hasOwn(Prism.languages, name) ? Prism.languages[name] : undefined;
  return grammar && typeof grammar === "object"
    ? renderTokens(Prism.tokenize(code, grammar), name)
    : code;
}
