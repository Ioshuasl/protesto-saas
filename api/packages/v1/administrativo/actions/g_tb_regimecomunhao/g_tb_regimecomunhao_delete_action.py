from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_regimecomunhao_schema import GTbRegimecomunhaoIdSchema
from packages.v1.administrativo.repositories.g_tb_regimecomunhao.g_tb_regimecomunhao_delete_repository import DeleteRepository


class DeleteAction(BaseAction):

    def execute(self, regimecomunhao_schema: GTbRegimecomunhaoIdSchema):

        # Instanciamento do repositório
        delete_repository = DeleteRepository()

        # Execução do repositório
        return delete_repository.execute(regimecomunhao_schema)