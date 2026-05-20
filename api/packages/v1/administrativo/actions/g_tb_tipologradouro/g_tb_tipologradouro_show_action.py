from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_tipologradouro_schema import GTbTipoLogradouroIdSchema
from packages.v1.administrativo.repositories.g_tb_tipologradouro.g_tb_tipologradouro_show_repository import ShowRepository

class ShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela g_tb_tipologradouro.
    """

    def execute(self, tipologradouro_schema: GTbTipoLogradouroIdSchema):
        """
        Executa a operação de exibição.
        
        Args:
            tipologradouro_schema (GTbTipologradouroIdSchema): O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # Instanciamento do repositório
        show_repository = ShowRepository()

        # Execução do repositório
        response = show_repository.execute(tipologradouro_schema)

        # Retorno da informação
        return response