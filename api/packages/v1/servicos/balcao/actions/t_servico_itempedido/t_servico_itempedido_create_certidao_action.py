from pathlib import Path

from fastapi import HTTPException, status

from actions.data.rtf_normalizer import normalize_rtf_for_storage
from actions.data.text import Text
from packages.v1.docx.services.docx_rtf_convert_service import DocxRtfConvertService
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemPedidoCreateCertidaoSchema,
)


class ProcessDocumentAction:
    """
    Trata certidão em RTF ou DOCX.

    - RTF  -> normaliza e converte para DOCX via LibreOffice
    - DOCX -> salva direto, sem conversão
    """

    def execute(self, data: TServicoItemPedidoCreateCertidaoSchema):
        conteudo = ""
        if not data.certidao_texto:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Texto do documento vázio",
            )
        if data.certidao_texto is not None:
            conteudo = Text.decompress(data.certidao_texto) or ""
        diretorio = Path("./storage/temp").resolve()
        diretorio.mkdir(parents=True, exist_ok=True)

        base_name = str(data.servico_itempedido_id)

        docx_path = diretorio / f"{base_name}.docx"

        conteudo_strip = conteudo.lstrip()
        if conteudo_strip.startswith("PK\x03\x04"):
            docx_path.write_bytes(conteudo.encode("latin1"))
            return docx_path.name

        if not conteudo_strip.startswith("{\\rtf"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Conteúdo não é um RTF nem um DOCX válido",
            )

        texto_rtf = normalize_rtf_for_storage(conteudo_strip.strip())
        try:
            docx_bytes = DocxRtfConvertService.rtf_text_to_docx_bytes(
                texto_rtf,
                storage_dir=str(diretorio),
                base_name=base_name,
                timeout_sec=180,
            )
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao converter RTF para DOCX via LibreOffice",
            ) from exc

        if not docx_bytes.startswith(b"PK\x03\x04"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="DOCX não foi gerado pelo LibreOffice",
            )

        docx_path.write_bytes(docx_bytes)
        return docx_path.name
