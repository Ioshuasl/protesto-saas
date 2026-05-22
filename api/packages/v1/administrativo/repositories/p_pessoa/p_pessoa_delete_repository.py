from __future__ import annotations

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_pessoa import get_p_pessoa_model
from packages.v1.administrativo.schemas.p_pessoa_schema import PPessoaIdSchema


class DeleteRepository(BaseRepository):
    def execute(self, pessoa_schema: PPessoaIdSchema) -> dict[str, int]:
        if use_orm_firebird():
            return self._execute_orm(pessoa_schema)
        return self._execute_sql(pessoa_schema)

    @staticmethod
    def _execute_orm(pessoa_schema: PPessoaIdSchema) -> dict[str, int]:
        get_p_pessoa_model().destroy({"where": {"PESSOA_ID": pessoa_schema.pessoa_id}})
        return {"pessoa_id": pessoa_schema.pessoa_id}

    def _execute_sql(self, pessoa_schema: PPessoaIdSchema) -> dict[str, int]:
        try:
            sql = """
            DELETE FROM P_PESSOA
            WHERE PESSOA_ID = :pessoa_id
            RETURNING PESSOA_ID;
            """
            response = self.run_and_return(sql, {"pessoa_id": pessoa_schema.pessoa_id})

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Pessoa não encontrada para exclusão.",
                )

            return {"pessoa_id": pessoa_schema.pessoa_id}
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir pessoa: {exc}",
            ) from exc
