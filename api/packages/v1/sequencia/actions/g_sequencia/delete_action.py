from packages.v1.sequencia.repositories.g_sequencia.delete import Delete
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from abstracts.action import BaseAction


class DeleteAction(BaseAction):

    def execute(self, sequencia_schema: GSequenciaDeleteSchema):

        # Instânciamento de repositório
        delete = Delete()

        # Execução do repositório
        return delete.execute(sequencia_schema)
