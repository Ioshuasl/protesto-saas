from __future__ import annotations

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_especie import get_p_especie_model
from packages.v1.administrativo.schemas.p_especie_schema import PEspecieIdSchema


class DeleteRepository(BaseRepository):
    def execute(self, especie_schema: PEspecieIdSchema) -> bool:
        if use_orm_firebird():
            return self._execute_orm(especie_schema)
        return self._execute_sql(especie_schema)

    def _execute_orm(self, especie_schema: PEspecieIdSchema) -> bool:
        existing = get_p_especie_model().findByPk(especie_schema.especie_id)
        if not existing:
            return False
        get_p_especie_model().destroy({"where": {"ESPECIE_ID": especie_schema.especie_id}})
        return True

    def _execute_sql(self, especie_schema: PEspecieIdSchema) -> bool:
        try:
            sql = """
            DELETE FROM P_ESPECIE
            WHERE ESPECIE_ID = :especie_id
            """
            self.run(sql, {"especie_id": especie_schema.especie_id})
            return True
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir espécie: {exc}",
            ) from exc
