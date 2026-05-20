from packages.v1.administrativo.actions.g_feriado.g_feriado_delete_action import DeleteAction
from packages.v1.administrativo.actions.g_feriado.g_feriado_show_action import ShowAction
from packages.v1.administrativo.schemas.g_feriado_schema import GFeriadoIdSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import (
    DeleteService as SequenciaDeleteService,
)


class DeleteService:
    def execute(self, feriado_schema: GFeriadoIdSchema):
        ShowAction().execute(feriado_schema)

        delete_action = DeleteAction()
        data = delete_action.execute(feriado_schema)

        if data:
            seq_service = SequenciaDeleteService()
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=feriado_schema.feriado_id,
                tabela="G_FERIADO",
            )
            seq_service.execute(sequencia_schema)

        return data
