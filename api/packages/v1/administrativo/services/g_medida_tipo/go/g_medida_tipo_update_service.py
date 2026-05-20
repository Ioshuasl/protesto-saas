from packages.v1.administrativo.schemas.g_medida_tipo_schema import GMedidaTipoUpdateSchema
from packages.v1.administrativo.actions.g_medida_tipo.g_medida_tipo_update_action import UpdateAction

class UpdateService:
    """
    Serviço para a operação de atualização de um registro na tabela
    g_medida_tipo.
    """
    def execute(self, medida_tipo_id : int, medida_tipo_schema: GMedidaTipoUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            medida_tipo_schema (GMedidaTipoUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instanciamento de ações
        update_action = UpdateAction()

        # Retorna o resultado da operação
        return update_action.execute(medida_tipo_id, medida_tipo_schema)