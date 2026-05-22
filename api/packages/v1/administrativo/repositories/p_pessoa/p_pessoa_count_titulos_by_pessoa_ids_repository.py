from __future__ import annotations

from decimal import Decimal
from typing import Any

from abstracts.repository import BaseRepository


class CountTitulosByPessoaIdsRepository(BaseRepository):
    """
    Quantidade de títulos distintos em que cada pessoa participou,
    via P_PESSOA_VINCULO (vínculo) referenciando P_TITULO.
    """

    def execute(self, pessoa_ids: list[int]) -> dict[int, int]:
        unique_ids = sorted({int(i) for i in pessoa_ids if i is not None})
        if not unique_ids:
            return {}

        placeholders = ", ".join(f":id_{i}" for i in range(len(unique_ids)))
        params: dict[str, Any] = {f"id_{i}": value for i, value in enumerate(unique_ids)}
        sql = f"""
        SELECT
            v.PESSOA_ID AS PESSOA_ID,
            COUNT(DISTINCT v.TITULO_ID) AS TOTAL
        FROM P_PESSOA_VINCULO v
        INNER JOIN P_TITULO t ON t.TITULO_ID = v.TITULO_ID
        WHERE v.PESSOA_ID IN ({placeholders})
          AND v.TITULO_ID IS NOT NULL
        GROUP BY v.PESSOA_ID
        """
        rows = self.fetch_all(sql, params)
        counts: dict[int, int] = {pid: 0 for pid in unique_ids}
        for row in rows or []:
            pessoa_id = row.get("PESSOA_ID") or row.get("pessoa_id")
            total = row.get("TOTAL") or row.get("total") or 0
            if pessoa_id is None:
                continue
            if isinstance(pessoa_id, Decimal):
                pessoa_id = int(pessoa_id)
            if isinstance(total, Decimal):
                total = int(total)
            counts[int(pessoa_id)] = int(total)
        return counts
