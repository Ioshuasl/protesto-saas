from __future__ import annotations

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_motivos_cancelamento import (
    get_p_motivos_cancelamento_model,
)
from packages.v1.administrativo.schemas.p_motivos_cancelamento_schema import (
    PMotivosCancelamentoIdSchema,
)


class DeleteRepository(BaseRepository):
    def execute(self, motivos_cancelamento_schema: PMotivosCancelamentoIdSchema):
        if use_orm_firebird():
            return self._execute_orm(motivos_cancelamento_schema)
        return self._execute_sql(motivos_cancelamento_schema)

    @staticmethod
    def _execute_orm(
        motivos_cancelamento_schema: PMotivosCancelamentoIdSchema,
    ) -> dict[str, int]:
        get_p_motivos_cancelamento_model().destroy(
            {
                "where": {
                    "MOTIVOS_CANCELAMENTO_ID": motivos_cancelamento_schema.motivos_cancelamento_id
                }
            }
        )
        return {
            "motivos_cancelamento_id": motivos_cancelamento_schema.motivos_cancelamento_id
        }

    def _execute_sql(
        self, motivos_cancelamento_schema: PMotivosCancelamentoIdSchema
    ) -> dict[str, int]:
        try:
            sql = """
            DELETE FROM P_MOTIVOS_CANCELAMENTO
            WHERE MOTIVOS_CANCELAMENTO_ID = :motivos_cancelamento_id
            RETURNING MOTIVOS_CANCELAMENTO_ID;
            """
            params = {
                "motivos_cancelamento_id": motivos_cancelamento_schema.motivos_cancelamento_id
            }
            response = self.run_and_return(sql, params)

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Motivo de cancelamento não encontrado para exclusão.",
                )

            return {
                "motivos_cancelamento_id": motivos_cancelamento_schema.motivos_cancelamento_id
            }
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir motivo de cancelamento: {exc}",
            ) from exc
