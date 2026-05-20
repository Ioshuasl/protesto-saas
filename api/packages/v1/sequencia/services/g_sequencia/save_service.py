from packages.v1.sequencia.actions.g_sequencia.save_action import \
    SaveAction
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema


class SaveService:

    def execute(self, sequencia_schema : GSequenciaSchema):

        # Instânciamento de Action
        saveAction = SaveAction()

        # Execução da Ação
        return saveAction.execute(sequencia_schema)