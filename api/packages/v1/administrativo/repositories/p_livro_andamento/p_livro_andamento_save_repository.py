from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_livro_andamento import get_p_livro_andamento_model
from packages.v1.administrativo.schemas.p_livro_andamento_schema import (
    PLivroAndamentoSaveSchema,
    is_livro_aberto,
    normalize_sigla,
)

_SELECT_COLUMNS = """
    LIVRO_ANDAMENTO_ID,
    LIVRO_NATUREZA_ID,
    FOLHA_ATUAL,
    NUMERO_LIVRO,
    DATA_ABERTURA,
    DATA_FECHAMENTO,
    NUMERO_FOLHAS,
    SIGLA,
    USUARIO_ID
"""


class SaveRepository(BaseRepository):
    def execute(self, livro_andamento_schema: PLivroAndamentoSaveSchema) -> dict[str, Any]:
        if use_orm_firebird():
            return self._execute_orm(livro_andamento_schema)
        return self._execute_sql(livro_andamento_schema)

    def _execute_orm(self, livro_andamento_schema: PLivroAndamentoSaveSchema) -> dict[str, Any]:
        payload = {
            "LIVRO_ANDAMENTO_ID": livro_andamento_schema.livro_andamento_id,
            "LIVRO_NATUREZA_ID": livro_andamento_schema.livro_natureza_id,
            "FOLHA_ATUAL": livro_andamento_schema.folha_atual,
            "NUMERO_LIVRO": livro_andamento_schema.numero_livro,
            "NUMERO_FOLHAS": livro_andamento_schema.numero_folhas,
            "DATA_ABERTURA": livro_andamento_schema.data_abertura,
            "DATA_FECHAMENTO": livro_andamento_schema.data_fechamento,
            "SIGLA": livro_andamento_schema.sigla,
            "USUARIO_ID": livro_andamento_schema.usuario_id,
        }
        created = get_p_livro_andamento_model().create(payload)
        return self._map_livro_andamento_row(created) or {}

    def _execute_sql(self, livro_andamento_schema: PLivroAndamentoSaveSchema) -> dict[str, Any]:
        try:
            sql = f"""
            INSERT INTO P_LIVRO_ANDAMENTO (
                LIVRO_ANDAMENTO_ID,
                LIVRO_NATUREZA_ID,
                FOLHA_ATUAL,
                NUMERO_LIVRO,
                NUMERO_FOLHAS,
                DATA_ABERTURA,
                DATA_FECHAMENTO,
                SIGLA,
                USUARIO_ID
            ) VALUES (
                :livro_andamento_id,
                :livro_natureza_id,
                :folha_atual,
                :numero_livro,
                :numero_folhas,
                :data_abertura,
                :data_fechamento,
                :sigla,
                :usuario_id
            )
            RETURNING {_SELECT_COLUMNS.strip()};
            """
            params = {
                "livro_andamento_id": livro_andamento_schema.livro_andamento_id,
                "livro_natureza_id": livro_andamento_schema.livro_natureza_id,
                "folha_atual": livro_andamento_schema.folha_atual,
                "numero_livro": livro_andamento_schema.numero_livro,
                "numero_folhas": livro_andamento_schema.numero_folhas,
                "data_abertura": livro_andamento_schema.data_abertura,
                "data_fechamento": livro_andamento_schema.data_fechamento,
                "sigla": livro_andamento_schema.sigla,
                "usuario_id": livro_andamento_schema.usuario_id,
            }
            result = self.run_and_return(sql, params)
            return self._map_livro_andamento_row(result) or {}
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar livro de andamento: {exc}",
            ) from exc

    @staticmethod
    def _map_livro_andamento_row(
        row: Optional[Mapping[str, Any]],
    ) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        for key in (
            "livro_andamento_id",
            "livro_natureza_id",
            "folha_atual",
            "numero_livro",
            "numero_folhas",
            "usuario_id",
        ):
            val = mapped.get(key)
            if isinstance(val, Decimal):
                mapped[key] = int(val)

        sigla = mapped.get("sigla")
        if sigla is not None:
            mapped["sigla"] = normalize_sigla(str(sigla))

        mapped["aberto"] = is_livro_aberto(mapped.get("data_fechamento"))
        return mapped
