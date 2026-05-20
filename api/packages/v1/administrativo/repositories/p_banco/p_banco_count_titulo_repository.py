from __future__ import annotations

from decimal import Decimal

from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.p_banco_schema import PBancoIdSchema


class CountTituloRepository(BaseRepository):
    def execute(self, banco_schema: PBancoIdSchema) -> int:
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
