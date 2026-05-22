from __future__ import annotations

from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.p_titulo_schema import PTituloIdSchema


class CountDependentsRepository(BaseRepository):
    def execute(self, titulo_schema: PTituloIdSchema) -> dict[str, int]:
        params = {"titulo_id": titulo_schema.titulo_id}

        vinculos_row = self.fetch_one(
            """
            SELECT COUNT(*) AS TOTAL
            FROM P_PESSOA_VINCULO
            WHERE TITULO_ID = :titulo_id
            """,
            params,
        ) or {}
        andamentos_row = self.fetch_one(
            """
            SELECT COUNT(*) AS TOTAL
            FROM P_ANDAMENTO
            WHERE TITULO_ID = :titulo_id
            """,
            params,
        ) or {}

        return {
            "pessoa_vinculos": int(
                vinculos_row.get("TOTAL") or vinculos_row.get("total") or 0
            ),
            "andamentos": int(
                andamentos_row.get("TOTAL") or andamentos_row.get("total") or 0
            ),
        }
