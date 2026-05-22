from __future__ import annotations

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_motivos import get_p_motivos_model
from packages.v1.administrativo.schemas.p_motivos_schema import PMotivosIdSchema


class DeleteRepository(BaseRepository):
    def execute(self, motivos_schema: PMotivosIdSchema):
        if use_orm_firebird():
            return self._execute_orm(motivos_schema)
        return self._execute_sql(motivos_schema)

    @staticmethod
    def _execute_orm(motivos_schema: PMotivosIdSchema) -> dict[str, int]:
        get_p_motivos_model().destroy({"where": {"MOTIVOS_ID": motivos_schema.motivos_id}})
        return {"motivos_id": motivos_schema.motivos_id}

    def _execute_sql(self, motivos_schema: PMotivosIdSchema) -> dict[str, int]:
        try:
            sql = """
            DELETE FROM P_MOTIVOS
            WHERE MOTIVOS_ID = :motivos_id
            RETURNING MOTIVOS_ID;
            """
            params = {"motivos_id": motivos_schema.motivos_id}
            response = self.run_and_return(sql, params)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Motivo não encontrado para exclusão.",
                )

            return {"motivos_id": motivos_schema.motivos_id}
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir motivo: {exc}",
            ) from exc
