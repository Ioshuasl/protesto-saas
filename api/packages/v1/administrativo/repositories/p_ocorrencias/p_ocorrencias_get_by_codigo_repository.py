from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.schemas.p_ocorrencias_schema import POcorrenciasCodigoSchema


class GetByCodigoRepository(BaseRepository):
    def execute(
        self, codigo_schema: POcorrenciasCodigoSchema
    ) -> Optional[dict[str, Any]]:
        if use_orm_firebird():
            return self._execute_orm(codigo_schema)
        return self._execute_sql(codigo_schema)

    def _execute_orm(
        self, codigo_schema: POcorrenciasCodigoSchema
    ) -> Optional[dict[str, Any]]:
        return self._execute_sql(codigo_schema)

    def _execute_sql(
        self, codigo_schema: POcorrenciasCodigoSchema
    ) -> Optional[dict[str, Any]]:
        sql = """
        SELECT OCORRENCIAS_ID, CODIGO
        FROM P_OCORRENCIAS
        WHERE UPPER(TRIM(CODIGO)) = UPPER(TRIM(:codigo))
        """
        params: dict[str, Any] = {"codigo": codigo_schema.codigo}
        if codigo_schema.ocorrencias_id is not None:
            sql += " AND OCORRENCIAS_ID <> :ocorrencias_id"
            params["ocorrencias_id"] = codigo_schema.ocorrencias_id
        row = self.fetch_one(sql, params)
        return self._map_row(row)

    @staticmethod
    def _map_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None
        ocorrencias_id = mapped.get("ocorrencias_id")
        if isinstance(ocorrencias_id, Decimal):
            mapped["ocorrencias_id"] = int(ocorrencias_id)
        return mapped
