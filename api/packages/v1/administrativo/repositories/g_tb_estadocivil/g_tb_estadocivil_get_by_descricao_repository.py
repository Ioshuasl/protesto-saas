from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.g_tb_estadocivil import get_g_tb_estadocivil_model
from packages.v1.administrativo.schemas.g_tb_estadocivil_schema import GTbEstadoCivilDescricaoSchema

SITUACAO_CODIGO_INATIVO = "I"

_SELECT_COLUMNS = """
    TB_ESTADOCIVIL_ID,
    DESCRICAO,
    SITUACAO,
    SISTEMA_ID,
    TIPO
"""


class GetByDescricaoRepository(BaseRepository):
    def execute(self, estadocivil_schema: GTbEstadoCivilDescricaoSchema):
        if use_orm_firebird():
            return self._execute_orm(estadocivil_schema)
        return self._execute_sql(estadocivil_schema)

    def _execute_orm(
        self, estadocivil_schema: GTbEstadoCivilDescricaoSchema
    ) -> Optional[dict[str, Any]]:
        row = get_g_tb_estadocivil_model().findOne(
            {"where": {"DESCRICAO": estadocivil_schema.descricao}}
        )
        return self._map_row(row)

    def _execute_sql(
        self, estadocivil_schema: GTbEstadoCivilDescricaoSchema
    ) -> Optional[dict[str, Any]]:
        sql = f"""
        SELECT
            {_SELECT_COLUMNS.strip()}
        FROM G_TB_ESTADOCIVIL
        WHERE DESCRICAO = :descricao
        """
        params = {"descricao": estadocivil_schema.descricao}
        result = self.fetch_one(sql, params)
        return self._map_row(result)

    @staticmethod
    def _map_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        for key in ("tb_estadocivil_id", "sistema_id", "tipo"):
            value = mapped.get(key)
            if isinstance(value, Decimal):
                mapped[key] = int(value)

        situacao = mapped.get("situacao")
        if situacao is None or not str(situacao).strip():
            mapped["situacao"] = SITUACAO_CODIGO_INATIVO
        else:
            mapped["situacao"] = str(situacao).strip().upper()

        return mapped
