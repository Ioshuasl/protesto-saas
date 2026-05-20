from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_tb_profissao.g_tb_profissao_search_by_descricao_repository import (
    SearchByDescricaoRepository,
)
from packages.v1.administrativo.schemas.g_tb_profissao_schema import GTbProfissaoDescricaoSchema


class GTbProfissaoSearchByDescricaoAction(BaseAction):
    """
    Action responsável por encapsular a operação
    de busca de profissões por descrição.
    """

    def execute(self, profissao_schema: GTbProfissaoDescricaoSchema):
        """
        Executa a operação de busca no banco de dados.
        """
        # Instanciamento do repositório
        search_repository = SearchByDescricaoRepository()

        # Execução do repositório
        response = search_repository.execute(profissao_schema)

        # Retorno da informação
        return response
