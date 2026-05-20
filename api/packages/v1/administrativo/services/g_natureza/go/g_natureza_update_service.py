from packages.v1.administrativo.schemas.g_natureza_schema import GNaturezaUpdateSchema
from packages.v1.administrativo.actions.g_natureza.g_natureza_update_action import UpdateAction

class UpdateService:
    """
    Serviço para a operação de atualização de um registro na tabela
    g_natureza.
    """
    def execute(self, natureza_id : int, natureza_schema: GNaturezaUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            natureza_schema (GNaturezaUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instanciamento de ações
        update_action = UpdateAction()

        # Retorna o resultado da operação
        return update_action.execute(natureza_id, natureza_schema)