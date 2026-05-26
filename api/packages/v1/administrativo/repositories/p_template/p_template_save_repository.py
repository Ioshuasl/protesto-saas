from __future__ import annotations

from typing import Any

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_template import get_p_template_model
from packages.v1.administrativo.repositories.p_template.p_template_index_repository import (
    _SELECT_COLUMNS,
    IndexRepository,
)
from packages.v1.administrativo.schemas.p_template_schema import PTemplateSaveSchema

_FIELD_TO_COLUMN = {
    "template_id": "TEMPLATE_ID",
    "descricao": "DESCRICAO",
}


class SaveRepository(BaseRepository):
    def execute(self, template_schema: PTemplateSaveSchema) -> dict[str, Any]:
        if use_orm_firebird():
            return self._execute_orm(template_schema)
        return self._execute_sql(template_schema)

    def _execute_orm(self, template_schema: PTemplateSaveSchema) -> dict[str, Any]:
        payload = self._build_payload(template_schema)
        created = get_p_template_model().create(payload)
        return IndexRepository._map_row(created) or {}

    def _execute_sql(self, template_schema: PTemplateSaveSchema) -> dict[str, Any]:
        try:
            payload = self._build_payload(template_schema)
            columns = list(payload.keys())
            values = [f":{column.lower()}" for column in columns]
            params = {column.lower(): value for column, value in payload.items()}

            sql = f"""
            INSERT INTO P_TEMPLATE (
                {', '.join(columns)}
            ) VALUES (
                {', '.join(values)}
            )
            RETURNING
                {_SELECT_COLUMNS.strip()};
            """
            result = self.run_and_return(sql, params)
            return IndexRepository._map_row(result) or {}
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar template: {exc}",
            ) from exc

    @staticmethod
    def _build_payload(template_schema: PTemplateSaveSchema) -> dict[str, Any]:
        data = template_schema.model_dump(exclude_none=True)
        return {
            column: data[field]
            for field, column in _FIELD_TO_COLUMN.items()
            if field in data
        }
