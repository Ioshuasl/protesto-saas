from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_natureza.g_natureza_index_by_sistema_id_repository import (
    IndexBySistemaIdRepository,
)
from packages.v1.administrativo.schemas.g_natureza_schema import (
    GNaturezaSistemaIdSchema,
)


class IndexActionBySistemaId(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de todos os registros na tabela g_natureza.
    """

    def execute(self, g_natureza_sistema_id_schema: GNaturezaSistemaIdSchema):
        """
        Executa a operação de listagem no banco de dados.

        Returns:
            A lista de todos os registros.
        """
        # Instanciamento do repositório
        index_repository = IndexBySistemaIdRepository()

        # Execução do repositório
        response = index_repository.execute(g_natureza_sistema_id_schema)

        # Retorno da informação
        return response
