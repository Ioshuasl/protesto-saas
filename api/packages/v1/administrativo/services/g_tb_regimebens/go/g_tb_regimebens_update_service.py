from packages.v1.administrativo.schemas.g_tb_regimebens_schema import GTbRegimebensUpdateSchema
from packages.v1.administrativo.actions.g_tb_regimebens.g_tb_regimebens_update_action import UpdateAction

class GTbRegimebensUpdateService:
    """
    Serviço para a operação de atualização de um registro na tabela
    g_tb_regimebens.
    """
    def execute(self, tb_regimebens_id: int, regimebens_schema: GTbRegimebensUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            regimebens_schema (GTbRegimebensUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instanciamento de ações
        update_action = UpdateAction()

        # Retorna o resultado da operação
        return update_action.execute(tb_regimebens_id, regimebens_schema)