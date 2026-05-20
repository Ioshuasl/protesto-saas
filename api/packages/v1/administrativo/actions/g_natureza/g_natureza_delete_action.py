from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_natureza_schema import GNaturezaIdSchema
from packages.v1.administrativo.repositories.g_natureza.g_natureza_delete_repository import DeleteRepository


class DeleteAction(BaseAction):

    def execute(self, natureza_schema: GNaturezaIdSchema):

        # Instanciamento do repositório
        delete_repository = DeleteRepository()

        # Execução do repositório
        return delete_repository.execute(natureza_schema)