from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_minuta_schema import TMinutaSaveSchema
from packages.v1.administrativo.repositories.t_minuta.t_minuta_save_repository import SaveRepository

class SaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvar um novo registro na tabela t_minuta.
    """

    def execute(self, minuta_schema: TMinutaSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            minuta_schema (TMinutaSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O resultado da operação de salvamento.
        """
        # Instanciamento do repositório
        save_repository = SaveRepository()

        # Execução do repositório
        response = save_repository.execute(minuta_schema)

        # Retorno da informação
        return response