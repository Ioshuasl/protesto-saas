from __future__ import annotations

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_layout import get_p_layout_model
from packages.v1.administrativo.schemas.p_banco_schema import PBancoLayoutIdSchema


class ExistsRepository(BaseRepository):
    def execute(self, layout_schema: PBancoLayoutIdSchema) -> bool:
        if use_orm_firebird():
            return self._execute_orm(layout_schema)
        return self._execute_sql(layout_schema)

    def _execute_orm(self, layout_schema: PBancoLayoutIdSchema) -> bool:
        row = get_p_layout_model().findByPk(layout_schema.layout_id)
        return row is not None

    def _execute_sql(self, layout_schema: PBancoLayoutIdSchema) -> bool:
        sql = """
        SELECT 1
        FROM P_LAYOUT
        WHERE LAYOUT_ID = :layout_id
        """
        row = self.fetch_one(sql, {"layout_id": layout_schema.layout_id})
        return row is not None
