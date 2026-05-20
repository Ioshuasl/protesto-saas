from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_cidade_schema import GCidadeNomeSchema
from packages.v1.administrativo.repositories.g_cidade.g_cidade_get_by_nome_repository import GetByNomeRepository


class GetByNomeAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela G_CIDADE por nome (CIDADE_NOME).
    """

    def execute(self, g_cidade_schema: GCidadeNomeSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            g_cidade_schema (GCidadeNomeSchema): O esquema com o nome da cidade a ser buscada.

        Returns:
            O registro encontrado ou None.
        """
        # Instanciamento do repositório
        show_repository = GetByNomeRepository()

        # Execução do repositório
        response = show_repository.execute(g_cidade_schema)

        # Retorno da informação
        return response