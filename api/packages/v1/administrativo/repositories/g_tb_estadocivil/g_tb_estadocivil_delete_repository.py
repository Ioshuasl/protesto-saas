from __future__ import annotations

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.g_tb_estadocivil import get_g_tb_estadocivil_model
from packages.v1.administrativo.schemas.g_tb_estadocivil_schema import GTbEstadoCivilIdSchema


class DeleteRepository(BaseRepository):
    def execute(self, estadocivil_schema: GTbEstadoCivilIdSchema):
        if use_orm_firebird():
            return self._execute_orm(estadocivil_schema)
        return self._execute_sql(estadocivil_schema)

    @staticmethod
    def _execute_orm(estadocivil_schema: GTbEstadoCivilIdSchema) -> dict[str, int]:
        get_g_tb_estadocivil_model().destroy(
            {"where": {"TB_ESTADOCIVIL_ID": estadocivil_schema.tb_estadocivil_id}}
        )
        return {"tb_estadocivil_id": estadocivil_schema.tb_estadocivil_id}

    def _execute_sql(self, estadocivil_schema: GTbEstadoCivilIdSchema):
        try:
            sql = """
            DELETE FROM G_TB_ESTADOCIVIL
            WHERE TB_ESTADOCIVIL_ID = :tb_estadocivil_id
            RETURNING TB_ESTADOCIVIL_ID;
            """
            params = {"tb_estadocivil_id": estadocivil_schema.tb_estadocivil_id}
            return self.run_and_return(sql, params)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir G_TB_ESTADOCIVIL: {exc}",
            ) from exc
