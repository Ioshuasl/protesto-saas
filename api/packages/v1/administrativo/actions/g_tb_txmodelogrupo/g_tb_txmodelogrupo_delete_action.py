from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_txmodelogrupo_schema import GTbTxmodelogrupoIdSchema
from packages.v1.administrativo.repositories.g_tb_txmodelogrupo.g_tb_txmodelogrupo_delete_repository import DeleteRepository


class DeleteAction(BaseAction):

    def execute(self, txmodelogrupo_schema: GTbTxmodelogrupoIdSchema):

        # Instanciamento do repositório
        delete_repository = DeleteRepository()

        # Execução do repositório
        return delete_repository.execute(txmodelogrupo_schema)