from __future__ import annotations

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_ocorrencias import get_p_ocorrencias_model
from packages.v1.administrativo.schemas.p_ocorrencias_schema import POcorrenciasIdSchema


class DeleteRepository(BaseRepository):
    def execute(self, ocorrencias_schema: POcorrenciasIdSchema):
        if use_orm_firebird():
            return self._execute_orm(ocorrencias_schema)
        return self._execute_sql(ocorrencias_schema)

    @staticmethod
    def _execute_orm(ocorrencias_schema: POcorrenciasIdSchema) -> dict[str, int]:
        get_p_ocorrencias_model().destroy(
            {"where": {"OCORRENCIAS_ID": ocorrencias_schema.ocorrencias_id}}
        )
        return {"ocorrencias_id": ocorrencias_schema.ocorrencias_id}

    def _execute_sql(self, ocorrencias_schema: POcorrenciasIdSchema) -> dict[str, int]:
        try:
            sql = """
            DELETE FROM P_OCORRENCIAS
            WHERE OCORRENCIAS_ID = :ocorrencias_id
            RETURNING OCORRENCIAS_ID;
            """
            params = {"ocorrencias_id": ocorrencias_schema.ocorrencias_id}
            response = self.run_and_return(sql, params)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Ocorrência não encontrada para exclusão.",
                )

            return {"ocorrencias_id": ocorrencias_schema.ocorrencias_id}
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir ocorrência: {exc}",
            ) from exc
