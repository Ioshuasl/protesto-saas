from __future__ import annotations

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.g_tb_profissao import get_g_tb_profissao_model
from packages.v1.administrativo.schemas.g_tb_profissao_schema import GTbProfissaoIdSchema


class DeleteRepository(BaseRepository):
    def execute(self, profissao_schema: GTbProfissaoIdSchema):
        if use_orm_firebird():
            return self._execute_orm(profissao_schema)
        return self._execute_sql(profissao_schema)

    @staticmethod
    def _execute_orm(profissao_schema: GTbProfissaoIdSchema) -> dict[str, int]:
        get_g_tb_profissao_model().destroy(
            {"where": {"TB_PROFISSAO_ID": profissao_schema.tb_profissao_id}}
        )
        return {"tb_profissao_id": profissao_schema.tb_profissao_id}

    def _execute_sql(self, profissao_schema: GTbProfissaoIdSchema):
        try:
            sql = """
            DELETE FROM G_TB_PROFISSAO
            WHERE TB_PROFISSAO_ID = :tb_profissao_id
            RETURNING TB_PROFISSAO_ID;
            """
            params = {"tb_profissao_id": profissao_schema.tb_profissao_id}
            return self.run_and_return(sql, params)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir G_TB_PROFISSAO: {exc}",
            ) from exc
