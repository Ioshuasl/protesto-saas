from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.schemas.p_especie_schema import PEspecieEspecieSchema


class GetByEspecieRepository(BaseRepository):
    def execute(self, especie_schema: PEspecieEspecieSchema) -> Optional[dict[str, Any]]:
        if use_orm_firebird():
            return self._execute_orm(especie_schema)
        return self._execute_sql(especie_schema)

    def _execute_orm(self, especie_schema: PEspecieEspecieSchema) -> Optional[dict[str, Any]]:
        return self._execute_sql(especie_schema)

    def _execute_sql(self, especie_schema: PEspecieEspecieSchema) -> Optional[dict[str, Any]]:
        sql = """
        SELECT ESPECIE_ID, ESPECIE
        FROM P_ESPECIE
        WHERE UPPER(TRIM(ESPECIE)) = UPPER(TRIM(:especie))
        """
        params: dict[str, Any] = {"especie": especie_schema.especie}
        if especie_schema.especie_id is not None:
            sql += " AND ESPECIE_ID <> :especie_id"
            params["especie_id"] = especie_schema.especie_id
        row = self.fetch_one(sql, params)
        return self._map_row(row)

    @staticmethod
    def _map_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None
        especie_id = mapped.get("especie_id")
        if isinstance(especie_id, Decimal):
            mapped["especie_id"] = int(especie_id)
        especie = mapped.get("especie")
        if especie is not None:
            mapped["especie"] = str(especie).strip().upper() or None
        return mapped
