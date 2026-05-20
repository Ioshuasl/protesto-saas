from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_regimebens_schema import GTbRegimebensSaveSchema
from packages.v1.administrativo.repositories.g_tb_regimebens.g_tb_regimebens_save_repository import SaveRepository

class SaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvar um novo registro na tabela g_tb_regimebens.
    """

    def execute(self, regimebens_schema: GTbRegimebensSaveSchema):
        """
        Executa a operação de salvamento.
        
        Args:
            regimebens_schema (GTbRegimebensSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O resultado da operação de salvamento.
        """
        # Instânciamento do repositório
        save_repository = SaveRepository()

        # Execução do repositório
        response = save_repository.execute(regimebens_schema)

        # Retorno da informação
        return response