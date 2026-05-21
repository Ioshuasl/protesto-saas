from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_pessoa import (
    P_PESSOA_ATTRIBUTES,
    get_p_pessoa_model,
)

_NUMERIC_ID_KEYS = frozenset(
    {
        "pessoa_id",
        "estado_civil_id",
        "profissao_id",
        "cidade_id",
        "chave_pessoa_imp",
    }
)


class ShowRepository(BaseRepository):
    def execute(self, pessoa_id: int) -> Optional[dict[str, Any]]:
        if use_orm_firebird():
            return self._execute_orm(pessoa_id)
        return self._execute_sql(pessoa_id)

    def _execute_orm(self, pessoa_id: int) -> Optional[dict[str, Any]]:
        row = get_p_pessoa_model().findByPk(pessoa_id)
        return self._map_pessoa_row(row)

    def _execute_sql(self, pessoa_id: int) -> Optional[dict[str, Any]]:
        columns = ", ".join(P_PESSOA_ATTRIBUTES.keys())
        sql = f"""
        SELECT {columns}
        FROM P_PESSOA
        WHERE PESSOA_ID = :pessoa_id
        """
        row = self.fetch_one(sql, {"pessoa_id": pessoa_id})
        return self._map_pessoa_row(row)

    @staticmethod
    def _map_pessoa_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        for key in _NUMERIC_ID_KEYS:
            value = mapped.get(key)
            if isinstance(value, Decimal):
                mapped[key] = int(value)

        for key, value in list(mapped.items()):
            if value is not None and isinstance(value, str):
                mapped[key] = value.strip() or None

        return mapped
