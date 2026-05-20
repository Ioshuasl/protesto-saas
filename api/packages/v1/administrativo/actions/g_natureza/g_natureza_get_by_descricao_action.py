from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_natureza_schema import GNaturezaDescricaoSchema
from packages.v1.administrativo.repositories.g_natureza.g_natureza_get_by_descricao_repository import GetByDescricaoRepository


class GetByDescricaoAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela g_natureza por descrição.
    """

    def execute(self, natureza_schema: GNaturezaDescricaoSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            natureza_schema (GNaturezaDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            O registro encontrado ou None.
        """
        # Instanciamento do repositório
        show_repository = GetByDescricaoRepository()

        # Execução do repositório
        response = show_repository.execute(natureza_schema)

        # Retorno da informação
        return response