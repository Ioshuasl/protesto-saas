from __future__ import annotations

from typing import Any

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_pessoa_vinculo import get_p_pessoa_vinculo_model
from packages.v1.administrativo.model.p_titulo import get_p_titulo_model
from packages.v1.administrativo.schemas.p_pessoa_vinculo_schema import map_pessoa_vinculo_row
from packages.v1.administrativo.schemas.p_titulo_schema import PTituloIdSchema


class DevedoresRepository(BaseRepository):
    def execute(self, titulo_schema: PTituloIdSchema) -> list[dict[str, Any]]:
        if use_orm_firebird():
            return self._execute_orm(titulo_schema)
        return self._execute_sql(titulo_schema)

    def _execute_orm(self, titulo_schema: PTituloIdSchema) -> list[dict[str, Any]]:
        rows = get_p_pessoa_vinculo_model().findAll(
            {
                "where": {
                    "TITULO_ID": titulo_schema.titulo_id,
                    "TIPO_VINCULO": "DEVEDOR",
                },
                "order": [("PESSOA_VINCULO_ID", "ASC")],
            }
        )
        return [map_pessoa_vinculo_row(row) or {} for row in (rows or []) if row is not None]

    def _execute_sql(self, titulo_schema: PTituloIdSchema) -> list[dict[str, Any]]:
        sql = """
        SELECT pv.*
        FROM P_PESSOA_VINCULO pv
        WHERE pv.TITULO_ID = :titulo_id
          AND UPPER(TRIM(COALESCE(pv.TIPO_VINCULO, ''))) = 'DEVEDOR'
        ORDER BY pv.PESSOA_VINCULO_ID
        """
        rows = self.fetch_all(sql, {"titulo_id": titulo_schema.titulo_id})
        return [map_pessoa_vinculo_row(row) or {} for row in rows if row is not None]

    @staticmethod
    def titulo_exists(titulo_id: int) -> bool:
        return (
            get_p_titulo_model().findOne(
                {
                    "attributes": ["TITULO_ID"],
                    "where": {"TITULO_ID": titulo_id},
                }
            )
            is not None
        )
