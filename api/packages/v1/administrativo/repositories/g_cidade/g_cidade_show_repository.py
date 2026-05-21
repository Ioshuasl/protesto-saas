from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.g_cidade import get_g_cidade_model
from packages.v1.administrativo.schemas.g_cidade_schema import GCidadeIdSchema

_SELECT_COLUMNS = """
    CIDADE_ID,
    UF,
    CIDADE_NOME,
    CODIGO_IBGE,
    CODIGO_GYN
"""


class ShowRepository(BaseRepository):
    def execute(self, g_cidade_schema: GCidadeIdSchema):
        if use_orm_firebird():
            return self._execute_orm(g_cidade_schema)
        return self._execute_sql(g_cidade_schema)

    def _execute_orm(self, g_cidade_schema: GCidadeIdSchema) -> dict[str, Any]:
        row = get_g_cidade_model().findByPk(g_cidade_schema.cidade_id)
        result = self._map_row(row)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro não encontrado",
            )
        return result

    def _execute_sql(self, g_cidade_schema: GCidadeIdSchema) -> dict[str, Any]:
        try:
            sql = f"""
            SELECT
                {_SELECT_COLUMNS.strip()}
            FROM G_CIDADE
            WHERE CIDADE_ID = :cidade_id
            """
            params = {"cidade_id": g_cidade_schema.cidade_id}
            result = self.fetch_one(sql, params)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Registro não encontrado",
                )

            return self._map_row(result)
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar registro: {exc}",
            ) from exc

    @staticmethod
    def _map_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        cidade_id = mapped.get("cidade_id")
        if isinstance(cidade_id, Decimal):
            mapped["cidade_id"] = int(cidade_id)

        uf = mapped.get("uf")
        if uf is not None:
            mapped["uf"] = str(uf).strip().upper() or None

        return mapped
