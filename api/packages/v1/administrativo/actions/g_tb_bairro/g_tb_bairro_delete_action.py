from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_bairro_schema import GTbBairroIdSchema
from packages.v1.administrativo.repositories.g_tb_bairro.g_tb_bairro_delete_repository import DeleteRepository


class DeleteAction(BaseAction):

    def execute(self, bairro_schema: GTbBairroIdSchema):

        # Instanciamento do repositório
        delete_repository = DeleteRepository()

        # Execução do repositório
        return delete_repository.execute(bairro_schema)