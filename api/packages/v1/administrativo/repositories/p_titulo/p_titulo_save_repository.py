from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_titulo import get_p_titulo_model
from packages.v1.administrativo.repositories.p_titulo.p_titulo_show_repository import (
    ShowRepository,
)
from packages.v1.administrativo.schemas.p_titulo_schema import (
    PTituloIdSchema,
    PTituloSaveSchema,
    titulo_schema_to_orm_payload,
)


class SaveRepository(BaseRepository):
    def execute(self, titulo_schema: PTituloSaveSchema) -> dict[str, Any]:
        if use_orm_firebird():
            return self._execute_orm(titulo_schema)
        return self._execute_sql(titulo_schema)

    def _execute_orm(self, titulo_schema: PTituloSaveSchema) -> dict[str, Any]:
        payload = titulo_schema_to_orm_payload(
            titulo_schema.model_dump(exclude_none=True)
        )
        payload["TITULO_ID"] = titulo_schema.titulo_id
        if "DATA_CADASTRO" not in payload:
            payload["DATA_CADASTRO"] = datetime.now()

        get_p_titulo_model().create(payload)
        saved = ShowRepository().execute(
            PTituloIdSchema(titulo_id=titulo_schema.titulo_id)
        )
        return saved or {}

    def _execute_sql(self, titulo_schema: PTituloSaveSchema) -> dict[str, Any]:
        payload = titulo_schema_to_orm_payload(
            titulo_schema.model_dump(exclude_none=True)
        )
        payload["TITULO_ID"] = titulo_schema.titulo_id
        if "DATA_CADASTRO" not in payload:
            payload["DATA_CADASTRO"] = datetime.now()

        columns = list(payload.keys())
        placeholders = ", ".join(f":{col.lower()}" for col in columns)
        col_sql = ", ".join(columns)
        params = {col.lower(): payload[col] for col in columns}

        try:
            sql = f"""
            INSERT INTO P_TITULO ({col_sql})
            VALUES ({placeholders})
            RETURNING TITULO_ID;
            """
            self.run_and_return(sql, params)
            saved = ShowRepository().execute(
                PTituloIdSchema(titulo_id=titulo_schema.titulo_id)
            )
            return saved or {}
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar título: {exc}",
            ) from exc
