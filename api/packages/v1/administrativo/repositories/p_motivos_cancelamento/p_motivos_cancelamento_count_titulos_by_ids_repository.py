from __future__ import annotations

from decimal import Decimal
from typing import Any

from abstracts.repository import BaseRepository


class CountTitulosByMotivosCancelamentoIdsRepository(BaseRepository):
    """Contagem de P_TITULO por MOTIVO_CANCELAMENTO para vários IDs (index)."""

    def execute(self, motivos_cancelamento_ids: list[int]) -> dict[int, int]:
        unique_ids = sorted({int(i) for i in motivos_cancelamento_ids if i is not None})
        if not unique_ids:
            return {}

        placeholders = ", ".join(f":id_{i}" for i in range(len(unique_ids)))
        params: dict[str, Any] = {f"id_{i}": value for i, value in enumerate(unique_ids)}
        sql = f"""
        SELECT
            MOTIVO_CANCELAMENTO AS MOTIVOS_CANCELAMENTO_ID,
            COUNT(*) AS TOTAL
        FROM P_TITULO
        WHERE MOTIVO_CANCELAMENTO IN ({placeholders})
        GROUP BY MOTIVO_CANCELAMENTO
        """
        rows = self.fetch_all(sql, params)
        counts: dict[int, int] = {mid: 0 for mid in unique_ids}
        for row in rows or []:
            pk = row.get("MOTIVOS_CANCELAMENTO_ID") or row.get("motivos_cancelamento_id")
            total = row.get("TOTAL") or row.get("total") or 0
            if pk is None:
                continue
            if isinstance(pk, Decimal):
                pk = int(pk)
            if isinstance(total, Decimal):
                total = int(total)
            counts[int(pk)] = int(total)
        return counts
