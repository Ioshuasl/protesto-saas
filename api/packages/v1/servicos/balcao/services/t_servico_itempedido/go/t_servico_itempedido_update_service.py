from packages.v1.servicos.balcao.actions.t_servico_itempedido.t_servico_itempedido_update_action import (
    TServicoItemPedidoUpdateAction,
)
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemPedidoUpdateSchema,
)


class TServicoItemPedidoUpdateService:
    def execute(self, data: TServicoItemPedidoUpdateSchema):
        return TServicoItemPedidoUpdateAction().execute(data)
