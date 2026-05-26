from __future__ import annotations

from typing import Any

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_template import get_p_template_model
from packages.v1.administrativo.repositories.p_template.p_template_index_repository import (
    _SELECT_ATTRIBUTES,
    _SELECT_COLUMNS,
    IndexRepository,
)
from packages.v1.administrativo.schemas.p_template_schema import PTemplateIdSchema


class ShowRepository(BaseRepository):
    def execute(self, template_schema: PTemplateIdSchema) -> dict[str, Any]:
        if use_orm_firebird():
            return self._execute_orm(template_schema)
        return self._execute_sql(template_schema)

    def _execute_orm(self, template_schema: PTemplateIdSchema) -> dict[str, Any]:
        row = get_p_template_model().findOne(
            {
                "attributes": _SELECT_ATTRIBUTES,
                "where": {"TEMPLATE_ID": template_schema.template_id},
            }
        )
        result = IndexRepository._map_row(row)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template não encontrado.",
            )
        return result

    def _execute_sql(self, template_schema: PTemplateIdSchema) -> dict[str, Any]:
        try:
            sql = f"""
            SELECT
                {_SELECT_COLUMNS.strip()}
            FROM P_TEMPLATE
            WHERE TEMPLATE_ID = :template_id
            """
            result = self.fetch_one(sql, {"template_id": template_schema.template_id})

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Template não encontrado.",
                )

            return IndexRepository._map_row(result) or {}
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar template: {exc}",
            ) from exc
