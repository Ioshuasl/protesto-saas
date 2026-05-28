from __future__ import annotations

from fastapi import HTTPException, status

from packages.v1.docx.services.docx_rtf_convert_service import DocxRtfConvertService


class DOCXConvertToRTFAction:
    """Converte DOCX para RTF via LibreOffice com normalização pós-conversão."""

    @staticmethod
    def execute(docx_bytes: bytes, timeout_sec: int = 120) -> bytes:
        if not docx_bytes or not docx_bytes.startswith(b"PK\x03\x04"):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Arquivo inválido para conversão DOCX -> RTF.",
            )

        return DocxRtfConvertService.docx_bytes_to_rtf_bytes(
            docx_bytes,
            timeout_sec=timeout_sec,
        )
