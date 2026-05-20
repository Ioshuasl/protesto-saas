import { readFile } from "node:fs/promises";
import { join } from "node:path";

type MarkdownBlock =
  | { type: "h1" | "h2" | "h3"; text: string }
  | { type: "paragraph"; text: string }
  | { type: "ul"; items: string[] }
  | { type: "hr" }
  | { type: "code"; text: string };

function parseMarkdown(content: string): MarkdownBlock[] {
  const lines = content.replace(/\r\n/g, "\n").split("\n");
  const blocks: MarkdownBlock[] = [];

  let i = 0;
  while (i < lines.length) {
    const line = lines[i].trimEnd();
    const trimmed = line.trim();

    if (!trimmed) {
      i += 1;
      continue;
    }

    if (trimmed.startsWith("```")) {
      i += 1;
      const codeLines: string[] = [];
      while (i < lines.length && !lines[i].trim().startsWith("```")) {
        codeLines.push(lines[i]);
        i += 1;
      }
      blocks.push({ type: "code", text: codeLines.join("\n") });
      i += 1;
      continue;
    }

    if (trimmed === "---") {
      blocks.push({ type: "hr" });
      i += 1;
      continue;
    }

    if (trimmed.startsWith("# ")) {
      blocks.push({ type: "h1", text: trimmed.slice(2).trim() });
      i += 1;
      continue;
    }
    if (trimmed.startsWith("## ")) {
      blocks.push({ type: "h2", text: trimmed.slice(3).trim() });
      i += 1;
      continue;
    }
    if (trimmed.startsWith("### ")) {
      blocks.push({ type: "h3", text: trimmed.slice(4).trim() });
      i += 1;
      continue;
    }

    if (trimmed.startsWith("- ")) {
      const items: string[] = [];
      while (i < lines.length && lines[i].trim().startsWith("- ")) {
        items.push(lines[i].trim().slice(2).trim());
        i += 1;
      }
      blocks.push({ type: "ul", items });
      continue;
    }

    const paragraphLines = [trimmed];
    i += 1;
    while (i < lines.length) {
      const next = lines[i].trim();
      if (!next || next === "---" || next.startsWith("#") || next.startsWith("- ") || next.startsWith("```")) {
        break;
      }
      paragraphLines.push(next);
      i += 1;
    }
    blocks.push({ type: "paragraph", text: paragraphLines.join(" ") });
  }

  return blocks;
}

export default async function DocsPage() {
  const filePath = join(process.cwd(), "DATA_CONFIG_ENDPOINTS_FLUXO_EDITAL.md");
  const markdown = await readFile(filePath, "utf-8");
  const blocks = parseMarkdown(markdown);

  return (
    <div className="mx-auto w-full max-w-5xl space-y-6 p-4 md:p-8">
      <header className="space-y-2">
        <h1 className="text-2xl font-bold tracking-tight">Documentação de Endpoints</h1>
        <p className="text-sm text-muted-foreground">
          Conteúdo renderizado de <code>DATA_CONFIG_ENDPOINTS_FLUXO_EDITAL.md</code>.
        </p>
      </header>

      <article className="space-y-4 rounded-lg border bg-card p-4 md:p-6">
        {blocks.map((block, index) => {
          if (block.type === "h1") {
            return (
              <h1 key={index} className="mt-6 text-2xl font-bold first:mt-0">
                {block.text}
              </h1>
            );
          }
          if (block.type === "h2") {
            return (
              <h2 key={index} className="mt-5 text-xl font-semibold first:mt-0">
                {block.text}
              </h2>
            );
          }
          if (block.type === "h3") {
            return (
              <h3 key={index} className="mt-4 text-lg font-semibold first:mt-0">
                {block.text}
              </h3>
            );
          }
          if (block.type === "ul") {
            return (
              <ul key={index} className="list-disc space-y-1 pl-6 text-sm leading-relaxed">
                {block.items.map((item, itemIndex) => (
                  <li key={itemIndex}>{item}</li>
                ))}
              </ul>
            );
          }
          if (block.type === "hr") {
            return <hr key={index} className="my-4 border-border" />;
          }
          if (block.type === "code") {
            return (
              <pre key={index} className="overflow-x-auto rounded-md bg-muted p-3 text-xs">
                <code>{block.text}</code>
              </pre>
            );
          }

          return (
            <p key={index} className="text-sm leading-relaxed">
              {block.text}
            </p>
          );
        })}
      </article>
    </div>
  );
}
