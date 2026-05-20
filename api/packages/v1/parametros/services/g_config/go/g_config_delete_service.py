from fastapi import HTTPException, status

from packages.v1.parametros.actions.g_config.g_config_delete_action import (
    GConfigDeleteAction,
)
from packages.v1.parametros.actions.g_config.g_config_show_action import GConfigShowAction
from packages.v1.parametros.schemas.g_config_schema import GConfigIdSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import (
    DeleteService as SequenciaDeleteService,
)


class GConfigDeleteService:
    def execute(self, data: GConfigIdSchema):
        show_action = GConfigShowAction()
        current = show_action.execute(data)
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel localizar G_CONFIG.",
            )

        delete_action = GConfigDeleteAction()
        deleted = delete_action.execute(data)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel excluir G_CONFIG.",
            )

        seq_service = SequenciaDeleteService()
        seq_service.execute(
            GSequenciaDeleteSchema(
                sequencia=int(data.config_id),
                tabela="G_CONFIG",
            )
        )

        return deleted
