from __future__ import annotations

from decimal import Decimal
from typing import Any, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from packages.v1.administrativo.schemas.p_arquivo_titulo_schema import (
    PArquivoTituloIdSchema,
    decode_blob_conteudo,
)


class ShowTextoRepository(BaseRepository):
    """Leitura de TEXTO via SQL para materializar o BLOB completo (sem limite de repr ORM)."""

    def __init__(self) -> None:
        super().__init__(blob_in_base64=False)

    def execute(self, arquivo_schema: PArquivoTituloIdSchema) -> dict[str, Any]:
        return self._execute_sql(arquivo_schema)

    def _execute_sql(self, arquivo_schema: PArquivoTituloIdSchema) -> dict[str, Any]:
        sql = """
        SELECT ARQUIVO_TITULO_ID, TEXTO
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

        conteudo = decode_blob_conteudo(mapped.get("texto"))
        return {
            "arquivo_titulo_id": int(arquivo_id),
            "conteudo": conteudo,
            "tamanho": len(conteudo) if conteudo is not None else 0,
        }
