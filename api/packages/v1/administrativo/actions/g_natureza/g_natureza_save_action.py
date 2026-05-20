from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_natureza_schema import GNaturezaSaveSchema
from packages.v1.administrativo.repositories.g_natureza.g_natureza_save_repository import SaveRepository

class SaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvar um novo registro na tabela g_natureza.
    """

    def execute(self, natureza_schema: GNaturezaSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            natureza_schema (GNaturezaSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O resultado da operação de salvamento.
        """
        # Instanciamento do repositório
        save_repository = SaveRepository()

        # Execução do repositório
        response = save_repository.execute(natureza_schema)

        # Retorno da informação
        return response