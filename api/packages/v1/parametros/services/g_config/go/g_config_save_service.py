from fastapi import HTTPException, status

from packages.v1.parametros.actions.g_config.g_config_save_action import GConfigSaveAction
from packages.v1.parametros.schemas.g_config_schema import GConfigSaveSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class GConfigSaveService:
    def execute(self, data: GConfigSaveSchema):
        if not data.config_id:
            sequencia_schema = GSequenciaSchema(tabela="G_CONFIG")
            generate = GenerateService()
            sequencia = generate.execute(sequencia_schema)
            data.config_id = float(sequencia.sequencia)

        action = GConfigSaveAction()
        response = action.execute(data)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Nao foi possivel salvar G_CONFIG.",
            )
        return response
