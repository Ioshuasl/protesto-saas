from packages.v1.administrativo.schemas.g_tb_bairro_schema import GTbBairroUpdateSchema
from packages.v1.administrativo.actions.g_tb_bairro.g_tb_bairro_update_action import UpdateAction

class UpdateService:
    """
    Serviço para a operação de atualização de um registro na tabela
    g_tb_bairro.
    """
    def execute(self, bairro_id : int, bairro_schema: GTbBairroUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            bairro_id (int): O ID do registro a ser atualizado.
            bairro_schema (GTbBairroUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instanciamento de ações
        update_action = UpdateAction()

        # Retorna o resultado da operação
        return update_action.execute(bairro_id, bairro_schema)