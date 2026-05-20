from packages.v1.servicos.balcao.actions.t_servico_itempedido.t_servico_itempedido_index_ids_action import (
    TServicoItemPedidoIndexIdsAction,
)
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemIndexSchema,
)


class TServicoItemPedidoIndexIdsService:
    def execute(self, data: TServicoItemIndexSchema):
        return TServicoItemPedidoIndexIdsAction().execute(data)
