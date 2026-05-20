from packages.v1.administrativo.schemas.c_caixa_servico_schema import CCaixaServicoUpdateSchema
from packages.v1.administrativo.actions.c_caixa_servico.c_caixa_servico_update_action import UpdateAction

class CCaixaServicoUpdateService: 

    def execute(self, caixa_servico_id : int, caixa_servico_schema: CCaixaServicoUpdateSchema):     

        # Instânciamento de ações
        updateAction = UpdateAction()

        # Retorna todos produtos desejados
        return updateAction.execute(caixa_servico_id, caixa_servico_schema)