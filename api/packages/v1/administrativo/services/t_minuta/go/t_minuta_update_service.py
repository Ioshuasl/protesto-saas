from packages.v1.administrativo.schemas.t_minuta_schema import TMinutaUpdateSchema
from packages.v1.administrativo.actions.t_minuta.t_minuta_update_action import UpdateAction

class UpdateService:
    """
    Serviço para a operação de atualização de um registro na tabela
    t_minuta.
    """
    def execute(self, minuta_id : int, minuta_schema: TMinutaUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            minuta_schema (TMinutaUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instanciamento de ações
        update_action = UpdateAction()

        # Retorna o resultado da operação
        return update_action.execute(minuta_id, minuta_schema)