from __future__ import annotations

from decimal import Decimal
from typing import Any, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from packages.v1.administrativo.schemas.p_arquivo_titulo_schema import (
    PArquivoTituloIdSchema,
    decode_blob_conteudo,
    encode_arquivo_download_content,
    sanitize_arquivo_download_filename,
)


class DownloadRepository(BaseRepository):
    """Download do arquivo importado (NOME_ARQUIVO + TEXTO_IMPORTADO)."""

    def __init__(self) -> None:
        super().__init__(blob_in_base64=False)

    def execute(self, arquivo_schema: PArquivoTituloIdSchema) -> dict[str, Any]:
        sql = """
        SELECT ARQUIVO_TITULO_ID, NOME_ARQUIVO, TEXTO_IMPORTADO
        FROM P_ARQUIVO_TITULO
        WHERE ARQUIVO_TITULO_ID = :arquivo_titulo_id
        """
        row = self.fetch_one(
            sql, {"arquivo_titulo_id": arquivo_schema.arquivo_titulo_id}
        )
        return self._map_row(row, arquivo_schema.arquivo_titulo_id)

    @staticmethod
    def _map_row(
        row: Optional[dict[str, Any]],
        arquivo_titulo_id: int,
    ) -> dict[str, Any]:
        if row is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Arquivo de título não encontrado.",
            )

        mapped = normalize_row_keys(row)
        if mapped is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Arquivo de título não encontrado.",
            )

        arquivo_id = mapped.get("arquivo_titulo_id", arquivo_titulo_id)
        if isinstance(arquivo_id, Decimal):
            arquivo_id = int(arquivo_id)

        conteudo = decode_blob_conteudo(mapped.get("texto_importado"))
        if conteudo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conteúdo do arquivo (TEXTO_IMPORTADO) não disponível.",
            )

        nome_arquivo = mapped.get("nome_arquivo")
        if nome_arquivo is not None:
            nome_arquivo = str(nome_arquivo).strip() or None

        filename = sanitize_arquivo_download_filename(nome_arquivo, int(arquivo_id))
        content = encode_arquivo_download_content(conteudo)

        return {
            "arquivo_titulo_id": int(arquivo_id),
            "filename": filename,
            "content": content,
            "tamanho": len(content),
        }
