from __future__ import annotations

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.g_feriado import get_g_feriado_model
from packages.v1.administrativo.schemas.g_feriado_schema import GFeriadoIdSchema


class DeleteRepository(BaseRepository):
    def execute(self, feriado_schema: GFeriadoIdSchema):
        if use_orm_firebird():
            return self._execute_orm(feriado_schema)
        return self._execute_sql(feriado_schema)

    @staticmethod
    def _execute_orm(feriado_schema: GFeriadoIdSchema) -> dict[str, int]:
        get_g_feriado_model().destroy({"where": {"FERIADO_ID": feriado_schema.feriado_id}})
        return {"feriado_id": feriado_schema.feriado_id}

    def _execute_sql(self, feriado_schema: GFeriadoIdSchema) -> dict[str, int]:
        try:
            sql = """
            DELETE FROM G_FERIADO
            WHERE FERIADO_ID = :feriado_id
            RETURNING FERIADO_ID;
            """
            params = {"feriado_id": feriado_schema.feriado_id}
            response = self.run_and_return(sql, params)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Feriado não encontrado para exclusão.",
                )

            return {"feriado_id": feriado_schema.feriado_id}
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir feriado: {exc}",
            ) from exc
