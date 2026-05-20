from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_regimecomunhao_schema import GTbRegimecomunhaoIdSchema
from packages.v1.administrativo.repositories.g_tb_regimecomunhao.g_tb_regimecomunhao_show_repository import ShowRepository


class ShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela g_tb_regimecomunhao.
    """

    def execute(self, regimecomunhao_schema: GTbRegimecomunhaoIdSchema):
        """
        Executa a operação de exibição.

        Args:
            regimecomunhao_schema (GTbRegimecomunhaoIdSchema): O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # Instânciamento do repositório
        show_repository = ShowRepository()

        # Execução do repositório
        response = show_repository.execute(regimecomunhao_schema)

        # Retorno da informação
        return response