from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_ato_partetipo.t_ato_partetipo_index_repository import (
    TAtoParteTipoIndexRepository,
)


class TAtoParteTipoIndexAction(BaseAction):
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
        t_ato_partetipo_index_repositoy = TAtoParteTipoIndexRepository()

        # Execução do repositório
        response = t_ato_partetipo_index_repositoy.execute()

        # Retorno da informação
        return response
