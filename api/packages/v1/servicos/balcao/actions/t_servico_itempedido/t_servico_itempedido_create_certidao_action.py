import os
import subprocess
from pathlib import Path

from fastapi import HTTPException, status

from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemPedidoCreateCertidaoSchema,
)
from actions.data.text import Text

# Caminho do LibreOffice (Windows)
SOFFICE_PATH = r"C:\Program Files\LibreOffice\program\soffice.exe"


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

        rtf_path = diretorio / f"{base_name}.rtf"
        docx_path = diretorio / f"{base_name}.docx"

        conteudo_strip = conteudo.lstrip()
        # DOCX é um ZIP e começa com PK\x03\x04
        if conteudo_strip.startswith("PK\x03\x04"):
            with open(docx_path, "wb") as f:
                f.write(conteudo.encode("latin1"))

            return docx_path.name
        if not conteudo_strip.startswith("{\\rtf"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Conteúdo não é um RTF nem um DOCX válido",
            )

        # Remove partes brancas do texto no início e fim
        texto_rtf = conteudo_strip.strip()
        with open(rtf_path, "w", encoding="cp1252", errors="replace") as f:
            f.write(texto_rtf)
        cmd = [
            SOFFICE_PATH,
            "--headless",
            "--nologo",
            "--nolockcheck",
            "--nodefault",
            "--nofirststartwizard",
            "--convert-to",
            "docx",
            "--outdir",
            str(diretorio),
            str(rtf_path),
        ]
        clean_env = {
            "SYSTEMROOT": os.environ.get("SYSTEMROOT", ""),
            "WINDIR": os.environ.get("WINDIR", ""),
            "PATH": os.environ.get("PATH", ""),
            "TEMP": os.environ.get("TEMP", ""),
            "TMP": os.environ.get("TMP", ""),
        }

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=180,
            env=clean_env,
        )

        if result.returncode != 0:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao converter RTF para DOCX via LibreOffice",
            )
        if not docx_path.exists():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="DOCX não foi gerado pelo LibreOffice",
            )
        return docx_path.name
