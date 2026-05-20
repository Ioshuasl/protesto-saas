from packages.v1.administrativo.schemas.g_tb_regimecomunhao_schema import GTbRegimecomunhaoUpdateSchema
from packages.v1.administrativo.actions.g_tb_regimecomunhao.g_tb_regimecomunhao_update_action import UpdateAction

class GTbRegimecomunhaoUpdateService: 

    def execute(self, tb_regimecomunhao_id : int, regimecomunhao_schema: GTbRegimecomunhaoUpdateSchema):     

        # Instanciamento de ações
        updateAction = UpdateAction()

        # Retorna todos produtos desejados
        return updateAction.execute(tb_regimecomunhao_id, regimecomunhao_schema)