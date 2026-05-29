"""
Destaque visual das marcas WPTools no DOCX para o OnlyOffice.

Marcadores (Delphi / WPTools):
  «m»...«m»  — campo manual
  «a»...«a»  — campo automático
  «w»...«w»  — variável / placeholder geral (ex.: CERTIDAO_*)
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

from docx import Document
from docx.enum.text import WD_COLOR_INDEX
from docx.table import Table
from docx.text.paragraph import Paragraph

# Ordem: padrões mais específicos primeiro (evita sobreposição).
_MARKER_RULES: tuple[tuple[re.Pattern[str], WD_COLOR_INDEX], ...] = (
    (re.compile(r"«m».*?«m»", re.DOTALL), WD_COLOR_INDEX.YELLOW),
    (re.compile(r"«a».*?«a»", re.DOTALL), WD_COLOR_INDEX.BRIGHT_GREEN),
    (re.compile(r"«w».*?«w»", re.DOTALL), WD_COLOR_INDEX.TURQUOISE),
)


@dataclass(frozen=True)
class MarkerHighlightSpan:
    start: int
    end: int
    color: WD_COLOR_INDEX


def _collect_spans(text: str) -> list[MarkerHighlightSpan]:
    spans: list[MarkerHighlightSpan] = []
    for pattern, color in _MARKER_RULES:
        for match in pattern.finditer(text):
            spans.append(MarkerHighlightSpan(match.start(), match.end(), color))

    if not spans:
        return []

    spans.sort(key=lambda item: item.start)
    merged: list[MarkerHighlightSpan] = []
    for span in spans:
        if merged and span.start < merged[-1].end:
            continue
        merged.append(span)
    return merged


def _rewrite_paragraph_with_highlights(paragraph: Paragraph) -> bool:
    text = paragraph.text
    if "«" not in text:
        return False

    spans = _collect_spans(text)
    if not spans:
        return False

    parent = paragraph._element
    for child in list(parent):
        parent.remove(child)

    cursor = 0
    for span in spans:
        if span.start > cursor:
            paragraph.add_run(text[cursor : span.start])
        highlighted = paragraph.add_run(text[span.start : span.end])
        highlighted.font.highlight_color = span.color
        cursor = span.end

    if cursor < len(text):
        paragraph.add_run(text[cursor:])
    return True


def _process_paragraphs(paragraphs) -> int:
    count = 0
    for paragraph in paragraphs:
        if _rewrite_paragraph_with_highlights(paragraph):
            count += 1
    return count


def _process_table(table: Table) -> int:
    count = 0
    for row in table.rows:
        for cell in row.cells:
            count += _process_paragraphs(cell.paragraphs)
            for nested in cell.tables:
                count += _process_table(nested)
    return count


def apply_marker_highlights_to_docx_bytes(docx_bytes: bytes) -> bytes:
    if not docx_bytes or not docx_bytes.startswith(b"PK\x03\x04"):
        return docx_bytes

    document = Document(BytesIO(docx_bytes))
    _process_paragraphs(document.paragraphs)
    for table in document.tables:
        _process_table(table)

    buffer = BytesIO()
    document.save(buffer)
    buffer.seek(0)
    return buffer.read()


def apply_marker_highlights_to_docx_path(path: Path) -> int:
    path = path.resolve()
    updated = apply_marker_highlights_to_docx_bytes(path.read_bytes())
    path.write_bytes(updated)
    document = Document(BytesIO(updated))
    return sum(1 for p in document.paragraphs if "«" in p.text)


def strip_marker_highlights_from_docx_bytes(docx_bytes: bytes) -> bytes:
    """Remove destaque antes de DOCX -> RTF (não persiste cor no BLOB)."""
    if not docx_bytes or not docx_bytes.startswith(b"PK\x03\x04"):
        return docx_bytes

    document = Document(BytesIO(docx_bytes))
    changed = False

    def _clear_runs(paragraphs) -> None:
        nonlocal changed
        for paragraph in paragraphs:
            for run in paragraph.runs:
                if run.font.highlight_color is not None:
                    run.font.highlight_color = None
                    changed = True

    _clear_runs(document.paragraphs)
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                _clear_runs(cell.paragraphs)

    if not changed:
        return docx_bytes

    buffer = BytesIO()
    document.save(buffer)
    buffer.seek(0)
    return buffer.read()
