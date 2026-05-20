from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_regimebens_schema import GTbRegimebensIdSchema
from packages.v1.administrativo.repositories.g_tb_regimebens.g_tb_regimebens_show_repository import ShowRepository

class ShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela g_tb_regimebens.
    """

    def execute(self, regimebens_schema: GTbRegimebensIdSchema):
        """
        Executa a operação de exibição.
        
        Args:
            regimebens_schema (GTbRegimebensIdSchema): O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # Instânciamento do repositório
        show_repository = ShowRepository()

        # Execução do repositório
        response = show_repository.execute(regimebens_schema)

        # Retorno da informação
        return response