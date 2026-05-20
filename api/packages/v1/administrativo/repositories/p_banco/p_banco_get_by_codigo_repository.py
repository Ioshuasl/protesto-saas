from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_banco import get_p_banco_model
from packages.v1.administrativo.schemas.p_banco_schema import PBancoCodigoSchema


class GetByCodigoRepository(BaseRepository):
    def execute(self, codigo_schema: PBancoCodigoSchema) -> Optional[dict[str, Any]]:
        if use_orm_firebird():
            return self._execute_orm(codigo_schema)
        return self._execute_sql(codigo_schema)

    def _execute_orm(self, codigo_schema: PBancoCodigoSchema) -> Optional[dict[str, Any]]:
        return self._execute_sql(codigo_schema)

    def _execute_sql(self, codigo_schema: PBancoCodigoSchema) -> Optional[dict[str, Any]]:
        sql = """
        SELECT BANCO_ID, CODIGO_BANCO
        FROM P_BANCO
        WHERE UPPER(TRIM(CODIGO_BANCO)) = UPPER(TRIM(:codigo_banco))
        """
        params: dict[str, Any] = {"codigo_banco": codigo_schema.codigo_banco}
        if codigo_schema.banco_id is not None:
            sql += " AND BANCO_ID <> :banco_id"
            params["banco_id"] = codigo_schema.banco_id
        row = self.fetch_one(sql, params)
        return self._map_row(row)

    @staticmethod
    def _map_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None
        banco_id = mapped.get("banco_id")
        if isinstance(banco_id, Decimal):
            mapped["banco_id"] = int(banco_id)
        return mapped
