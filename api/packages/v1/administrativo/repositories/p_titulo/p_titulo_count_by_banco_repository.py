from __future__ import annotations

from decimal import Decimal

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_titulo import get_p_titulo_model
from packages.v1.administrativo.schemas.p_banco_schema import PBancoIdSchema


class CountByBancoRepository(BaseRepository):
    def execute(self, banco_schema: PBancoIdSchema) -> int:
        if use_orm_firebird():
            return self._execute_orm(banco_schema)
        return self._execute_sql(banco_schema)

    def _execute_orm(self, banco_schema: PBancoIdSchema) -> int:
        total = get_p_titulo_model().count(
            {"where": {"BANCO_ID": banco_schema.banco_id}}
        )
        if isinstance(total, Decimal):
            return int(total)
        return int(total or 0)

    def _execute_sql(self, banco_schema: PBancoIdSchema) -> int:
        sql = """
        SELECT COUNT(*) AS TOTAL
        FROM P_TITULO
        WHERE BANCO_ID = :banco_id
        """
        row = self.fetch_one(sql, {"banco_id": banco_schema.banco_id})
        if row is None:
            return 0
        total = row.get("TOTAL") or row.get("total")
        if isinstance(total, Decimal):
            return int(total)
        return int(total or 0)
