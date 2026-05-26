from __future__ import annotations

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_certidao import get_p_certidao_model
from packages.v1.administrativo.schemas.p_certidao_schema import PCertidaoIdSchema


class DeleteRepository(BaseRepository):
    def execute(self, certidao_schema: PCertidaoIdSchema) -> dict[str, int]:
        if use_orm_firebird():
            return self._execute_orm(certidao_schema)
        return self._execute_sql(certidao_schema)

    @staticmethod
    def _execute_orm(certidao_schema: PCertidaoIdSchema) -> dict[str, int]:
        get_p_certidao_model().destroy(
            {"where": {"CERTIDAO_ID": certidao_schema.certidao_id}}
        )
        return {"certidao_id": certidao_schema.certidao_id}

    def _execute_sql(self, certidao_schema: PCertidaoIdSchema) -> dict[str, int]:
        try:
            sql = """
            DELETE FROM P_CERTIDAO
            WHERE CERTIDAO_ID = :certidao_id
            RETURNING CERTIDAO_ID;
            """
            response = self.run_and_return(sql, {"certidao_id": certidao_schema.certidao_id})

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Certidão não encontrada para exclusão.",
                )

            return {"certidao_id": certidao_schema.certidao_id}
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir certidão: {exc}",
            ) from exc
