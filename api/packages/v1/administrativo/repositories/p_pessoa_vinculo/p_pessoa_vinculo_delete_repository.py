from __future__ import annotations

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_pessoa_vinculo import get_p_pessoa_vinculo_model
from packages.v1.administrativo.schemas.p_pessoa_vinculo_schema import PPessoaVinculoIdSchema


class DeleteRepository(BaseRepository):
    def execute(self, vinculo_schema: PPessoaVinculoIdSchema) -> bool:
        if use_orm_firebird():
            return self._execute_orm(vinculo_schema)
        return self._execute_sql(vinculo_schema)

    def _execute_orm(self, vinculo_schema: PPessoaVinculoIdSchema) -> bool:
        existing = get_p_pessoa_vinculo_model().findByPk(vinculo_schema.pessoa_vinculo_id)
        if not existing:
            return False
        get_p_pessoa_vinculo_model().destroy(
            {"where": {"PESSOA_VINCULO_ID": vinculo_schema.pessoa_vinculo_id}}
        )
        return True

    def _execute_sql(self, vinculo_schema: PPessoaVinculoIdSchema) -> bool:
        try:
            sql = """
            DELETE FROM P_PESSOA_VINCULO
            WHERE PESSOA_VINCULO_ID = :pessoa_vinculo_id
            """
            self.run(sql, {"pessoa_vinculo_id": vinculo_schema.pessoa_vinculo_id})
            return True
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir vínculo de pessoa: {exc}",
            ) from exc
