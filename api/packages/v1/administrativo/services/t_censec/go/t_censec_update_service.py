from packages.v1.administrativo.schemas.t_censec_schema import TCensecUpdateSchema
from packages.v1.administrativo.actions.t_censec.t_censec_update_action import UpdateAction

class UpdateService:
    """
    Serviço para a operação de atualização de um registro na tabela
    t_censec.
    """
    def execute(self, censec_id : int, censec_schema: TCensecUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            censec_schema (TCensecUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instanciamento de ações
        update_action = UpdateAction()

        # Retorna o resultado da operação
        return update_action.execute(censec_id, censec_schema)