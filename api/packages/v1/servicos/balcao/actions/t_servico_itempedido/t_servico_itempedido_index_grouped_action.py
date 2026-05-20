from abstracts.action import BaseAction
from packages.v1.servicos.balcao.repositories.t_servico_itempedido.t_servico_itempedido_index_grouped_repository import (
    TServicoItemPedidoIndexGroupedRepository,
)
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemIndexSchema,
)


class TServicoItemPedidoIndexGroupedAction(BaseAction):
    def execute(self, data: TServicoItemIndexSchema):
        return TServicoItemPedidoIndexGroupedRepository().execute(data)
