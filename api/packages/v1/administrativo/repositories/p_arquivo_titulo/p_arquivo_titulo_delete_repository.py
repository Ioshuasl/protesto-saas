from __future__ import annotations

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_arquivo_titulo import get_p_arquivo_titulo_model
from packages.v1.administrativo.schemas.p_arquivo_titulo_schema import PArquivoTituloIdSchema


class DeleteRepository(BaseRepository):
    def execute(self, arquivo_schema: PArquivoTituloIdSchema) -> bool:
        if use_orm_firebird():
            return self._execute_orm(arquivo_schema)
        return self._execute_sql(arquivo_schema)

    def _execute_orm(self, arquivo_schema: PArquivoTituloIdSchema) -> bool:
        existing = get_p_arquivo_titulo_model().findByPk(arquivo_schema.arquivo_titulo_id)
        if existing is None:
            return False
        get_p_arquivo_titulo_model().destroy(
            {"where": {"ARQUIVO_TITULO_ID": arquivo_schema.arquivo_titulo_id}}
        )
        return True

    def _execute_sql(self, arquivo_schema: PArquivoTituloIdSchema) -> bool:
        sql = """
        DELETE FROM P_ARQUIVO_TITULO
        WHERE ARQUIVO_TITULO_ID = :arquivo_titulo_id
        """
        self.run(sql, {"arquivo_titulo_id": arquivo_schema.arquivo_titulo_id})
        return True
