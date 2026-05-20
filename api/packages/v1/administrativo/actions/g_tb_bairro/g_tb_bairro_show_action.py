from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_bairro_schema import GTbBairroIdSchema
from packages.v1.administrativo.repositories.g_tb_bairro.g_tb_bairro_show_repository import ShowRepository

class ShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela g_tb_bairro.
    """

    def execute(self, bairro_schema: GTbBairroIdSchema):
        """
        Executa a operação de exibição.
        
        Args:
            bairro_schema (GTbBairroIdSchema): O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # Instânciamento do repositório
        show_repository = ShowRepository()

        # Execução do repositório
        response = show_repository.execute(bairro_schema)

        # Retorno da informação
        return response