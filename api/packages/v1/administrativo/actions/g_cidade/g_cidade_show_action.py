from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_cidade_schema import GCidadeIdSchema
from packages.v1.administrativo.repositories.g_cidade.g_cidade_show_repository import ShowRepository

class ShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela G_CIDADE, usando o CIDADE_ID.
    """

    def execute(self, g_cidade_schema: GCidadeIdSchema):
        """
        Executa a operação de exibição.
        
        Args:
            g_cidade_schema (GCidadeIdSchema): O esquema com o ID (CIDADE_ID) do registro a ser exibido.

        Returns:
            O resultado da operação de exibição (o registro encontrado ou None).
        """
        # Instanciamento do repositório
        show_repository = ShowRepository()

        # Execução do repositório
        response = show_repository.execute(g_cidade_schema)

        # Retorno da informação
        return response