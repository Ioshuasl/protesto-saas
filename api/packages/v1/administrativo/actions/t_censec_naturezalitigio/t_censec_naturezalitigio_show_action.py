from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_censec_naturezalitigio_schema import TCensecNaturezalitigioIdSchema
from packages.v1.administrativo.repositories.t_censec_naturezalitigio.t_censec_naturezalitigio_show_repository import ShowRepository

class ShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela t_censec_naturezalitigio.
    """

    def execute(self, censec_naturezalitigio_schema: TCensecNaturezalitigioIdSchema):
        """
        Executa a operação de exibição.

        Args:
            censec_naturezalitigio_schema (TCensecNaturezalitigioIdSchema): O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # Instânciamento do repositório
        show_repository = ShowRepository()

        # Execução do repositório
        response = show_repository.execute(censec_naturezalitigio_schema)

        # Retorno da informação
        return response