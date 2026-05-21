from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_especie import get_p_especie_model
from packages.v1.administrativo.schemas.p_especie_schema import (
    PEspecieIdSchema,
    normalize_especie_from_db,
)

_SELECT_COLUMNS = """
    ESPECIE_ID,
    ESPECIE,
    DESCRICAO
"""


class ShowRepository(BaseRepository):
    def execute(self, especie_schema: PEspecieIdSchema):
        if use_orm_firebird():
            return self._execute_orm(especie_schema)
        return self._execute_sql(especie_schema)

    def _execute_orm(self, especie_schema: PEspecieIdSchema) -> Optional[dict[str, Any]]:
        row = get_p_especie_model().findByPk(especie_schema.especie_id)
        return self._map_especie_row(row)

    def _execute_sql(self, especie_schema: PEspecieIdSchema) -> Optional[dict[str, Any]]:
        sql = f"""
        SELECT
            {_SELECT_COLUMNS.strip()}
        FROM P_ESPECIE
        WHERE ESPECIE_ID = :especie_id
        """
        row = self.fetch_one(sql, {"especie_id": especie_schema.especie_id})
        return self._map_especie_row(row)

    @staticmethod
    def _map_especie_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        especie_id = mapped.get("especie_id")
        if isinstance(especie_id, Decimal):
            mapped["especie_id"] = int(especie_id)

        mapped["especie"] = normalize_especie_from_db(mapped.get("especie"))

        descricao = mapped.get("descricao")
        if descricao is not None:
            mapped["descricao"] = str(descricao).strip() or None

        return mapped
