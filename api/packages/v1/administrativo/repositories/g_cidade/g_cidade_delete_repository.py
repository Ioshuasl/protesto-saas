from __future__ import annotations

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.g_cidade import get_g_cidade_model
from packages.v1.administrativo.schemas.g_cidade_schema import GCidadeIdSchema


class DeleteRepository(BaseRepository):
    def execute(self, g_cidade_schema: GCidadeIdSchema):
        if use_orm_firebird():
            return self._execute_orm(g_cidade_schema)
        return self._execute_sql(g_cidade_schema)

    @staticmethod
    def _execute_orm(g_cidade_schema: GCidadeIdSchema) -> dict[str, int]:
        get_g_cidade_model().destroy({"where": {"CIDADE_ID": g_cidade_schema.cidade_id}})
        return {"cidade_id": g_cidade_schema.cidade_id}

    def _execute_sql(self, g_cidade_schema: GCidadeIdSchema):
        try:
            sql = """
            DELETE FROM G_CIDADE
            WHERE CIDADE_ID = :cidade_id
            RETURNING CIDADE_ID;
            """
            params = {"cidade_id": g_cidade_schema.cidade_id}
            return self.run_and_return(sql, params)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir G_CIDADE: {exc}",
            ) from exc
