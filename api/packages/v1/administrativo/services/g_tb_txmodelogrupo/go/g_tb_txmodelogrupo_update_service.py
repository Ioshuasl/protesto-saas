from packages.v1.administrativo.schemas.g_tb_txmodelogrupo_schema import GTbTxmodelogrupoUpdateSchema
from packages.v1.administrativo.actions.g_tb_txmodelogrupo.g_tb_txmodelogrupo_update_action import UpdateAction

class GTbTxmodelogrupoUpdateService:

    def execute(self, tb_txmodelogrupo_id : int, txmodelogrupo_schema: GTbTxmodelogrupoUpdateSchema):
        """
        Executa a lógica de negócio para a atualização de um registro na tabela
        G_TB_TXMODELOGRUPO.

        Args:
            tb_txmodelogrupo_id (int): O ID do registro a ser atualizado.
            txmodelogrupo_schema (GTbTxmodelogrupoUpdateSchema): O schema com os dados atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instanciamento de ação
        updateAction = UpdateAction()

        # Retorna o resultado da execução da ação de atualização
        return updateAction.execute(tb_txmodelogrupo_id, txmodelogrupo_schema)