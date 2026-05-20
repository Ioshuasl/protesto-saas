from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_natureza_schema import GNaturezaIdSchema
from packages.v1.administrativo.repositories.g_natureza.g_natureza_show_repository import ShowRepository

class ShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela g_natureza.
    """

    def execute(self, natureza_schema: GNaturezaIdSchema):
        """
        Executa a operação de exibição.
        
        Args:
            natureza_schema (GNaturezaIdSchema): O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # Instânciamento do repositório
        show_repository = ShowRepository()

        # Execução do repositório
        response = show_repository.execute(natureza_schema)

        # Retorno da informação
        return response