from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.g_cidade import get_g_cidade_model
from packages.v1.administrativo.schemas.g_cidade_schema import GCidadeNomeSchema

_SELECT_COLUMNS = """
    CIDADE_ID,
    UF,
    CIDADE_NOME,
    CODIGO_IBGE,
    CODIGO_GYN
"""


class GetByNomeRepository(BaseRepository):
    def execute(self, g_cidade_schema: GCidadeNomeSchema):
        if use_orm_firebird():
            return self._execute_orm(g_cidade_schema)
        return self._execute_sql(g_cidade_schema)

    def _execute_orm(
        self, g_cidade_schema: GCidadeNomeSchema
    ) -> Optional[dict[str, Any]]:
        row = get_g_cidade_model().findOne(
            {"where": {"CIDADE_NOME": g_cidade_schema.cidade_nome}}
        )
        return self._map_row(row)

    def _execute_sql(
        self, g_cidade_schema: GCidadeNomeSchema
    ) -> Optional[dict[str, Any]]:
        sql = f"""
        SELECT
            {_SELECT_COLUMNS.strip()}
        FROM G_CIDADE
        WHERE CIDADE_NOME = :cidade_nome
        """
        params = {"cidade_nome": g_cidade_schema.cidade_nome}
        result = self.fetch_one(sql, params)
        return self._map_row(result)

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
