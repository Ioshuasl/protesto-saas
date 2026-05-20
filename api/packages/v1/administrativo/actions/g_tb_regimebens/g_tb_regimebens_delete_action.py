from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_regimebens_schema import GTbRegimebensIdSchema
from packages.v1.administrativo.repositories.g_tb_regimebens.g_tb_regimebens_delete_repository import DeleteRepository


class DeleteAction(BaseAction):

    def execute(self, regimebens_schema: GTbRegimebensIdSchema):

        # Instanciamento do repositório
        delete_repository = DeleteRepository()

        # Execução do repositório
        return delete_repository.execute(regimebens_schema)