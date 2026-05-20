from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_regimecomunhao_schema import GTbRegimecomunhaoDescricaoSchema
from packages.v1.administrativo.repositories.g_tb_regimecomunhao.g_tb_regimecomunhao_get_by_descricao_repository import GetByDescricaoRepository


class GetByDescricaoAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela g_tb_regimecomunhao por descrição.
    """

    def execute(self, regimecomunhao_schema: GTbRegimecomunhaoDescricaoSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            regimecomunhao_schema (GTbRegimecomunhaoDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            O registro encontrado ou None.
        """
        # Instanciamento do repositório
        show_repository = GetByDescricaoRepository()

        # Execução do repositório
        response = show_repository.execute(regimecomunhao_schema)

        # Retorno da informação
        return response