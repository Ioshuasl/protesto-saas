from __future__ import annotations

from decimal import Decimal

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_titulo import get_p_titulo_model
from packages.v1.administrativo.schemas.p_especie_schema import PEspecieIdSchema


class CountByEspecieRepository(BaseRepository):
    def execute(self, especie_schema: PEspecieIdSchema) -> int:
        if use_orm_firebird():
            return self._execute_orm(especie_schema)
        return self._execute_sql(especie_schema)

    def _execute_orm(self, especie_schema: PEspecieIdSchema) -> int:
        total = get_p_titulo_model().count(
            {"where": {"ESPECIE_ID": especie_schema.especie_id}}
        )
        if isinstance(total, Decimal):
            return int(total)
        return int(total or 0)

    def _execute_sql(self, especie_schema: PEspecieIdSchema) -> int:
        sql = """
        SELECT COUNT(*) AS TOTAL
        FROM P_TITULO
        WHERE ESPECIE_ID = :especie_id
        """
        row = self.fetch_one(sql, {"especie_id": especie_schema.especie_id})
        if row is None:
            return 0
        total = row.get("TOTAL") or row.get("total")
        if isinstance(total, Decimal):
            return int(total)
        return int(total or 0)
