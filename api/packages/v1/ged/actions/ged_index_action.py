from packages.v1.ged.repositories.ged_index_repository import GEDIndexRepository
from packages.v1.ged.schemas.ged_schema import GEDIndexSchema


class GEDIndexAction:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de todos os registros na tabela g_tb_regimebens.
    """

    def execute(self, data: GEDIndexSchema):
        """
        Executa a operação de listagem no banco de dados.

        Returns:
            A lista de todos os registros.
        """
        # Instanciamento do repositório
        index_repository = GEDIndexRepository()

        # Execução do repositório
        response = index_repository.execute(data)

        # Retorno da informação
        return response
