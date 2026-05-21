from __future__ import annotations

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_livro_andamento import get_p_livro_andamento_model
from packages.v1.administrativo.schemas.p_livro_andamento_schema import PLivroAndamentoIdSchema


class DeleteRepository(BaseRepository):
    def execute(self, livro_andamento_schema: PLivroAndamentoIdSchema) -> bool:
        if use_orm_firebird():
            return self._execute_orm(livro_andamento_schema)
        return self._execute_sql(livro_andamento_schema)

    def _execute_orm(self, livro_andamento_schema: PLivroAndamentoIdSchema) -> bool:
        existing = get_p_livro_andamento_model().findByPk(
            livro_andamento_schema.livro_andamento_id
        )
        if not existing:
            return False
        get_p_livro_andamento_model().destroy(
            {"where": {"LIVRO_ANDAMENTO_ID": livro_andamento_schema.livro_andamento_id}}
        )
        return True

    def _execute_sql(self, livro_andamento_schema: PLivroAndamentoIdSchema) -> bool:
        try:
            sql = """
            DELETE FROM P_LIVRO_ANDAMENTO
            WHERE LIVRO_ANDAMENTO_ID = :livro_andamento_id
            """
            self.run(
                sql, {"livro_andamento_id": livro_andamento_schema.livro_andamento_id}
            )
            return True
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir livro de andamento: {exc}",
            ) from exc
