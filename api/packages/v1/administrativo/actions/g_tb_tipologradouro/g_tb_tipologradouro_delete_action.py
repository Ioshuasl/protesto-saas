from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_tipologradouro_schema import GTbTipoLogradouroIdSchema
from packages.v1.administrativo.repositories.g_tb_tipologradouro.g_tb_tipologradouro_delete_repository import DeleteRepository


class DeleteAction(BaseAction):

    def execute(self, tipologradouro_schema: GTbTipoLogradouroIdSchema):

        # Instanciamento do repositório
        delete_repository = DeleteRepository()

        # Execução do repositório
        return delete_repository.execute(tipologradouro_schema)