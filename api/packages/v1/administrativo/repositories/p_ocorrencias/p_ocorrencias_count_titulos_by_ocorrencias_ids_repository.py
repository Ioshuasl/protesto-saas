from __future__ import annotations

from decimal import Decimal
from typing import Any

from abstracts.repository import BaseRepository


class CountTitulosByOcorrenciasIdsRepository(BaseRepository):
    """Contagem de P_TITULO por OCORRENCIA_ID para várias ocorrências (index)."""

    def execute(self, ocorrencias_ids: list[int]) -> dict[int, int]:
        unique_ids = sorted({int(i) for i in ocorrencias_ids if i is not None})
        if not unique_ids:
            return {}

        placeholders = ", ".join(f":id_{i}" for i in range(len(unique_ids)))
        params: dict[str, Any] = {f"id_{i}": value for i, value in enumerate(unique_ids)}
        sql = f"""
        SELECT
            OCORRENCIA_ID AS OCORRENCIAS_ID,
            COUNT(*) AS TOTAL
        FROM P_TITULO
        WHERE OCORRENCIA_ID IN ({placeholders})
        GROUP BY OCORRENCIA_ID
        """
        rows = self.fetch_all(sql, params)
        counts: dict[int, int] = {oid: 0 for oid in unique_ids}
        for row in rows or []:
            ocorrencias_id = row.get("OCORRENCIAS_ID") or row.get("ocorrencias_id")
            total = row.get("TOTAL") or row.get("total") or 0
            if ocorrencias_id is None:
                continue
            if isinstance(ocorrencias_id, Decimal):
                ocorrencias_id = int(ocorrencias_id)
            if isinstance(total, Decimal):
                total = int(total)
            counts[int(ocorrencias_id)] = int(total)
        return counts
