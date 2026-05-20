from packages.v1.servicos.balcao.actions.t_servico_itempedido.t_servico_itempedido_save_action import (
    TServicoItemPedidoSaveAction,
)
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemPedidoSaveSituacaoSchema,
)


class TServicoItemPedidoSaveSituacaoService:
    def execute(self, data: TServicoItemPedidoSaveSituacaoSchema):
        return TServicoItemPedidoSaveAction().execute(data)
