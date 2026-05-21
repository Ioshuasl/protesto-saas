from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_livro_natureza import get_p_livro_natureza_model
from packages.v1.administrativo.schemas.p_livro_natureza_schema import (
    PLivroNaturezaUpdateSchema,
    normalize_sigla_from_db,
    situacao_from_db,
    situacao_to_db,
)

_SELECT_COLUMNS = """
    LIVRO_NATUREZA_ID,
    SIGLA,
    DESCRICAO,
    SITUACAO
"""


class UpdateRepository(BaseRepository):
    def execute(self, livro_natureza_id: int, livro_natureza_schema: PLivroNaturezaUpdateSchema):
        if use_orm_firebird():
            return self._execute_orm(livro_natureza_id, livro_natureza_schema)
        return self._execute_sql(livro_natureza_id, livro_natureza_schema)

    def _execute_orm(
        self, livro_natureza_id: int, livro_natureza_schema: PLivroNaturezaUpdateSchema
    ) -> dict[str, Any]:
        payload = livro_natureza_schema.model_dump(exclude_none=True)
        if not payload:
            row = get_p_livro_natureza_model().findByPk(livro_natureza_id)
            return self._map_livro_natureza_row(row) or {}

        orm_payload: dict[str, Any] = {"TIPO": None}
        if "sigla" in payload:
            orm_payload["SIGLA"] = payload["sigla"]
        if "descricao" in payload:
            orm_payload["DESCRICAO"] = payload["descricao"]
        if "situacao" in payload:
            orm_payload["SITUACAO"] = situacao_to_db(payload["situacao"])

        get_p_livro_natureza_model().update(
            orm_payload, {"where": {"LIVRO_NATUREZA_ID": livro_natureza_id}}
        )
        row = get_p_livro_natureza_model().findByPk(livro_natureza_id)
        return self._map_livro_natureza_row(row) or {}

    def _execute_sql(
        self, livro_natureza_id: int, livro_natureza_schema: PLivroNaturezaUpdateSchema
    ) -> dict[str, Any]:
        payload = livro_natureza_schema.model_dump(exclude_none=True)
        if not payload:
            sql = f"""
            SELECT {_SELECT_COLUMNS.strip()}
            FROM P_LIVRO_NATUREZA
            WHERE LIVRO_NATUREZA_ID = :livro_natureza_id
            """
            row = self.fetch_one(sql, {"livro_natureza_id": livro_natureza_id})
            return self._map_livro_natureza_row(row) or {}

        set_parts: list[str] = ["TIPO = NULL"]
        params: dict[str, Any] = {"livro_natureza_id": livro_natureza_id}

        if "sigla" in payload:
            set_parts.append("SIGLA = :sigla")
            params["sigla"] = payload["sigla"]
        if "descricao" in payload:
            set_parts.append("DESCRICAO = :descricao")
            params["descricao"] = payload["descricao"]
        if "situacao" in payload:
            set_parts.append("SITUACAO = :situacao")
            params["situacao"] = situacao_to_db(payload["situacao"])

        try:
            sql = f"""
            UPDATE P_LIVRO_NATUREZA
            SET {", ".join(set_parts)}
            WHERE LIVRO_NATUREZA_ID = :livro_natureza_id
            RETURNING
                {_SELECT_COLUMNS.strip()};
            """
            result = self.run_and_return(sql, params)
            return self._map_livro_natureza_row(result) or {}
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar natureza de livro: {exc}",
            ) from exc

    @staticmethod
    def _map_livro_natureza_row(
        row: Optional[Mapping[str, Any]],
    ) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        livro_natureza_id = mapped.get("livro_natureza_id")
        if isinstance(livro_natureza_id, Decimal):
            mapped["livro_natureza_id"] = int(livro_natureza_id)

        mapped["sigla"] = normalize_sigla_from_db(mapped.get("sigla"))

        descricao = mapped.get("descricao")
        if descricao is not None:
            mapped["descricao"] = str(descricao).strip() or None

        mapped["situacao"] = situacao_from_db(mapped.get("situacao"))
        mapped.pop("tipo", None)
        mapped.pop("natureza_id", None)

        return mapped
