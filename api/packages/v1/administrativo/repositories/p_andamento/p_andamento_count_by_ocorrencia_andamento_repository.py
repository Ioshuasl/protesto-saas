from __future__ import annotations

from decimal import Decimal

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_andamento import get_p_andamento_model
from packages.v1.administrativo.schemas.p_ocorrencia_andamento_schema import (
    POcorrenciaAndamentoIdSchema,
)


class CountByOcorrenciaAndamentoRepository(BaseRepository):
    def execute(self, ocorrencia_andamento_schema: POcorrenciaAndamentoIdSchema) -> int:
        if use_orm_firebird():
            return self._execute_orm(ocorrencia_andamento_schema)
        return self._execute_sql(ocorrencia_andamento_schema)

    def _execute_orm(self, ocorrencia_andamento_schema: POcorrenciaAndamentoIdSchema) -> int:
        total = get_p_andamento_model().count(
            {
                "where": {
                    "OCORRENCIA_ANDAMENTO_ID": ocorrencia_andamento_schema.ocorrencia_andamento_id
                }
            }
        )
        if isinstance(total, Decimal):
            return int(total)
        return int(total or 0)

    def _execute_sql(self, ocorrencia_andamento_schema: POcorrenciaAndamentoIdSchema) -> int:
        sql = """
        SELECT COUNT(*) AS TOTAL
        FROM P_ANDAMENTO
        WHERE OCORRENCIA_ANDAMENTO_ID = :ocorrencia_andamento_id
        """
        row = self.fetch_one(
            sql,
            {
                "ocorrencia_andamento_id": ocorrencia_andamento_schema.ocorrencia_andamento_id
            },
        )
        if row is None:
            return 0
        total = row.get("TOTAL") or row.get("total")
        if isinstance(total, Decimal):
            return int(total)
        return int(total or 0)
