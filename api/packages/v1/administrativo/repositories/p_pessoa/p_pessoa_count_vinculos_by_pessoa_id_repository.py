from __future__ import annotations

from decimal import Decimal

from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.p_pessoa_schema import PPessoaIdSchema


class CountVinculosByPessoaIdRepository(BaseRepository):
    def execute(self, schema: PPessoaIdSchema) -> int:
        sql = """
        SELECT COUNT(*) AS TOTAL
        FROM P_PESSOA_VINCULO
        WHERE PESSOA_ID = :pessoa_id
        """
        row = self.fetch_one(sql, {"pessoa_id": schema.pessoa_id}) or {}
        total = row.get("TOTAL") or row.get("total") or 0
        if isinstance(total, Decimal):
            return int(total)
        return int(total)
