from __future__ import annotations

from copy import deepcopy
from io import BytesIO
from pathlib import Path
from typing import Literal, Optional
import uuid

from docx import Document

from actions.data.base64 import Base64
from actions.data.text import Text


class DOCXAppendLastParagraphService:
    DOCX_MAGIC = b"PK\x03\x04"

    def execute(
        self,
        input_content,
        append_text: str,
        *,
        output: Literal["binary", "base64", "path"] = "binary",
        save_disk: bool = False,
        storage_dir: str = "./storage/temp",
        filename_prefix: Optional[str] = None,
        prepend_space: bool = True,
    ):
        docx_bytes = self._to_docx_bytes(input_content)
        merged_bytes = self._append_to_last_paragraph(
            docx_bytes=docx_bytes,
            append_text=append_text,
            prepend_space=prepend_space,
        )

        if output == "base64":
            return Base64.encode(merged_bytes)

        if output == "path" or save_disk:
            filename = self._save_docx_to_disk(
                docx_bytes=merged_bytes,
                storage_dir=storage_dir,
                filename_prefix=filename_prefix,
            )
            if output == "path":
                return filename

        return merged_bytes

    def _append_to_last_paragraph(
        self,
        *,
        docx_bytes: bytes,
        append_text,
        prepend_space: bool,
    ) -> bytes:
        append_docx, text = self._resolve_append_content(append_text)
        if append_docx is None and not text:
            return docx_bytes

        doc = Document(BytesIO(docx_bytes))
        if append_docx is not None:
            self._append_docx_inline_to_last_paragraph(doc, append_docx, prepend_space)
        else:
            self._append_plain_text_inline_to_last_paragraph(doc, text, prepend_space)

        output = BytesIO()
        doc.save(output)
        return output.getvalue()

    def _resolve_append_content(self, value) -> tuple[bytes | None, str]:
        if value is None:
            return None, ""

        if isinstance(value, str):
            if not Base64.is_valid(value):
                return None, value

        decoded = Base64.decode(value)
        normalized = Text.normalize_binary(decoded)

        if isinstance(normalized, (bytes, bytearray)) and bytes(normalized).startswith(
            self.DOCX_MAGIC
        ):
            return bytes(normalized), ""

        return None, Text.plain(normalized)

    def _append_plain_text_inline_to_last_paragraph(
        self, target_doc: Document, text: str, prepend_space: bool
    ) -> None:
        value = (text or "").strip()
        if not value:
            return

        if target_doc.paragraphs:
            last_paragraph = target_doc.paragraphs[-1]
        else:
            last_paragraph = target_doc.add_paragraph("")

        if prepend_space and (last_paragraph.text or "").strip():
            value = f" {value}"

        last_paragraph.add_run(value)

    def _append_docx_inline_to_last_paragraph(
        self, target_doc: Document, source_docx: bytes, prepend_space: bool
    ) -> None:
        source_doc = Document(BytesIO(source_docx))
        paragraphs = source_doc.paragraphs
        if not paragraphs:
            return

        if target_doc.paragraphs:
            last_paragraph = target_doc.paragraphs[-1]
        else:
            last_paragraph = target_doc.add_paragraph("")

        if prepend_space and (last_paragraph.text or "").strip():
            last_paragraph.add_run(" ")

        last_p = last_paragraph._p
        first = True
        for paragraph in paragraphs:
            if not first:
                last_paragraph.add_run(" ")
            first = False

            for run in paragraph.runs:
                last_p.append(deepcopy(run._r))

    def _to_docx_bytes(self, input_content) -> bytes:
        decoded = Base64.decode(input_content)
        normalized = Text.normalize_binary(decoded)

        if not isinstance(normalized, (bytes, bytearray)) or not normalized.startswith(
            self.DOCX_MAGIC
        ):
            raise ValueError("input_content deve conter um arquivo DOCX valido.")

        return bytes(normalized)

    def _save_docx_to_disk(
        self,
        *,
        docx_bytes: bytes,
        storage_dir: str,
        filename_prefix: Optional[str],
    ) -> str:
        directory = Path(storage_dir).resolve()
        directory.mkdir(parents=True, exist_ok=True)

        prefix = (filename_prefix or "docx_append_last_paragraph").strip().replace(" ", "_")
        filename = f"{prefix}_{uuid.uuid4().hex}.docx"
        path = directory / filename
        path.write_bytes(docx_bytes)
        return filename
