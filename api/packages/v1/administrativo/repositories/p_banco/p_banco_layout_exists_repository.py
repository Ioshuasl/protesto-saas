from __future__ import annotations

from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.p_banco_schema import PBancoLayoutIdSchema


class LayoutExistsRepository(BaseRepository):
    def execute(self, layout_schema: PBancoLayoutIdSchema) -> bool:
        sql = """
        SELECT 1
        FROM P_LAYOUT
        WHERE LAYOUT_ID = :layout_id
        """
        row = self.fetch_one(sql, {"layout_id": layout_schema.layout_id})
        return row is not None
