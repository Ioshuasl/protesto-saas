from packages.v1.administrativo.schemas.g_tb_estadocivil_schema import GTbEstadoCivilUpdateSchema
from packages.v1.administrativo.actions.g_tb_estadocivil.g_tb_estadocivil_update_action import UpdateAction

class UpdateService:
    """
    Serviço para a operação de atualização de um registro na tabela
    G_TB_ESTADOCIVIL.
    """
    def execute(self, tb_estadocivil_id : int, estado_civil_schema: GTbEstadoCivilUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            estado_civil_schema (GTBEstadoCivilUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instanciamento de ações
        update_action = UpdateAction()

        # Retorna o resultado da operação
        return update_action.execute(tb_estadocivil_id, estado_civil_schema)