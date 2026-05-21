from __future__ import annotations

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_banco import get_p_banco_model
from packages.v1.administrativo.schemas.p_banco_schema import PBancoIdSchema


class DeleteRepository(BaseRepository):
    def execute(self, banco_schema: PBancoIdSchema) -> bool:
        if use_orm_firebird():
            return self._execute_orm(banco_schema)
        return self._execute_sql(banco_schema)

    def _execute_orm(self, banco_schema: PBancoIdSchema) -> bool:
        existing = get_p_banco_model().findByPk(banco_schema.banco_id)
        if not existing:
            return False
        get_p_banco_model().destroy({"where": {"BANCO_ID": banco_schema.banco_id}})
        return True

    def _execute_sql(self, banco_schema: PBancoIdSchema) -> bool:
        try:
            sql = """
            DELETE FROM P_BANCO
            WHERE BANCO_ID = :banco_id
            """
            self.run(sql, {"banco_id": banco_schema.banco_id})
            return True
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir banco: {exc}",
            ) from exc
