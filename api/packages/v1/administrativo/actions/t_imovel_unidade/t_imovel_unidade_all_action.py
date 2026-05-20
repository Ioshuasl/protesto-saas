from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_imovel_unidade.t_imovel_unidade_all_repository import (
    TImovelUnidadeAllRepository,
)


class TImovelUnidadeAllAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de todos os registros na tabela t_censec_qualidade.
    """

    def execute(self):
        """
        Executa a operação de listagem no banco de dados.

        Returns:
            A lista de todos os registros.
        """
        # Instanciamento do repositório
        all_repository = TImovelUnidadeAllRepository()

        # Execução do repositório
        response = all_repository.execute()

        # Retorno da informação
        return response
