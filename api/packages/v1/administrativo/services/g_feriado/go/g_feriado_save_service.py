from fastapi import HTTPException, status

from packages.v1.administrativo.actions.g_feriado.g_feriado_save_action import SaveAction
from packages.v1.administrativo.repositories.g_feriado.g_feriado_get_by_data_tipo_repository import (
    GetByDataTipoRepository,
)
from packages.v1.administrativo.schemas.g_feriado_schema import (
    GFeriadoDataTipoSchema,
    GFeriadoSaveSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class SaveService:
    def _ensure_unique(self, feriado_schema: GFeriadoDataTipoSchema):
        duplicate = GetByDataTipoRepository().execute(feriado_schema)
        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=[
                    {
                        "input": "data",
                        "message": "Já existe feriado cadastrado para esta data e tipo.",
                    }
                ],
            )

    def execute(self, feriado_schema: GFeriadoSaveSchema):
        self._ensure_unique(
            GFeriadoDataTipoSchema(data=feriado_schema.data, tipo=feriado_schema.tipo)
        )

        if not feriado_schema.feriado_id:
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "G_FERIADO"
            feriado_schema.feriado_id = GenerateService().execute(sequencia_schema).sequencia

        save_action = SaveAction()
        return save_action.execute(feriado_schema)
