from __future__ import annotations

from decimal import Decimal

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_livro_andamento import get_p_livro_andamento_model
from packages.v1.administrativo.schemas.p_livro_natureza_schema import PLivroNaturezaIdSchema


class CountByLivroNaturezaRepository(BaseRepository):
    def execute(self, livro_natureza_schema: PLivroNaturezaIdSchema) -> int:
        if use_orm_firebird():
            return self._execute_orm(livro_natureza_schema)
        return self._execute_sql(livro_natureza_schema)

    def _execute_orm(self, livro_natureza_schema: PLivroNaturezaIdSchema) -> int:
        total = get_p_livro_andamento_model().count(
            {
                "where": {
                    "LIVRO_NATUREZA_ID": livro_natureza_schema.livro_natureza_id
                }
            }
        )
        if isinstance(total, Decimal):
            return int(total)
        return int(total or 0)

    def _execute_sql(self, livro_natureza_schema: PLivroNaturezaIdSchema) -> int:
        sql = """
        SELECT COUNT(*) AS TOTAL
        FROM P_LIVRO_ANDAMENTO
        WHERE LIVRO_NATUREZA_ID = :livro_natureza_id
        """
        row = self.fetch_one(
            sql, {"livro_natureza_id": livro_natureza_schema.livro_natureza_id}
        )
        if row is None:
            return 0
        total = row.get("TOTAL") or row.get("total")
        if isinstance(total, Decimal):
            return int(total)
        return int(total or 0)
