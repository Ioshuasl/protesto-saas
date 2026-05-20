from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_profissao_schema import GTbProfissaoIdSchema
from packages.v1.administrativo.repositories.g_tb_profissao.g_tb_profissao_show_repository import ShowRepository

class GTbProfissaoShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela G_TB_PROFISSAO.
    """

    def execute(self, profissao_schema: GTbProfissaoIdSchema):
        """
        Executa a operação de exibição.
        
        Args:
            profissao_schema (GTbProfissaoIdSchema): O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # Instanciamento do repositório
        show_repository = ShowRepository()

        # Execução do repositório
        response = show_repository.execute(profissao_schema)

        # Retorno da informação
        return response