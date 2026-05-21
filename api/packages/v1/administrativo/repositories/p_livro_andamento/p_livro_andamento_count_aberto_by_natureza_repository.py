from __future__ import annotations

from decimal import Decimal

from abstracts.repository import BaseRepository


class CountAbertoByNaturezaRepository(BaseRepository):
    def execute(
        self,
        livro_natureza_id: int,
        exclude_livro_andamento_id: int | None = None,
    ) -> int:
        sql = """
        SELECT COUNT(*) AS TOTAL
        FROM P_LIVRO_ANDAMENTO
        WHERE LIVRO_NATUREZA_ID = :livro_natureza_id
          AND DATA_FECHAMENTO IS NULL
        """
        params: dict = {"livro_natureza_id": livro_natureza_id}
        if exclude_livro_andamento_id is not None:
            sql += " AND LIVRO_ANDAMENTO_ID <> :exclude_id"
            params["exclude_id"] = exclude_livro_andamento_id

        row = self.fetch_one(sql, params)
        if row is None:
            return 0
        total = row.get("TOTAL") or row.get("total") or 0
        if isinstance(total, Decimal):
            return int(total)
        return int(total)
