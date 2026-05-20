from packages.v1.sequencia.repositories.g_sequencia.save import Save
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from abstracts.action import BaseAction


class SaveAction(BaseAction):

    def execute(self, sequencia_schema : GSequenciaSchema):

        # Instânciamento de repositório
        save = Save()

        # Execução do repositório
        return save.execute(sequencia_schema)