from __future__ import annotations

from decimal import Decimal

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_titulo import get_p_titulo_model
from packages.v1.administrativo.schemas.p_ocorrencias_schema import POcorrenciasIdSchema


class CountByOcorrenciaRepository(BaseRepository):
    def execute(self, ocorrencias_schema: POcorrenciasIdSchema) -> int:
        if use_orm_firebird():
            return self._execute_orm(ocorrencias_schema)
        return self._execute_sql(ocorrencias_schema)

    def _execute_orm(self, ocorrencias_schema: POcorrenciasIdSchema) -> int:
        total = get_p_titulo_model().count(
            {"where": {"OCORRENCIA_ID": ocorrencias_schema.ocorrencias_id}}
        )
        if isinstance(total, Decimal):
            return int(total)
        return int(total or 0)

    def _execute_sql(self, ocorrencias_schema: POcorrenciasIdSchema) -> int:
        sql = """
        SELECT COUNT(*) AS TOTAL
        FROM P_TITULO
        WHERE OCORRENCIA_ID = :ocorrencias_id
        """
        row = self.fetch_one(sql, {"ocorrencias_id": ocorrencias_schema.ocorrencias_id})
        if row is None:
            return 0
        total = row.get("TOTAL") or row.get("total")
        if isinstance(total, Decimal):
            return int(total)
        return int(total or 0)
