from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.g_tb_estadocivil import get_g_tb_estadocivil_model

SITUACAO_CODIGO_INATIVO = "I"

_SELECT_COLUMNS = """
    TB_ESTADOCIVIL_ID,
    DESCRICAO,
    SITUACAO,
    SISTEMA_ID,
    TIPO
"""


class IndexRepository(BaseRepository):
    def execute(self):
        if use_orm_firebird():
            return self._execute_orm()
        return self._execute_sql()

    def _execute_orm(self) -> list[dict[str, Any]]:
        rows = get_g_tb_estadocivil_model().findAll({})
        return [self._map_row(row) or {} for row in rows]

    def _execute_sql(self) -> list[dict[str, Any]]:
        sql = f"""
        SELECT
            {_SELECT_COLUMNS.strip()}
        FROM G_TB_ESTADOCIVIL
        """
        rows = self.fetch_all(sql)
        return [self._map_row(row) or {} for row in rows]

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
