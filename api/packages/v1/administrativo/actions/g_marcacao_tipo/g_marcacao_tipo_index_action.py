from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_marcacao_tipo.g_marcacao_tipo_index_repository import (
    GMarcacaoTipoIndexRepository,
)


class GMarcacaoTipoIndexAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de todos os registros na tabela G_MARCACAO_TIPO.
    """

    def execute(self):
        """
        Executa a operação de listagem no banco de dados.

        Returns:
            A lista de todos os registros.
        """
        # Instanciamento do repositório
        index_repository = GMarcacaoTipoIndexRepository()

        # Execução do repositório
        response = index_repository.execute()

        # Retorno da informação
        return response
