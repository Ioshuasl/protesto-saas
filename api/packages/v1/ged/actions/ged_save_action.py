from packages.v1.ged.repositories.ged_save_repository import GEDSaveRepository
from packages.v1.ged.schemas.ged_schema import GEDSaveSchema


class GEDSaveAction:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de todos os registros na tabela g_tb_regimebens.
    """

    def execute(self, data: GEDSaveSchema):
        """
        Executa a operação de listagem no banco de dados.

        Returns:
            A lista de todos os registros.
        """
        # Instanciamento do repositório
        save_repository = GEDSaveRepository()

        # Execução do repositório
        response = save_repository.execute(data)

        # Retorno da informação
        return response
