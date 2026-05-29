import pytest
from docx import Document
from docx.enum.text import WD_COLOR_INDEX
from io import BytesIO

from packages.v1.docx.services.docx_wptools_marker_highlight_service import (
    apply_marker_highlights_to_docx_bytes,
    strip_marker_highlights_from_docx_bytes,
)


def _build_docx(text: str) -> bytes:
    document = Document()
    document.add_paragraph(text)
    buffer = BytesIO()
    document.save(buffer)
    buffer.seek(0)
    return buffer.read()


@pytest.mark.unit
def test_apply_highlights_wptools_markers():
    docx = _build_docx("Texto «w»CERTIDAO_NOME«w» e «m»campo«m» e «a»auto«a»")
    highlighted = apply_marker_highlights_to_docx_bytes(docx)
    document = Document(BytesIO(highlighted))
    paragraph = document.paragraphs[0]
    colors = {run.font.highlight_color for run in paragraph.runs if run.font.highlight_color}
    assert WD_COLOR_INDEX.TURQUOISE in colors
    assert WD_COLOR_INDEX.YELLOW in colors
    assert WD_COLOR_INDEX.BRIGHT_GREEN in colors


@pytest.mark.unit
def test_strip_highlights_before_save():
    docx = _build_docx("«w»VAR«w»")
    highlighted = apply_marker_highlights_to_docx_bytes(docx)
    stripped = strip_marker_highlights_from_docx_bytes(highlighted)
    document = Document(BytesIO(stripped))
    assert all(run.font.highlight_color is None for run in document.paragraphs[0].runs)
