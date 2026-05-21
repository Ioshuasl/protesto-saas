from __future__ import annotations

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_livro_natureza import get_p_livro_natureza_model
from packages.v1.administrativo.schemas.p_livro_natureza_schema import PLivroNaturezaIdSchema


class DeleteRepository(BaseRepository):
    def execute(self, livro_natureza_schema: PLivroNaturezaIdSchema) -> bool:
        if use_orm_firebird():
            return self._execute_orm(livro_natureza_schema)
        return self._execute_sql(livro_natureza_schema)

    def _execute_orm(self, livro_natureza_schema: PLivroNaturezaIdSchema) -> bool:
        existing = get_p_livro_natureza_model().findByPk(
            livro_natureza_schema.livro_natureza_id
        )
        if not existing:
            return False
        get_p_livro_natureza_model().destroy(
            {"where": {"LIVRO_NATUREZA_ID": livro_natureza_schema.livro_natureza_id}}
        )
        return True

    def _execute_sql(self, livro_natureza_schema: PLivroNaturezaIdSchema) -> bool:
        try:
            sql = """
            DELETE FROM P_LIVRO_NATUREZA
            WHERE LIVRO_NATUREZA_ID = :livro_natureza_id
            """
            self.run(
                sql, {"livro_natureza_id": livro_natureza_schema.livro_natureza_id}
            )
            return True
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir natureza de livro: {exc}",
            ) from exc
