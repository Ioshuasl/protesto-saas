from __future__ import annotations

from typing import Union

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.g_sistema import get_g_sistema_model
from packages.v1.administrativo.schemas.g_sistema_schema import GSistemaIdSchema


class DeleteRepository(BaseRepository):
    def execute(self, sistema_schema: GSistemaIdSchema):
        if use_orm_firebird():
            return self._execute_orm(sistema_schema)
        return self._execute_sql(sistema_schema)

    @staticmethod
    def _execute_orm(sistema_schema: GSistemaIdSchema) -> dict[str, Union[int, float]]:
        get_g_sistema_model().destroy({"where": {"SISTEMA_ID": sistema_schema.sistema_id}})
        return {"sistema_id": sistema_schema.sistema_id}

    def _execute_sql(self, sistema_schema: GSistemaIdSchema) -> dict[str, Union[int, float]]:
        try:
            sql = """
            DELETE FROM G_SISTEMA
            WHERE SISTEMA_ID = :sistema_id
            RETURNING SISTEMA_ID;
            """
            params = {"sistema_id": sistema_schema.sistema_id}
            response = self.run_and_return(sql, params)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Sistema não encontrado para exclusão.",
                )

            return {"sistema_id": sistema_schema.sistema_id}
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir sistema: {exc}",
            ) from exc
