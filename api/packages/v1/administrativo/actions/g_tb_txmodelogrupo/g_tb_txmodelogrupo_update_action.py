from packages.v1.administrativo.schemas.g_tb_txmodelogrupo_schema import GTbTxmodelogrupoUpdateSchema
from packages.v1.administrativo.repositories.g_tb_txmodelogrupo.g_tb_txmodelogrupo_update_repository import UpdateRepository


class UpdateAction:
    """
    Serviço responsável por encapsular a lógica de negócio para a atualização
    de um registro na tabela G_TB_TXMODELOGRUPO.
    """

    def execute(self, tb_txmodelogrupo_id: int, txmodelogrupo_schema: GTbTxmodelogrupoUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            txmodelogrupo_schema (GTbTxmodelogrupoUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instância o repositório de atualização
        update_repository = UpdateRepository()

        # Chama o método de execução do repositório para realizar a atualização
        return update_repository.execute(tb_txmodelogrupo_id, txmodelogrupo_schema)