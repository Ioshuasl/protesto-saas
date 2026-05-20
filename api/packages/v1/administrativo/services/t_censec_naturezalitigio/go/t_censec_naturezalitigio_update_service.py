from packages.v1.administrativo.schemas.t_censec_naturezalitigio_schema import TCensecNaturezalitigioUpdateSchema
from packages.v1.administrativo.actions.t_censec_naturezalitigio.t_censec_naturezalitigio_update_action import UpdateAction

class UpdateService:
    """
    Serviço para a operação de atualização de um registro na tabela
    t_censec_naturezalitigio.
    """
    def execute(self, censec_naturezalitigio_id : int, censec_naturezalitigio_schema: TCensecNaturezalitigioUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            censec_naturezalitigio_schema (TCensecNaturezalitigioUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instanciamento de ações
        update_action = UpdateAction()

        # Retorna o resultado da operação
        return update_action.execute(censec_naturezalitigio_id, censec_naturezalitigio_schema)