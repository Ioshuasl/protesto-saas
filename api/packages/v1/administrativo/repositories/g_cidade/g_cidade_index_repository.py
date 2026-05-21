from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.g_cidade import get_g_cidade_model
from packages.v1.administrativo.schemas.g_cidade_schema import GCidadeIndexSchema

_SELECT_COLUMNS = """
    CIDADE_ID,
    UF,
    CIDADE_NOME,
    CODIGO_IBGE,
    CODIGO_GYN
"""


class IndexRepository(BaseRepository):
    def execute(self, data: GCidadeIndexSchema):
        if use_orm_firebird():
            return self._execute_orm(data)
        return self._execute_sql(data)

    def _execute_orm(self, data: GCidadeIndexSchema) -> list[dict[str, Any]]:
        rows = get_g_cidade_model().findAll(
            {
                "where": {"UF": data.uf},
                "order": [("CIDADE_NOME", "ASC")],
            }
        )
        return [self._map_row(row) or {} for row in rows]

    def _execute_sql(self, data: GCidadeIndexSchema) -> list[dict[str, Any]]:
        sql = f"""
        SELECT
            {_SELECT_COLUMNS.strip()}
        FROM G_CIDADE
        WHERE UF = :uf
        ORDER BY CIDADE_NOME ASC
        """
        params = {"uf": data.uf}
        rows = self.fetch_all(sql, params)
        return [self._map_row(row) or {} for row in rows]

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
