from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_txmodelogrupo_schema import GTbTxmodelogrupoSaveSchema
from packages.v1.administrativo.repositories.g_tb_txmodelogrupo.g_tb_txmodelogrupo_save_repository import SaveRepository


class SaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvar um novo registro na tabela G_TB_TXMODELOGRUPO.
    """

    def execute(self, txmodelogrupo_schema: GTbTxmodelogrupoSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            txmodelogrupo_schema (GTbTxmodelogrupoSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O resultado da operação de salvamento.
        """
        # Instanciamento do repositório
        save_repository = SaveRepository()

        # Execução do repositório
        response = save_repository.execute(txmodelogrupo_schema)

        # Retorno da informação
        return response