from packages.v1.administrativo.schemas.g_tb_tipologradouro_schema import GTbTipoLogradouroUpdateSchema
from packages.v1.administrativo.actions.g_tb_tipologradouro.g_tb_tipologradouro_update_action import UpdateAction

class UpdateService:
    """
    Serviço para a operação de atualização de um registro na tabela
    g_tb_tipologradouro.
    """
    def execute(self, g_tb_tipologradouro_id : int, g_tb_tipologradouro_schema: GTbTipoLogradouroUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            g_tb_tipologradouro_schema (GTbTipoLogradouroUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instanciamento de ações
        update_action = UpdateAction()

        # Retorna o resultado da operação
        return update_action.execute(g_tb_tipologradouro_id, g_tb_tipologradouro_schema)