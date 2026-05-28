from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_template import get_p_template_model
from packages.v1.administrativo.schemas.p_template_schema import PTemplateIdSchema


class ShowTextoRepository(BaseRepository):
    def execute(self, template_schema: PTemplateIdSchema) -> dict[str, Any]:
        if use_orm_firebird():
            return self._execute_orm(template_schema)
        return self._execute_sql(template_schema)

    def _execute_orm(self, template_schema: PTemplateIdSchema) -> dict[str, Any]:
        row = get_p_template_model().findOne(
            {
                "attributes": ["TEMPLATE_ID", "DESCRICAO", "TEXTO"],
                "where": {"TEMPLATE_ID": template_schema.template_id},
            }
        )
        result = self._map_row(row)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template não encontrado.",
            )
        return result

    def _execute_sql(self, template_schema: PTemplateIdSchema) -> dict[str, Any]:
        try:
            sql = """
            SELECT
                TEMPLATE_ID,
                DESCRICAO,
                TEXTO
            FROM P_TEMPLATE
            WHERE TEMPLATE_ID = :template_id
            """
            result = self.fetch_one(sql, {"template_id": template_schema.template_id})
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Template não encontrado.",
                )
            return self._map_row(result) or {}
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar texto do template: {exc}",
            ) from exc

    @staticmethod
    def _map_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        template_id = mapped.get("template_id")
        if isinstance(template_id, Decimal):
            mapped["template_id"] = int(template_id)

        texto = mapped.get("texto")
        if isinstance(texto, memoryview):
            mapped["texto"] = texto.tobytes()

        return {
            "template_id": mapped.get("template_id"),
            "descricao": mapped.get("descricao"),
            "texto": mapped.get("texto"),
        }

