from __future__ import annotations

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_titulo import get_p_titulo_model
from packages.v1.administrativo.schemas.p_titulo_schema import PTituloIdSchema


class DeleteRepository(BaseRepository):
    def execute(self, titulo_schema: PTituloIdSchema) -> dict[str, int]:
        if use_orm_firebird():
            return self._execute_orm(titulo_schema)
        return self._execute_sql(titulo_schema)

    @staticmethod
    def _execute_orm(titulo_schema: PTituloIdSchema) -> dict[str, int]:
        destroyed = get_p_titulo_model().destroy(
            {"where": {"TITULO_ID": titulo_schema.titulo_id}}
        )
        if not destroyed:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Título não encontrado para exclusão.",
            )
        return {"titulo_id": titulo_schema.titulo_id}

    def _execute_sql(self, titulo_schema: PTituloIdSchema) -> dict[str, int]:
        try:
            sql = """
            DELETE FROM P_TITULO
            WHERE TITULO_ID = :titulo_id
            RETURNING TITULO_ID;
            """
            response = self.run_and_return(sql, {"titulo_id": titulo_schema.titulo_id})
            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Título não encontrado para exclusão.",
                )
            return {"titulo_id": titulo_schema.titulo_id}
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir título: {exc}",
            ) from exc
