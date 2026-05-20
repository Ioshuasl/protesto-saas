from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_estadocivil_schema import GTbEstadoCivilIdSchema
from packages.v1.administrativo.repositories.g_tb_estadocivil.g_tb_estadocivil_show_repository import ShowRepository

class ShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela g_tb_estadocivil.
    """

    def execute(self, estadocivil_schema: GTbEstadoCivilIdSchema):
        """
        Executa a operação de exibição.
        
        Args:
            estadocivil_schema (GTbEstadoCivilIdSchema): O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # Instânciamento do repositório
        show_repository = ShowRepository()

        # Execução do repositório
        response = show_repository.execute(estadocivil_schema)

        # Retorno da informação
        return response