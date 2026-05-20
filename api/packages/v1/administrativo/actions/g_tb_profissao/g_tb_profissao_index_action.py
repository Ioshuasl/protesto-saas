from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_tb_profissao.g_tb_profissao_index_repository import IndexRepository

class GTbProfissaoIndexAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de todos os registros na tabela G_TB_PROFISSAO.
    """

    def execute(self):
        """
        Executa a operação de listagem no banco de dados.

        Returns:
            A lista de todos os registros.
        """
        # Instanciamento do repositório
        index_repository = IndexRepository()

        # Execução do repositório
        response = index_repository.execute()

        # Retorno da informação
        return response