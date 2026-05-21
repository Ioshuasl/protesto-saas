from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_livro_natureza import get_p_livro_natureza_model
from packages.v1.administrativo.schemas.p_livro_natureza_schema import (
    PLivroNaturezaSaveSchema,
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


class SaveRepository(BaseRepository):
    def execute(self, livro_natureza_schema: PLivroNaturezaSaveSchema):
        if use_orm_firebird():
            return self._execute_orm(livro_natureza_schema)
        return self._execute_sql(livro_natureza_schema)

    def _execute_orm(self, livro_natureza_schema: PLivroNaturezaSaveSchema) -> dict[str, Any]:
        payload = {
            "LIVRO_NATUREZA_ID": livro_natureza_schema.livro_natureza_id,
            "SIGLA": livro_natureza_schema.sigla,
            "DESCRICAO": livro_natureza_schema.descricao,
            "SITUACAO": situacao_to_db(livro_natureza_schema.situacao),
            "TIPO": None,
            "NATUREZA_ID": None,
        }
        created = get_p_livro_natureza_model().create(payload)
        return self._map_livro_natureza_row(created) or {}

    def _execute_sql(self, livro_natureza_schema: PLivroNaturezaSaveSchema) -> dict[str, Any]:
        try:
            sql = f"""
            INSERT INTO P_LIVRO_NATUREZA (
                LIVRO_NATUREZA_ID,
                SIGLA,
                DESCRICAO,
                SITUACAO,
                TIPO,
                NATUREZA_ID
            ) VALUES (
                :livro_natureza_id,
                :sigla,
                :descricao,
                :situacao,
                NULL,
                NULL
            )
            RETURNING
                {_SELECT_COLUMNS.strip()};
            """
            params = {
                "livro_natureza_id": livro_natureza_schema.livro_natureza_id,
                "sigla": livro_natureza_schema.sigla,
                "descricao": livro_natureza_schema.descricao,
                "situacao": situacao_to_db(livro_natureza_schema.situacao),
            }
            result = self.run_and_return(sql, params)
            return self._map_livro_natureza_row(result) or {}
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar natureza de livro: {exc}",
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
