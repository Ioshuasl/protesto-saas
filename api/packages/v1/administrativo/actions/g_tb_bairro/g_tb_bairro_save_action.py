from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_bairro_schema import GTbBairroSaveSchema
from packages.v1.administrativo.repositories.g_tb_bairro.g_tb_bairro_save_repository import SaveRepository

class SaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvar um novo registro na tabela g_tb_bairro.
    """

    def execute(self, bairro_schema: GTbBairroSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            bairro_schema (GTbBairroSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O resultado da operação de salvamento.
        """
        # Instanciamento do repositório
        save_repository = SaveRepository()

        # Execução do repositório
        response = save_repository.execute(bairro_schema)

        # Retorno da informação
        return response