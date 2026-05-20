from __future__ import annotations

from copy import deepcopy
from io import BytesIO
from pathlib import Path
from typing import Literal, Optional
import uuid

from docx import Document
from striprtf.striprtf import rtf_to_text

from actions.data.base64 import Base64
from actions.data.text import Text


class DOCXMergeModeloMinutaService:
    DOCX_MAGIC = b"PK\x03\x04"

    def execute(
        self,
        modelo_content,
        minuta_content,
        *,
        output: Literal["binary", "path"] = "binary",
        save_disk: bool = False,
        storage_dir: str = "./storage/temp",
        filename_prefix: Optional[str] = None,
    ):
        modelo_raw = self._to_bytes(
            Base64().decode(modelo_content),
            storage_dir=storage_dir,
        )
        minuta_raw = self._to_bytes(
            Base64().decode(minuta_content),
            storage_dir=storage_dir,
        )

        modelo = Text.normalize_binary(modelo_raw)
        minuta = Text.normalize_binary(minuta_raw)

        merged_docx = self._merge_to_docx(modelo, minuta)

        filename = None
        if output == "path" or save_disk:
            filename = self._save_docx_to_disk(
                docx_bytes=merged_docx,
                storage_dir=storage_dir,
                filename_prefix=filename_prefix,
            )

        if output == "path":
            return filename or ""
        return merged_docx

    def _merge_to_docx(self, modelo: bytes, minuta: bytes) -> bytes:
        if self._is_docx(modelo) and self._is_docx(minuta):
            return self._merge_docx(modelo, minuta)

        if self._is_docx(modelo):
            return self._append_text_to_docx(modelo, self._extract_plain_text(minuta))

        merged_text = self._extract_plain_text(modelo)
        minuta_text = self._extract_plain_text(minuta)
        if minuta_text:
            merged_text = f"{merged_text}\n\n{minuta_text}".strip() if merged_text else minuta_text

        return self._create_docx_with_text(merged_text)

    def _merge_docx(self, modelo_docx: bytes, minuta_docx: bytes) -> bytes:
        modelo_doc = Document(BytesIO(modelo_docx))
        minuta_doc = Document(BytesIO(minuta_docx))

        model_body = modelo_doc.element.body
        insert_at = len(model_body)
        if insert_at > 0 and model_body[-1].tag.endswith("}sectPr"):
            insert_at -= 1

        for node in minuta_doc.element.body.iterchildren():
            if node.tag.endswith("}sectPr"):
                continue
            model_body.insert(insert_at, deepcopy(node))
            insert_at += 1

        out = BytesIO()
        modelo_doc.save(out)
        return out.getvalue()

    def _append_text_to_docx(self, modelo_docx: bytes, minuta_text: str) -> bytes:
        if not minuta_text:
            return modelo_docx

        doc = Document(BytesIO(modelo_docx))
        for line in minuta_text.splitlines() or [""]:
            doc.add_paragraph(line)

        out = BytesIO()
        doc.save(out)
        return out.getvalue()

    def _create_docx_with_text(self, text: str) -> bytes:
        out = BytesIO()
        doc = Document()
        for line in (text or "").splitlines() or [""]:
            doc.add_paragraph(line)
        doc.save(out)
        return out.getvalue()

    def _extract_plain_text(self, content: bytes) -> str:
        if not content:
            return ""

        if self._is_rtf(content):
            try:
                return (rtf_to_text(content.decode("latin1", errors="ignore")) or "").strip()
            except Exception:
                return ""
        if self._is_docx(content):
            try:
                doc = Document(BytesIO(content))
                return "\n".join(
                    (p.text or "").strip() for p in doc.paragraphs if (p.text or "").strip()
                )
            except Exception:
                return ""
        return content.decode("utf-8", errors="ignore").strip()

    def _save_docx_to_disk(
        self,
        *,
        docx_bytes: bytes,
        storage_dir: str,
        filename_prefix: Optional[str],
    ) -> str:
        directory = Path(storage_dir).resolve()
        directory.mkdir(parents=True, exist_ok=True)

        prefix = (filename_prefix or "modelo_minuta").strip().replace(" ", "_")
        filename = f"{prefix}_{uuid.uuid4().hex}.docx"
        path = directory / filename
        path.write_bytes(docx_bytes)
        return filename

    def _is_docx(self, value: bytes) -> bool:
        return isinstance(value, bytes) and value.startswith(self.DOCX_MAGIC)

    def _is_rtf(self, value: bytes) -> bool:
        return isinstance(value, bytes) and value.lstrip().startswith(b"{\\rtf")

    def _try_read_file_bytes(self, value, storage_dir: Optional[str]) -> Optional[bytes]:
        raw = str(value).strip()
        if not raw:
            return None

        candidates = [Path(raw)]

        if storage_dir:
            path = Path(raw)
            if not path.is_absolute():
                candidates.append(Path(storage_dir) / path)

        for candidate in candidates:
            try:
                resolved = candidate.resolve()
            except Exception:
                resolved = candidate

            try:
                if resolved.exists() and resolved.is_file():
                    return resolved.read_bytes()
            except Exception:
                continue

        return None

    def _to_bytes(self, value, *, storage_dir: Optional[str] = None) -> bytes:
        if isinstance(value, bytes):
            return value
        if isinstance(value, bytearray):
            return bytes(value)
        if isinstance(value, memoryview):
            return value.tobytes()
        if isinstance(value, Path):
            file_bytes = self._try_read_file_bytes(value, storage_dir)
            if file_bytes is not None:
                return file_bytes
            return str(value).encode("utf-8")
        if isinstance(value, str):
            file_bytes = self._try_read_file_bytes(value, storage_dir)
            if file_bytes is not None:
                return file_bytes
            return value.encode("utf-8")
        if value is None:
            return b""
        return str(value).encode("utf-8")
