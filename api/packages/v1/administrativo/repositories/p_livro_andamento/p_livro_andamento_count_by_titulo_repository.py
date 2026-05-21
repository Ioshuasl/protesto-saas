from __future__ import annotations

from decimal import Decimal

from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.p_livro_andamento_schema import (
    PLivroAndamentoIdSchema,
)


class CountByTituloRepository(BaseRepository):
    def execute(self, schema: PLivroAndamentoIdSchema) -> int:
        sql = """
        SELECT COUNT(*) AS TOTAL
        FROM P_TITULO
        WHERE LIVRO_ID_APONTAMENTO = :livro_andamento_id
           OR LIVRO_ID_PROTESTO = :livro_andamento_id
        """
        row = self.fetch_one(
            sql, {"livro_andamento_id": schema.livro_andamento_id}
        )
        if row is None:
            return 0
        total = row.get("TOTAL") or row.get("total") or 0
        if isinstance(total, Decimal):
            return int(total)
        return int(total)
