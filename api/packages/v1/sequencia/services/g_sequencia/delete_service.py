from packages.v1.sequencia.actions.g_sequencia.delete_action import DeleteAction
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema


class DeleteService:

    def execute(self, sequencia_schema: GSequenciaDeleteSchema):

        # Instânciamento de Action
        deleteAction = DeleteAction()

        # Execução da Ação
        return deleteAction.execute(sequencia_schema)
