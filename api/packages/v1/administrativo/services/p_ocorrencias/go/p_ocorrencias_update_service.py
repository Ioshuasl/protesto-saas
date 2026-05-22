from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_ocorrencias.p_ocorrencias_show_action import ShowAction
from packages.v1.administrativo.actions.p_ocorrencias.p_ocorrencias_update_action import (
    UpdateAction,
)
from packages.v1.administrativo.repositories.p_ocorrencias.p_ocorrencias_get_by_codigo_repository import (
    GetByCodigoRepository,
)
from packages.v1.administrativo.schemas.p_ocorrencias_schema import (
    POcorrenciasCodigoSchema,
    POcorrenciasIdSchema,
    POcorrenciasUpdateSchema,
)


class UpdateService:
    def _ensure_codigo_unique(
        self, codigo: str, ocorrencias_id: int, ocorrencias_schema: POcorrenciasUpdateSchema
    ):
        if ocorrencias_schema.codigo is None:
            return
        duplicate = GetByCodigoRepository().execute(
            POcorrenciasCodigoSchema(codigo=codigo, ocorrencias_id=ocorrencias_id)
        )
        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=[
                    {
                        "input": "codigo",
                        "message": "Já existe ocorrência cadastrada com este código.",
                    }
                ],
            )

    def execute(self, ocorrencias_id: int, ocorrencias_schema: POcorrenciasUpdateSchema):
        current = ShowAction().execute(POcorrenciasIdSchema(ocorrencias_id=ocorrencias_id))
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar a ocorrência.",
            )

        codigo = ocorrencias_schema.codigo or current.get("codigo")
        if codigo:
            self._ensure_codigo_unique(codigo, ocorrencias_id, ocorrencias_schema)

        return UpdateAction().execute(ocorrencias_id, ocorrencias_schema)
