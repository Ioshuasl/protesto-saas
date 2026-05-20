from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_cidade_schema import GCidadeIdSchema
from packages.v1.administrativo.repositories.g_cidade.g_cidade_delete_repository import DeleteRepository


class DeleteAction(BaseAction):

    def execute(self, g_cidade_schema: GCidadeIdSchema):

        # Instanciamento do repositório
        delete_repository = DeleteRepository()

        # Execução do repositório
        return delete_repository.execute(g_cidade_schema)