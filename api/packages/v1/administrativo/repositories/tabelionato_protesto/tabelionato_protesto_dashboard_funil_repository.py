from __future__ import annotations

from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Any, Mapping

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys


class TabelionatoProtestoDashboardFunilRepository(BaseRepository):
    def execute(self) -> list[dict[str, Any]]:
        sql = """
        SELECT
            CAST(t.DATA_APONTAMENTO AS DATE) AS DIA,
            COUNT(*) AS APONTADOS,
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
        WHERE t.DATA_APONTAMENTO IS NOT NULL
          AND CAST(t.DATA_APONTAMENTO AS DATE) >= DATEADD(-6 DAY TO CURRENT_DATE)
          AND CAST(t.DATA_APONTAMENTO AS DATE) <= CURRENT_DATE
        GROUP BY CAST(t.DATA_APONTAMENTO AS DATE)
        ORDER BY CAST(t.DATA_APONTAMENTO AS DATE) ASC
        """
        rows = self.fetch_all(sql, {})
        rows_by_day = self._build_rows_by_day(rows)
        return self._build_week_series(rows_by_day)

    def _build_rows_by_day(self, rows: list[Mapping[str, Any]]) -> dict[str, dict[str, int]]:
        by_day: dict[str, dict[str, int]] = {}
        for row in rows:
            mapped = normalize_row_keys(row) or {}
            day_key = self._to_date_key(mapped.get("dia"))
            if not day_key:
                continue
            by_day[day_key] = {
                "apontados": self._to_int(mapped.get("apontados")),
                "liquidados": self._to_int(mapped.get("liquidados")),
                "protestados": self._to_int(mapped.get("protestados")),
            }
        return by_day

    def _build_week_series(
        self, rows_by_day: dict[str, dict[str, int]]
    ) -> list[dict[str, int | str]]:
        today = date.today()
        start_day = today - timedelta(days=6)
        series: list[dict[str, int | str]] = []

        for offset in range(7):
            current_day = start_day + timedelta(days=offset)
            label = current_day.isoformat()
            values = rows_by_day.get(
                label,
                {
                    "apontados": 0,
                    "liquidados": 0,
                    "protestados": 0,
                },
            )
            series.append(
                {
                    "label": label,
                    "apontados": int(values["apontados"]),
                    "liquidados": int(values["liquidados"]),
                    "protestados": int(values["protestados"]),
                }
            )

        return series

    @staticmethod
    def _to_date_key(value: Any) -> str | None:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.date().isoformat()
        if isinstance(value, date):
            return value.isoformat()
        text = str(value).strip()
        if not text:
            return None
        return text[:10]

    @staticmethod
    def _to_int(value: Any) -> int:
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
