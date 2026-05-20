from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_imovel.t_imovel_index_repository import (
    TImovelIndexRepository,
)
from packages.v1.administrativo.schemas.t_imovel_schema import TImovelIndexSchema


class TImovelIndexAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de todos os registros na tabela t_censec_qualidade.
    """

    def execute(self, t_imovel_index_schema: TImovelIndexSchema):
        """
        Executa a operação de listagem no banco de dados.

        Returns:
            A lista de todos os registros.
        """
        # Instanciamento do repositório
        t_imovel_index_repositoy = TImovelIndexRepository()

        # Execução do repositório
        response = t_imovel_index_repositoy.execute(t_imovel_index_schema)

        # Retorno da informação
        return response
