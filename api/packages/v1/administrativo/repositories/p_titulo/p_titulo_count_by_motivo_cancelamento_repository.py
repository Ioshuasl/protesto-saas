from __future__ import annotations

from decimal import Decimal

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_titulo import get_p_titulo_model
from packages.v1.administrativo.schemas.p_motivos_cancelamento_schema import (
    PMotivosCancelamentoIdSchema,
)


class CountByMotivoCancelamentoRepository(BaseRepository):
    def execute(self, motivos_cancelamento_schema: PMotivosCancelamentoIdSchema) -> int:
        if use_orm_firebird():
            return self._execute_orm(motivos_cancelamento_schema)
        return self._execute_sql(motivos_cancelamento_schema)

    def _execute_orm(
        self, motivos_cancelamento_schema: PMotivosCancelamentoIdSchema
    ) -> int:
        total = get_p_titulo_model().count(
            {
                "where": {
                    "MOTIVO_CANCELAMENTO": motivos_cancelamento_schema.motivos_cancelamento_id
                }
            }
        )
        if isinstance(total, Decimal):
            return int(total)
        return int(total or 0)

    def _execute_sql(
        self, motivos_cancelamento_schema: PMotivosCancelamentoIdSchema
    ) -> int:
        sql = """
        SELECT COUNT(*) AS TOTAL
        FROM P_TITULO
        WHERE MOTIVO_CANCELAMENTO = :motivos_cancelamento_id
        """
        row = self.fetch_one(
            sql,
            {
                "motivos_cancelamento_id": motivos_cancelamento_schema.motivos_cancelamento_id
            },
        )
        if row is None:
            return 0
        total = row.get("TOTAL") or row.get("total")
        if isinstance(total, Decimal):
            return int(total)
        return int(total or 0)
