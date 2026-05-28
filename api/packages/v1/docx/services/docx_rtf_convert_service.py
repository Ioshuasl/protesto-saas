from __future__ import annotations

from pathlib import Path

from actions.data.rtf_normalizer import (
    decode_rtf_bytes,
    normalize_rtf_for_storage,
    prepare_rtf_for_libreoffice,
)
from packages.v1.docx.actions.soffice_convert_action import SofficeConvertAction


class DocxRtfConvertService:
    """
    Orquestra conversões DOCX <-> RTF reutilizando LibreOffice e normalização RTF.

    Fluxo alinhado ao código Node:
    - DOCX -> RTF (soffice) + normalize_rtf_for_storage (deduplica \\u + \\'XX)
    - RTF -> DOCX (prepare_rtf_for_libreoffice + soffice)
    - RTF -> HTML (soffice) para preview/extração quando necessário
    """

    @staticmethod
    def docx_bytes_to_rtf_text(
        docx_bytes: bytes,
        *,
        timeout_sec: int = 120,
    ) -> str:
        rtf_bytes = SofficeConvertAction.convert_bytes(
            docx_bytes,
            input_format="docx",
            output_format="rtf",
            timeout_sec=timeout_sec,
        )
        rtf_text = decode_rtf_bytes(rtf_bytes)
        return normalize_rtf_for_storage(rtf_text)

    @staticmethod
    def docx_bytes_to_rtf_bytes(
        docx_bytes: bytes,
        *,
        timeout_sec: int = 120,
    ) -> bytes:
        rtf_text = DocxRtfConvertService.docx_bytes_to_rtf_text(
            docx_bytes, timeout_sec=timeout_sec
        )
        encoding = prepare_rtf_for_libreoffice(rtf_text)[1]
        return rtf_text.encode(encoding, errors="replace")

    @staticmethod
    def rtf_text_to_docx_bytes(
        rtf_text: str,
        *,
        storage_dir: str = "./storage/temp",
        base_name: str = "document",
        timeout_sec: int = 180,
    ) -> bytes:
        diretorio = Path(storage_dir).resolve()
        diretorio.mkdir(parents=True, exist_ok=True)

        rtf_norm, write_encoding = prepare_rtf_for_libreoffice(rtf_text)
        rtf_path = diretorio / f"{base_name}.rtf"
        docx_path = diretorio / f"{base_name}.docx"

        rtf_path.write_text(rtf_norm, encoding=write_encoding, newline="", errors="replace")

        SofficeConvertAction.convert_file(
            rtf_path,
            "docx",
            diretorio,
            timeout_sec=timeout_sec,
        )

        if not docx_path.exists():
            raise FileNotFoundError(
                f"DOCX não gerado pelo LibreOffice: {docx_path}"
            )

        try:
            return docx_path.read_bytes()
        finally:
            for path in (rtf_path, docx_path):
                try:
                    path.unlink(missing_ok=True)
                except OSError:
                    pass

    @staticmethod
    def rtf_bytes_to_docx_bytes(
        rtf_bytes: bytes,
        *,
        storage_dir: str = "./storage/temp",
        base_name: str = "document",
        timeout_sec: int = 180,
    ) -> bytes:
        rtf_text = decode_rtf_bytes(rtf_bytes)
        return DocxRtfConvertService.rtf_text_to_docx_bytes(
            rtf_text,
            storage_dir=storage_dir,
            base_name=base_name,
            timeout_sec=timeout_sec,
        )

    @staticmethod
    def rtf_text_to_html(
        rtf_text: str,
        *,
        storage_dir: str = "./storage/temp",
        base_name: str = "document",
        timeout_sec: int = 120,
    ) -> str:
        """Equivalente a convertRtfToHtml do Node."""
        diretorio = Path(storage_dir).resolve()
        diretorio.mkdir(parents=True, exist_ok=True)

        rtf_norm, write_encoding = prepare_rtf_for_libreoffice(rtf_text)
        rtf_path = diretorio / f"{base_name}.rtf"
        rtf_path.write_text(rtf_norm, encoding=write_encoding, newline="", errors="replace")

        html_path = SofficeConvertAction.convert_file(
            rtf_path,
            "html",
            diretorio,
            timeout_sec=timeout_sec,
        )

        try:
            return html_path.read_text(encoding="utf-8", errors="replace")
        finally:
            for path in (rtf_path, html_path):
                try:
                    path.unlink(missing_ok=True)
                except OSError:
                    pass
