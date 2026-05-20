from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_cidade.g_cidade_index_repository import (
    IndexRepository,
)
from packages.v1.administrativo.schemas.g_cidade_schema import GCidadeIndexSchema


class IndexAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de todos os registros na tabela G_CIDADE.
    """

    def execute(self, data: GCidadeIndexSchema):
        """
        Executa a operação de listagem no banco de dados.

        Returns:
            A lista de todos os registros.
        """
        # Instanciamento do repositório
        index_repository = IndexRepository()

        # Execução do repositório
        response = index_repository.execute(data)

        # Retorno da informação
        return response
