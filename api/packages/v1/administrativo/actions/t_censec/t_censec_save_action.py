from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_censec_schema import TCensecSaveSchema
from packages.v1.administrativo.repositories.t_censec.t_censec_save_repository import SaveRepository

class SaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvar um novo registro na tabela t_censec.
    """

    def execute(self, censec_schema: TCensecSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            censec_schema (TCensecSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O resultado da operação de salvamento.
        """
        # Instanciamento do repositório
        save_repository = SaveRepository()

        # Execução do repositório
        response = save_repository.execute(censec_schema)

        # Retorno da informação
        return response