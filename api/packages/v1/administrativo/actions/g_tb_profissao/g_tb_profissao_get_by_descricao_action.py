from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_profissao_schema import GTbProfissaoDescricaoSchema
from packages.v1.administrativo.repositories.g_tb_profissao.g_tb_profissao_get_by_descricao_repository import GetByDescricaoRepository

class GTbProfissaoGetByDescricaoAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela G_TB_PROFISSAO por descrição.
    """

    def execute(self, profissao_schema: GTbProfissaoDescricaoSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            profissao_schema (GTbProfissaoDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            O registro encontrado ou None.
        """
        # Instanciamento do repositório
        show_repository = GetByDescricaoRepository()

        # Execução do repositório
        response = show_repository.execute(profissao_schema)

        # Retorno da informação
        return response