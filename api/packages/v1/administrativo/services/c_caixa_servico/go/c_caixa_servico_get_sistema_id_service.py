
from packages.v1.administrativo.schemas.c_caixa_servico_schema import CCaixaServicoSistemaIdSchema
from packages.v1.administrativo.actions.c_caixa_servico.c_caixa_servico_get_by_sistema_id_action import ShowSistemaIdAction

class GetSistemaIdService:

    def execute(self, caixa_servico_schema: CCaixaServicoSistemaIdSchema):

        # Instânciamento de ação
        show_sistema_id_action = ShowSistemaIdAction()

        # Executa a ação em questão
        data = show_sistema_id_action.execute(caixa_servico_schema)

        # Retorno da informação
        return data