from __future__ import annotations

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_template import get_p_template_model
from packages.v1.administrativo.schemas.p_template_schema import PTemplateIdSchema


class DeleteRepository(BaseRepository):
    def execute(self, template_schema: PTemplateIdSchema) -> dict[str, int]:
        if use_orm_firebird():
            return self._execute_orm(template_schema)
        return self._execute_sql(template_schema)

    @staticmethod
    def _execute_orm(template_schema: PTemplateIdSchema) -> dict[str, int]:
        get_p_template_model().destroy(
            {"where": {"TEMPLATE_ID": template_schema.template_id}}
        )
        return {"template_id": template_schema.template_id}

    def _execute_sql(self, template_schema: PTemplateIdSchema) -> dict[str, int]:
        try:
            sql = """
            DELETE FROM P_TEMPLATE
            WHERE TEMPLATE_ID = :template_id
            RETURNING TEMPLATE_ID;
            """
            response = self.run_and_return(sql, {"template_id": template_schema.template_id})

            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Template não encontrado para exclusão.",
                )

            return {"template_id": template_schema.template_id}
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir template: {exc}",
            ) from exc
