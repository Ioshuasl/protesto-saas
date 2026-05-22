from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_ocorrencia_andamento.p_ocorrencia_andamento_save_action import (
    SaveAction,
)
from packages.v1.administrativo.repositories.p_ocorrencia_andamento.p_ocorrencia_andamento_get_by_codigo_repository import (
    GetByCodigoRepository,
)
from packages.v1.administrativo.schemas.p_ocorrencia_andamento_schema import (
    POcorrenciaAndamentoCodigoSchema,
    POcorrenciaAndamentoSaveSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class SaveService:
    def _ensure_codigo_unique(self, codigo: str, ocorrencia_andamento_id: int | None = None):
        duplicate = GetByCodigoRepository().execute(
            POcorrenciaAndamentoCodigoSchema(
                codigo=codigo, ocorrencia_andamento_id=ocorrencia_andamento_id
            )
        )
        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=[
                    {
                        "input": "codigo",
                        "message": "Já existe ocorrência de andamento cadastrada com este código.",
                    }
                ],
            )

    def execute(self, ocorrencia_andamento_schema: POcorrenciaAndamentoSaveSchema):
        self._ensure_codigo_unique(ocorrencia_andamento_schema.codigo)

        if not ocorrencia_andamento_schema.ocorrencia_andamento_id:
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "P_OCORRENCIA_ANDAMENTO"
            ocorrencia_andamento_schema.ocorrencia_andamento_id = GenerateService().execute(
                sequencia_schema
            ).sequencia

        return SaveAction().execute(ocorrencia_andamento_schema)
