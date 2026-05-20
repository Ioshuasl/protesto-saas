from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_censec_qualidade_schema import TCensecQualidadeIdSchema
from packages.v1.administrativo.repositories.t_censec_qualidade.t_censec_qualidade_show_repository import ShowRepository

class ShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela t_censec_qualidade.
    """

    def execute(self, censec_qualidade_schema: TCensecQualidadeIdSchema):
        """
        Executa a operação de exibição.
        
        Args:
            censec_qualidade_schema (TCensecQualidadeIdSchema): O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # Instânciamento do repositório
        show_repository = ShowRepository()

        # Execução do repositório
        response = show_repository.execute(censec_qualidade_schema)

        # Retorno da informação
        return response