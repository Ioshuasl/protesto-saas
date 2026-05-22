from __future__ import annotations

from typing import Any, Optional

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_pessoa import (
    P_PESSOA_ATTRIBUTES,
    get_p_pessoa_model,
)
from packages.v1.administrativo.schemas.p_pessoa_schema import map_pessoa_row


class ShowRepository(BaseRepository):
    def execute(self, pessoa_id: int) -> Optional[dict[str, Any]]:
        if use_orm_firebird():
            return self._execute_orm(pessoa_id)
        return self._execute_sql(pessoa_id)

    def _execute_orm(self, pessoa_id: int) -> Optional[dict[str, Any]]:
        row = get_p_pessoa_model().findByPk(pessoa_id)
        return map_pessoa_row(row)

    def _execute_sql(self, pessoa_id: int) -> Optional[dict[str, Any]]:
        columns = ", ".join(P_PESSOA_ATTRIBUTES.keys())
        sql = f"""
        SELECT {columns}
        FROM P_PESSOA
        WHERE PESSOA_ID = :pessoa_id
        """
        row = self.fetch_one(sql, {"pessoa_id": pessoa_id})
        return map_pessoa_row(row)
