from __future__ import annotations

from typing import Any

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import is_firebird_connection_error, run_with_firebird_retry
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_template import get_p_template_model
from packages.v1.administrativo.repositories.p_template.p_template_index_repository import (
    IndexRepository,
)
from packages.v1.administrativo.schemas.p_template_schema import PTemplateUpdateTextoSchema


class UpdateTextoRepository(BaseRepository):
    def execute(self, data: PTemplateUpdateTextoSchema) -> dict[str, Any]:
        if not use_orm_firebird():
            return self._execute_sql(data)

        try:
            return run_with_firebird_retry(lambda: self._execute_orm(data))
        except Exception as exc:
            if is_firebird_connection_error(exc):
                return self._execute_sql(data)
            raise

    def _execute_orm(self, data: PTemplateUpdateTextoSchema) -> dict[str, Any]:
        model = get_p_template_model()
        model.update(
            {"TEXTO": data.texto},
            {"where": {"TEMPLATE_ID": data.template_id}},
        )
        row = model.findOne(
            {
                "attributes": ["TEMPLATE_ID", "DESCRICAO"],
                "where": {"TEMPLATE_ID": data.template_id},
            }
        )
        mapped = IndexRepository._map_row(row)
        if not mapped:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template não encontrado para atualização de texto.",
            )
        return mapped

    def _execute_sql(self, data: PTemplateUpdateTextoSchema) -> dict[str, Any]:
        try:
            sql = """
            UPDATE P_TEMPLATE
            SET TEXTO = :texto
            WHERE TEMPLATE_ID = :template_id
            RETURNING TEMPLATE_ID, DESCRICAO;
            """
            result = self.run_and_return(
                sql,
                {"template_id": data.template_id, "texto": data.texto},
            )
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Template não encontrado para atualização de texto.",
                )
            return IndexRepository._map_row(result) or {}
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar texto do template: {exc}",
            ) from exc

