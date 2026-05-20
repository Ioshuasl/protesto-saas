from packages.v1.sequencia.repositories.g_sequencia.get import Get
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from abstracts.action import BaseAction


class GetAction(BaseAction):

    def execute(self, sequencia_schema: GSequenciaSchema):

        # Instânciamento de repositório
        get = Get()

        # Execução do repositório
        return get.execute(sequencia_schema)
