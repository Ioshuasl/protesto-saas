from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_bairro_schema import GTbBairroDescricaoSchema
from packages.v1.administrativo.repositories.g_tb_bairro.g_tb_bairro_get_by_descricao_repository import GetByDescricaoRepository


class GetByDescricaoAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela g_tb_bairro por descrição.
    """

    def execute(self, bairro_schema: GTbBairroDescricaoSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            bairro_schema (GTbBairroDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            O registro encontrado ou None.
        """
        # Instanciamento do repositório
        show_repository = GetByDescricaoRepository()

        # Execução do repositório
        response = show_repository.execute(bairro_schema)

        # Retorno da informação
        return response