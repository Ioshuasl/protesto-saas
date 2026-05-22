from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.schemas.p_ocorrencia_andamento_schema import (
    POcorrenciaAndamentoCodigoSchema,
)


class GetByCodigoRepository(BaseRepository):
    def execute(
        self, ocorrencia_andamento_schema: POcorrenciaAndamentoCodigoSchema
    ) -> Optional[dict[str, Any]]:
        if use_orm_firebird():
            return self._execute_orm(ocorrencia_andamento_schema)
        return self._execute_sql(ocorrencia_andamento_schema)

    def _execute_orm(
        self, ocorrencia_andamento_schema: POcorrenciaAndamentoCodigoSchema
    ) -> Optional[dict[str, Any]]:
        return self._execute_sql(ocorrencia_andamento_schema)

    def _execute_sql(
        self, ocorrencia_andamento_schema: POcorrenciaAndamentoCodigoSchema
    ) -> Optional[dict[str, Any]]:
        sql = """
        SELECT OCORRENCIA_ANDAMENTO_ID, CODIGO
        FROM P_OCORRENCIA_ANDAMENTO
        WHERE UPPER(TRIM(CODIGO)) = UPPER(TRIM(:codigo))
        """
        params: dict[str, Any] = {"codigo": ocorrencia_andamento_schema.codigo}
        if ocorrencia_andamento_schema.ocorrencia_andamento_id is not None:
            sql += " AND OCORRENCIA_ANDAMENTO_ID <> :ocorrencia_andamento_id"
            params["ocorrencia_andamento_id"] = (
                ocorrencia_andamento_schema.ocorrencia_andamento_id
            )
        row = self.fetch_one(sql, params)
        return self._map_row(row)

    @staticmethod
    def _map_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None
        pk = mapped.get("ocorrencia_andamento_id")
        if isinstance(pk, Decimal):
            mapped["ocorrencia_andamento_id"] = int(pk)
        codigo = mapped.get("codigo")
        if codigo is not None:
            mapped["codigo"] = str(codigo).strip().upper() or None
        return mapped
