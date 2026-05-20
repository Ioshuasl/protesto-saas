from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_tipologradouro_schema import GTbTipoLogradouroSaveSchema
from packages.v1.administrativo.repositories.g_tb_tipologradouro.g_tb_tipologradouro_save_repository import SaveRepository

class SaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvar um novo registro na tabela g_tb_tipologradouro.
    """

    def execute(self, tipologradouro_schema: GTbTipoLogradouroSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            tipologradouro_schema (GTbTipologradouroSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O resultado da operação de salvamento.
        """
        # Instanciamento do repositório
        save_repository = SaveRepository()

        # Execução do repositório
        response = save_repository.execute(tipologradouro_schema)

        # Retorno da informação
        return response