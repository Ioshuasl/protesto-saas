from __future__ import annotations

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_andamento import get_p_andamento_model
from packages.v1.administrativo.schemas.p_andamento_schema import PAndamentoIdSchema


class DeleteRepository(BaseRepository):
    def execute(self, andamento_schema: PAndamentoIdSchema):
        if use_orm_firebird():
            return self._execute_orm(andamento_schema)
        return self._execute_sql(andamento_schema)

    @staticmethod
    def _execute_orm(andamento_schema: PAndamentoIdSchema) -> dict[str, int]:
        get_p_andamento_model().destroy(
            {"where": {"ANDAMENTO_ID": andamento_schema.andamento_id}}
        )
        return {"andamento_id": andamento_schema.andamento_id}

    def _execute_sql(self, andamento_schema: PAndamentoIdSchema) -> dict[str, int]:
        try:
            sql = """
            DELETE FROM P_ANDAMENTO
            WHERE ANDAMENTO_ID = :andamento_id
            RETURNING ANDAMENTO_ID;
            """
            params = {"andamento_id": andamento_schema.andamento_id}
            response = self.run_and_return(sql, params)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Andamento não encontrado para exclusão.",
                )

            return {"andamento_id": andamento_schema.andamento_id}
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir andamento: {exc}",
            ) from exc
