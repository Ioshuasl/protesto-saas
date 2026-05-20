from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_censec_naturezalitigio_schema import TCensecNaturezalitigioSaveSchema
from packages.v1.administrativo.repositories.t_censec_naturezalitigio.t_censec_naturezalitigio_save_repository import SaveRepository

class SaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvar um novo registro na tabela t_censec_naturezalitigio.
    """

    def execute(self, censec_naturezalitigio_schema: TCensecNaturezalitigioSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            censec_naturezalitigio_schema (TCensecNaturezalitigioSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O resultado da operação de salvamento.
        """
        # Instanciamento do repositório
        save_repository = SaveRepository()

        # Execução do repositório
        response = save_repository.execute(censec_naturezalitigio_schema)

        # Retorno da informação
        return response