from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_minuta_schema import TMinutaIdSchema
from packages.v1.administrativo.repositories.t_minuta.t_minuta_show_repository import ShowRepository

class ShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela t_minuta.
    """

    def execute(self, minuta_schema: TMinutaIdSchema):
        """
        Executa a operação de exibição.
        
        Args:
            minuta_schema (TMinutaIdSchema): O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # Instânciamento do repositório
        show_repository = ShowRepository()

        # Execução do repositório
        response = show_repository.execute(minuta_schema)

        # Retorno da informação
        return response