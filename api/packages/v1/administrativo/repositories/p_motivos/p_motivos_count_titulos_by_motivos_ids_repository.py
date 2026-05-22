from __future__ import annotations

from decimal import Decimal
from typing import Any

from abstracts.repository import BaseRepository


class CountTitulosByMotivosIdsRepository(BaseRepository):
    """Contagem de P_TITULO por MOTIVO_APONTAMENTO_ID para vários motivos (index)."""

    def execute(self, motivos_ids: list[int]) -> dict[int, int]:
        unique_ids = sorted({int(i) for i in motivos_ids if i is not None})
        if not unique_ids:
            return {}

        placeholders = ", ".join(f":id_{i}" for i in range(len(unique_ids)))
        params: dict[str, Any] = {f"id_{i}": value for i, value in enumerate(unique_ids)}
        sql = f"""
        SELECT
            MOTIVO_APONTAMENTO_ID AS MOTIVOS_ID,
            COUNT(*) AS TOTAL
        FROM P_TITULO
        WHERE MOTIVO_APONTAMENTO_ID IN ({placeholders})
        GROUP BY MOTIVO_APONTAMENTO_ID
        """
        rows = self.fetch_all(sql, params)
        counts: dict[int, int] = {mid: 0 for mid in unique_ids}
        for row in rows or []:
            motivos_id = row.get("MOTIVOS_ID") or row.get("motivos_id")
            total = row.get("TOTAL") or row.get("total") or 0
            if motivos_id is None:
                continue
            if isinstance(motivos_id, Decimal):
                motivos_id = int(motivos_id)
            if isinstance(total, Decimal):
                total = int(total)
            counts[int(motivos_id)] = int(total)
        return counts
