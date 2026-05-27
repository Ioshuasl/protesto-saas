from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys


class TabelionatoProtestoDashboardResumoRepository(BaseRepository):
    def execute(self) -> dict[str, int | float | None]:
        sql = """
        SELECT
            COUNT(*) AS TOTAL_TITULOS,
            SUM(
                CASE
                    WHEN t.DATA_APONTAMENTO IS NOT NULL
                     AND t.DATA_INTIMACAO IS NOT NULL
                     AND t.DATA_PROTESTO IS NULL
                    THEN 1
                    ELSE 0
                END
            ) AS TITULOS_EM_TRIDUO,
            SUM(
                CASE
                    WHEN t.DATA_APONTAMENTO IS NOT NULL
                     AND t.DATA_INTIMACAO IS NOT NULL
                     AND t.DATA_PROTESTO IS NULL
                     AND t.DATA_DESISTENCIA IS NOT NULL
                    THEN 1
                    ELSE 0
                END
            ) AS LIQUIDADOS,
            SUM(
                CASE
                    WHEN t.DATA_APONTAMENTO IS NOT NULL
                     AND t.DATA_INTIMACAO IS NOT NULL
                     AND t.DATA_PROTESTO IS NOT NULL
                    THEN 1
                    ELSE 0
                END
            ) AS PROTESTADOS
        FROM P_TITULO t
        """
        row = self.fetch_one(sql, {}) or {}
        mapped = normalize_row_keys(row) or {}
        variacao_percentual_mes_anterior = self._fetch_variacao_percentual_mes_anterior()

        return {
            "total_titulos": self._to_int(mapped, "total_titulos"),
            "titulos_em_triduo": self._to_int(mapped, "titulos_em_triduo"),
            "liquidados": self._to_int(mapped, "liquidados"),
            "protestados": self._to_int(mapped, "protestados"),
            "variacao_percentual_mes_anterior": variacao_percentual_mes_anterior,
        }

    def _fetch_variacao_percentual_mes_anterior(self) -> float | None:
        sql = """
        SELECT
            SUM(
                CASE
                    WHEN EXTRACT(YEAR FROM t.DATA_APONTAMENTO) = EXTRACT(YEAR FROM CURRENT_DATE)
                     AND EXTRACT(MONTH FROM t.DATA_APONTAMENTO) = EXTRACT(MONTH FROM CURRENT_DATE)
                    THEN 1
                    ELSE 0
                END
            ) AS TOTAL_MES_ATUAL,
            SUM(
                CASE
                    WHEN EXTRACT(YEAR FROM t.DATA_APONTAMENTO) = EXTRACT(YEAR FROM DATEADD(-1 MONTH TO CURRENT_DATE))
                     AND EXTRACT(MONTH FROM t.DATA_APONTAMENTO) = EXTRACT(MONTH FROM DATEADD(-1 MONTH TO CURRENT_DATE))
                    THEN 1
                    ELSE 0
                END
            ) AS TOTAL_MES_ANTERIOR
        FROM P_TITULO t
        WHERE t.DATA_APONTAMENTO IS NOT NULL
        """
        row = self.fetch_one(sql, {}) or {}
        mapped = normalize_row_keys(row) or {}
        total_mes_atual = self._to_int(mapped, "total_mes_atual")
        total_mes_anterior = self._to_int(mapped, "total_mes_anterior")
        return self._calculate_variation_percent(total_mes_atual, total_mes_anterior)

    @staticmethod
    def _calculate_variation_percent(
        total_mes_atual: int, total_mes_anterior: int
    ) -> float | None:
        if total_mes_anterior <= 0:
            if total_mes_atual <= 0:
                return 0.0
            return None
        variation = ((total_mes_atual - total_mes_anterior) / total_mes_anterior) * 100
        return round(float(variation), 2)

    @staticmethod
    def _to_int(row: Mapping[str, Any], key: str) -> int:
        value = row.get(key)
        if value is None:
            return 0
        if isinstance(value, Decimal):
            return int(value)
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return int(value)
        try:
            return int(str(value))
        except (TypeError, ValueError):
            return 0
