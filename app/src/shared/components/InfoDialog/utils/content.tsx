'use client';

import React from 'react';

export type InfoDialogContent = React.ReactNode | string | Record<string, unknown> | unknown[];

function escapeHtml(value: string) {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function parseInlineMarkdown(markdown: string) {
  return markdown
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/`(.+?)`/g, '<code class="rounded bg-muted px-1 py-0.5 text-xs">$1</code>')
    .replace(/\[(.+?)\]\((.+?)\)/g, '<a class="text-primary underline" href="$2" target="_blank" rel="noreferrer">$1</a>');
}

function markdownToHtml(markdown: string) {
  const escaped = escapeHtml(markdown);
  const lines = escaped.split('\n');
  const html: string[] = [];
  let insideList = false;

  lines.forEach((line) => {
    if (/^\s*[-*]\s+/.test(line)) {
      if (!insideList) {
        html.push('<ul class="ml-5 list-disc space-y-1">');
        insideList = true;
      }
      html.push(`<li>${parseInlineMarkdown(line.replace(/^\s*[-*]\s+/, ''))}</li>`);
      return;
    }

    if (insideList) {
      html.push('</ul>');
      insideList = false;
    }

    if (/^###\s+/.test(line)) {
      html.push(`<h3 class="text-base font-semibold">${parseInlineMarkdown(line.replace(/^###\s+/, ''))}</h3>`);
      return;
    }

    if (/^##\s+/.test(line)) {
      html.push(`<h2 class="text-lg font-semibold">${parseInlineMarkdown(line.replace(/^##\s+/, ''))}</h2>`);
      return;
    }

    if (/^#\s+/.test(line)) {
      html.push(`<h1 class="text-xl font-semibold">${parseInlineMarkdown(line.replace(/^#\s+/, ''))}</h1>`);
      return;
    }

    if (!line.trim()) {
      html.push('<br />');
      return;
    }

    html.push(`<p>${parseInlineMarkdown(line)}</p>`);
  });

  if (insideList) {
    html.push('</ul>');
  }

  return html.join('');
}

function looksLikeHtml(content: string) {
  return /<[a-z][\s\S]*>/i.test(content);
}

function looksLikeMarkdown(content: string) {
  return /(^#{1,3}\s)|(\*\*.+?\*\*)|(\*.+?\*)|(\[[^\]]+\]\([^)]+\))|(^\s*[-*]\s+)/m.test(content);
}

export function renderInfoContent(content?: InfoDialogContent) {
  if (content == null) return null;

  if (React.isValidElement(content)) {
    return content;
  }

  if (typeof content === 'string') {
    if (looksLikeHtml(content)) {
      return <div className="max-h-[55vh] overflow-auto rounded-md border p-3" dangerouslySetInnerHTML={{ __html: content }} />;
    }

    if (looksLikeMarkdown(content)) {
      const markdownHtml = markdownToHtml(content);
      return <div className="max-h-[55vh] space-y-2 overflow-auto rounded-md border p-3" dangerouslySetInnerHTML={{ __html: markdownHtml }} />;
    }

    return <div className="max-h-[55vh] overflow-auto whitespace-pre-wrap rounded-md border p-3 text-sm">{content}</div>;
  }

  return (
    <pre className="max-h-[55vh] overflow-auto rounded-md border p-3 text-xs">
      {JSON.stringify(content, null, 2)}
    </pre>
  );
}
