from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_profissao_schema import GTbProfissaoIdSchema
from packages.v1.administrativo.repositories.g_tb_profissao.g_tb_profissao_delete_repository import DeleteRepository


class GTbProfissaoDeleteAction(BaseAction):

    def execute(self, profissao_schema: GTbProfissaoIdSchema):

        # Instanciamento do repositório
        delete_repository = DeleteRepository()

        # Execução do repositório
        return delete_repository.execute(profissao_schema)