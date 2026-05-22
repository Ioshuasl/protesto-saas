from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.schemas.p_motivos_schema import PMotivosCodigoSchema


class GetByCodigoRepository(BaseRepository):
    def execute(self, codigo_schema: PMotivosCodigoSchema) -> Optional[dict[str, Any]]:
        if use_orm_firebird():
            return self._execute_orm(codigo_schema)
        return self._execute_sql(codigo_schema)

    def _execute_orm(self, codigo_schema: PMotivosCodigoSchema) -> Optional[dict[str, Any]]:
        return self._execute_sql(codigo_schema)

    def _execute_sql(self, codigo_schema: PMotivosCodigoSchema) -> Optional[dict[str, Any]]:
        sql = """
        SELECT MOTIVOS_ID, CODIGO
        FROM P_MOTIVOS
        WHERE UPPER(TRIM(CODIGO)) = UPPER(TRIM(:codigo))
        """
        params: dict[str, Any] = {"codigo": codigo_schema.codigo}
        if codigo_schema.motivos_id is not None:
            sql += " AND MOTIVOS_ID <> :motivos_id"
            params["motivos_id"] = codigo_schema.motivos_id
        row = self.fetch_one(sql, params)
        return self._map_row(row)

    @staticmethod
    def _map_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None
        motivos_id = mapped.get("motivos_id")
        if isinstance(motivos_id, Decimal):
            mapped["motivos_id"] = int(motivos_id)
        return mapped
