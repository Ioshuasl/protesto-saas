from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_censec_schema import TCensecIdSchema
from packages.v1.administrativo.repositories.t_censec.t_censec_show_repository import ShowRepository

class ShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela t_censec.
    """

    def execute(self, censec_schema: TCensecIdSchema):
        """
        Executa a operação de exibição.
        
        Args:
            censec_schema (TCensecIdSchema): O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # Instânciamento do repositório
        show_repository = ShowRepository()

        # Execução do repositório
        response = show_repository.execute(censec_schema)

        # Retorno da informação
        return response