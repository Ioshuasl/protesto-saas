from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_livro_andamento import get_p_livro_andamento_model
from packages.v1.administrativo.schemas.p_livro_andamento_schema import (
    PLivroAndamentoUpdateSchema,
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


class UpdateRepository(BaseRepository):
    def execute(
        self, livro_andamento_id: int, livro_andamento_schema: PLivroAndamentoUpdateSchema
    ) -> dict[str, Any]:
        if use_orm_firebird():
            return self._execute_orm(livro_andamento_id, livro_andamento_schema)
        return self._execute_sql(livro_andamento_id, livro_andamento_schema)

    def _execute_orm(
        self, livro_andamento_id: int, livro_andamento_schema: PLivroAndamentoUpdateSchema
    ) -> dict[str, Any]:
        payload = livro_andamento_schema.model_dump(exclude_none=True)
        if not payload:
            row = get_p_livro_andamento_model().findByPk(livro_andamento_id)
            return self._map_livro_andamento_row(row) or {}

        orm_payload: dict[str, Any] = {}
        field_map = {
            "livro_natureza_id": "LIVRO_NATUREZA_ID",
            "folha_atual": "FOLHA_ATUAL",
            "numero_livro": "NUMERO_LIVRO",
            "numero_folhas": "NUMERO_FOLHAS",
            "data_abertura": "DATA_ABERTURA",
            "data_fechamento": "DATA_FECHAMENTO",
            "sigla": "SIGLA",
            "usuario_id": "USUARIO_ID",
        }
        for key, column in field_map.items():
            if key in payload:
                orm_payload[column] = payload[key]

        get_p_livro_andamento_model().update(
            orm_payload, {"where": {"LIVRO_ANDAMENTO_ID": livro_andamento_id}}
        )
        row = get_p_livro_andamento_model().findByPk(livro_andamento_id)
        return self._map_livro_andamento_row(row) or {}

    def _execute_sql(
        self, livro_andamento_id: int, livro_andamento_schema: PLivroAndamentoUpdateSchema
    ) -> dict[str, Any]:
        payload = livro_andamento_schema.model_dump(exclude_none=True)
        if not payload:
            sql = f"""
            SELECT {_SELECT_COLUMNS.strip()}
            FROM P_LIVRO_ANDAMENTO
            WHERE LIVRO_ANDAMENTO_ID = :livro_andamento_id
            """
            row = self.fetch_one(sql, {"livro_andamento_id": livro_andamento_id})
            return self._map_livro_andamento_row(row) or {}

        set_parts: list[str] = []
        params: dict[str, Any] = {"livro_andamento_id": livro_andamento_id}
        field_map = {
            "livro_natureza_id": "LIVRO_NATUREZA_ID",
            "folha_atual": "FOLHA_ATUAL",
            "numero_livro": "NUMERO_LIVRO",
            "numero_folhas": "NUMERO_FOLHAS",
            "data_abertura": "DATA_ABERTURA",
            "data_fechamento": "DATA_FECHAMENTO",
            "sigla": "SIGLA",
            "usuario_id": "USUARIO_ID",
        }
        for key, column in field_map.items():
            if key in payload:
                set_parts.append(f"{column} = :{key}")
                params[key] = payload[key]

        try:
            sql = f"""
            UPDATE P_LIVRO_ANDAMENTO
            SET {", ".join(set_parts)}
            WHERE LIVRO_ANDAMENTO_ID = :livro_andamento_id
            RETURNING {_SELECT_COLUMNS.strip()};
            """
            result = self.run_and_return(sql, params)
            return self._map_livro_andamento_row(result) or {}
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar livro de andamento: {exc}",
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
