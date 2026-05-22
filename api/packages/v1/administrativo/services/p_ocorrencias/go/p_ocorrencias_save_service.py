from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_ocorrencias.p_ocorrencias_save_action import SaveAction
from packages.v1.administrativo.repositories.p_ocorrencias.p_ocorrencias_get_by_codigo_repository import (
    GetByCodigoRepository,
)
from packages.v1.administrativo.schemas.p_ocorrencias_schema import (
    POcorrenciasCodigoSchema,
    POcorrenciasSaveSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class SaveService:
    def _ensure_codigo_unique(self, codigo: str, ocorrencias_id: int | None = None):
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

    def execute(self, ocorrencias_schema: POcorrenciasSaveSchema):
        self._ensure_codigo_unique(ocorrencias_schema.codigo)

        if not ocorrencias_schema.ocorrencias_id:
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "P_OCORRENCIAS"
            ocorrencias_schema.ocorrencias_id = GenerateService().execute(
                sequencia_schema
            ).sequencia

        return SaveAction().execute(ocorrencias_schema)
