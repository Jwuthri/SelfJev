"use client";
import { useMemo, useState } from "react";
import { Check, Copy } from "lucide-react";
import { highlightCode } from "@/lib/highlight";
export function CodeBlock({
  code,
  label = "Terminal",
  language = "text",
}: {
  code: string;
  label?: string;
  language?: string;
}) {
  const [copied, setCopied] = useState(false);
  const [failed, setFailed] = useState(false);
  const highlighted = useMemo(() => highlightCode(code, language), [code, language]);
  return (
    <div className="code-block">
      <div className="code-top">
        <span>{label}</span>
        <button
          aria-label={`Copy ${label} code`}
          onClick={async () => {
            try {
              await navigator.clipboard.writeText(code);
              setCopied(true);
              setFailed(false);
              setTimeout(() => setCopied(false), 2000);
            } catch {
              setFailed(true);
            }
          }}
        >
          {copied ? <Check size={14} /> : <Copy size={14} />}{" "}
          {copied ? "Copied" : "Copy"}
        </button>
      </div>
      <pre>
        <code className={`language-${language}`}>{highlighted}</code>
      </pre>
      <span className="sr-only" role="status">
        {copied
          ? "Copied to clipboard"
          : failed
            ? "Copy unavailable. Select and copy the code manually."
            : ""}
      </span>
    </div>
  );
}
