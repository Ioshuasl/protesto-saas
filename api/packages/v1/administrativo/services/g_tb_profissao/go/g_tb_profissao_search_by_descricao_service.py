from packages.v1.administrativo.actions.g_tb_profissao.g_tb_profissao_search_by_descricao_action import (
    GTbProfissaoSearchByDescricaoAction,
)
from packages.v1.administrativo.schemas.g_tb_profissao_schema import GTbProfissaoDescricaoSchema


class SearchByDescricaoService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de registros na tabela G_TB_PROFISSAO por descrição.
    """

    def execute(self, profissao_schema: GTbProfissaoDescricaoSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            profissao_schema (GTbProfissaoDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            Lista de profissões encontradas.
        """
        # Instanciamento da action
        search_action = GTbProfissaoSearchByDescricaoAction()

        # Executa a busca em questão
        data = search_action.execute(profissao_schema)

        # Retorna os dados localizados (lista vazia quando não houver resultados)
        return data or []
