from abstracts.action import BaseAction
from packages.v1.servicos.balcao.repositories.t_servico_itempedido.t_servico_itempedido_delete_repository import (
    TServicoItemPedidoDeleteRepository,
)
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemPedidoIdSchema,
)


class TServicoItemPedidoDeleteAction(BaseAction):
    def execute(self, data: TServicoItemPedidoIdSchema):
        return TServicoItemPedidoDeleteRepository().execute(data)
