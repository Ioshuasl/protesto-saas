from __future__ import annotations

from decimal import Decimal

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_titulo import get_p_titulo_model
from packages.v1.administrativo.schemas.p_motivos_schema import PMotivosIdSchema


class CountByMotivoApontamentoRepository(BaseRepository):
    def execute(self, motivos_schema: PMotivosIdSchema) -> int:
        if use_orm_firebird():
            return self._execute_orm(motivos_schema)
        return self._execute_sql(motivos_schema)

    def _execute_orm(self, motivos_schema: PMotivosIdSchema) -> int:
        total = get_p_titulo_model().count(
            {"where": {"MOTIVO_APONTAMENTO_ID": motivos_schema.motivos_id}}
        )
        if isinstance(total, Decimal):
            return int(total)
        return int(total or 0)

    def _execute_sql(self, motivos_schema: PMotivosIdSchema) -> int:
        sql = """
        SELECT COUNT(*) AS TOTAL
        FROM P_TITULO
        WHERE MOTIVO_APONTAMENTO_ID = :motivos_id
        """
        row = self.fetch_one(sql, {"motivos_id": motivos_schema.motivos_id})
        if row is None:
            return 0
        total = row.get("TOTAL") or row.get("total")
        if isinstance(total, Decimal):
            return int(total)
        return int(total or 0)
