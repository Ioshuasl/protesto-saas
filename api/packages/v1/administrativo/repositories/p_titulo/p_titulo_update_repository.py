from __future__ import annotations

from typing import Any

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_titulo import get_p_titulo_model
from packages.v1.administrativo.repositories.p_titulo.p_titulo_show_repository import (
    ShowRepository,
)
from packages.v1.administrativo.schemas.p_titulo_schema import (
    PTituloIdSchema,
    PTituloUpdateSchema,
    titulo_schema_to_orm_payload,
)


class UpdateRepository(BaseRepository):
    def execute(self, titulo_id: int, titulo_schema: PTituloUpdateSchema) -> dict[str, Any]:
        if use_orm_firebird():
            return self._execute_orm(titulo_id, titulo_schema)
        return self._execute_sql(titulo_id, titulo_schema)

    def _execute_orm(
        self, titulo_id: int, titulo_schema: PTituloUpdateSchema
    ) -> dict[str, Any]:
        payload = titulo_schema_to_orm_payload(
            titulo_schema.model_dump(exclude_none=True)
        )
        if not payload:
            row = ShowRepository().execute(PTituloIdSchema(titulo_id=titulo_id))
            return row or {}

        get_p_titulo_model().update(payload, {"where": {"TITULO_ID": titulo_id}})
        row = ShowRepository().execute(PTituloIdSchema(titulo_id=titulo_id))
        return row or {}

    def _execute_sql(
        self, titulo_id: int, titulo_schema: PTituloUpdateSchema
    ) -> dict[str, Any]:
        payload = titulo_schema_to_orm_payload(
            titulo_schema.model_dump(exclude_none=True)
        )
        if not payload:
            row = ShowRepository().execute(PTituloIdSchema(titulo_id=titulo_id))
            return row or {}

        set_parts = [f"{column} = :{column.lower()}" for column in payload]
        params = {column.lower(): payload[column] for column in payload}
        params["titulo_id"] = titulo_id

        try:
            sql = f"""
            UPDATE P_TITULO
            SET {", ".join(set_parts)}
            WHERE TITULO_ID = :titulo_id
            """
            self.run(sql, params)
            row = ShowRepository().execute(PTituloIdSchema(titulo_id=titulo_id))
            return row or {}
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar título: {exc}",
            ) from exc
