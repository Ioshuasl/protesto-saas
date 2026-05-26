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
from packages.v1.administrativo.repositories.p_template.p_template_save_repository import (
    _FIELD_TO_COLUMN,
)
from packages.v1.administrativo.schemas.p_template_schema import PTemplateUpdateSchema


class UpdateRepository(BaseRepository):
    def execute(
        self,
        template_id: int,
        template_schema: PTemplateUpdateSchema,
    ) -> dict[str, Any]:
        if use_orm_firebird():
            return self._execute_orm(template_id, template_schema)
        return self._execute_sql(template_id, template_schema)

    def _execute_orm(
        self,
        template_id: int,
        template_schema: PTemplateUpdateSchema,
    ) -> dict[str, Any]:
        values = self._build_payload(template_schema)
        if not values:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Nenhum campo informado para atualização.",
            )

        model = get_p_template_model()
        result = model.update(values, {"where": {"TEMPLATE_ID": template_id}})
        rows = result.get("rows") if isinstance(result, dict) else None
        if rows:
            return IndexRepository._map_row(rows[0]) or {}

        row = model.findOne(
            {
                "attributes": ["TEMPLATE_ID", "DESCRICAO"],
                "where": {"TEMPLATE_ID": template_id},
            }
        )
        mapped = IndexRepository._map_row(row)
        if not mapped:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template não encontrado para atualização.",
            )
        return mapped

    def _execute_sql(
        self,
        template_id: int,
        template_schema: PTemplateUpdateSchema,
    ) -> dict[str, Any]:
        try:
            payload = self._build_payload(template_schema)
            if not payload:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Nenhum campo informado para atualização.",
                )

            updates = [f"{column} = :{column.lower()}" for column in payload]
            params = {column.lower(): value for column, value in payload.items()}
            params["template_id"] = template_id

            sql = f"""
            UPDATE P_TEMPLATE
            SET {', '.join(updates)}
            WHERE TEMPLATE_ID = :template_id
            RETURNING
                {_SELECT_COLUMNS.strip()};
            """
            result = self.run_and_return(sql, params)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Template não encontrado para atualização.",
                )

            return IndexRepository._map_row(result) or {}
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar template: {exc}",
            ) from exc

    @staticmethod
    def _build_payload(template_schema: PTemplateUpdateSchema) -> dict[str, Any]:
        data = template_schema.model_dump(exclude_none=True)
        return {
            column: data[field]
            for field, column in _FIELD_TO_COLUMN.items()
            if field in data and field != "template_id"
        }
