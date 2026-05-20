from abstracts.action import BaseAction
from packages.v1.servicos.balcao.repositories.t_servico_itempedido.t_servico_itempedido_update_repository import (
    TServicoItemPedidoUpdateRepository,
)
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemPedidoUpdateSchema,
)


class TServicoItemPedidoUpdateAction(BaseAction):
    def execute(self, data: TServicoItemPedidoUpdateSchema):
        return TServicoItemPedidoUpdateRepository().execute(data)
