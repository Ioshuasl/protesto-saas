from __future__ import annotations

from decimal import Decimal

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_titulo import get_p_titulo_model
from packages.v1.administrativo.schemas.p_arquivo_titulo_schema import PArquivoTituloIdSchema


class CountTituloRepository(BaseRepository):
    def execute(self, arquivo_schema: PArquivoTituloIdSchema) -> int:
        if use_orm_firebird():
            return self._execute_orm(arquivo_schema)
        return self._execute_sql(arquivo_schema)

    def _execute_orm(self, arquivo_schema: PArquivoTituloIdSchema) -> int:
        total = get_p_titulo_model().count(
            {"where": {"ARQUIVO_TITULO_ID": arquivo_schema.arquivo_titulo_id}}
        )
        if isinstance(total, Decimal):
            return int(total)
        return int(total or 0)

    def _execute_sql(self, arquivo_schema: PArquivoTituloIdSchema) -> int:
        sql = """
        SELECT COUNT(*) AS TOTAL
        FROM P_TITULO
        WHERE ARQUIVO_TITULO_ID = :arquivo_titulo_id
        """
        row = self.fetch_one(
            sql, {"arquivo_titulo_id": arquivo_schema.arquivo_titulo_id}
        )
        if row is None:
            return 0
        total = row.get("TOTAL") or row.get("total")
        if isinstance(total, Decimal):
            return int(total)
        return int(total or 0)
