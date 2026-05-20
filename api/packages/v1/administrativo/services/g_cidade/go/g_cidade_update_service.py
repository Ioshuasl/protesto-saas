from packages.v1.administrativo.schemas.g_cidade_schema import GCidadeUpdateSchema
from packages.v1.administrativo.actions.g_cidade.g_cidade_update_action import UpdateAction

class UpdateService:
    """
    Serviço para a operação de atualização de um registro na tabela
    G_CIDADE.
    """
    def execute(self, cidade_id : int, g_cidade_schema: GCidadeUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            cidade_id (int): O ID (CIDADE_ID) do registro a ser atualizado.
            g_cidade_schema (GCidadeUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instanciamento de ações
        update_action = UpdateAction()

        # Retorna o resultado da operação
        return update_action.execute(cidade_id, g_cidade_schema)