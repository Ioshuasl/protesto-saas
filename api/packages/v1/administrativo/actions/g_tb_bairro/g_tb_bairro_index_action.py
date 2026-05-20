from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_tb_bairro.g_tb_bairro_index_repository import IndexRepository

class IndexAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de todos os registros na tabela g_tb_bairro.
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