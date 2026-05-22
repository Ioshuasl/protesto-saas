from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_motivos.p_motivos_save_action import SaveAction
from packages.v1.administrativo.repositories.p_motivos.p_motivos_get_by_codigo_repository import (
    GetByCodigoRepository,
)
from packages.v1.administrativo.schemas.p_motivos_schema import (
    PMotivosCodigoSchema,
    PMotivosSaveSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class SaveService:
    def _ensure_codigo_unique(self, codigo: str, motivos_id: int | None = None):
        duplicate = GetByCodigoRepository().execute(
            PMotivosCodigoSchema(codigo=codigo, motivos_id=motivos_id)
        )
        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=[
                    {
                        "input": "codigo",
                        "message": "Já existe motivo cadastrado com este código.",
                    }
                ],
            )

    def execute(self, motivos_schema: PMotivosSaveSchema):
        self._ensure_codigo_unique(motivos_schema.codigo)

        if not motivos_schema.motivos_id:
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "P_MOTIVOS"
            motivos_schema.motivos_id = GenerateService().execute(sequencia_schema).sequencia

        return SaveAction().execute(motivos_schema)
