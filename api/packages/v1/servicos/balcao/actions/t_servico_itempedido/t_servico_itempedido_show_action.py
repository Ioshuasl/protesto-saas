from abstracts.action import BaseAction
from packages.v1.servicos.balcao.repositories.t_servico_itempedido.t_servico_itempedido_show_repository import (
    TServicoItemPedidoShowRepository,
)
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemPedidoIdSchema,
)


class TServicoItemPedidoShowAction(BaseAction):
    def execute(self, data: TServicoItemPedidoIdSchema):
        return TServicoItemPedidoShowRepository().execute(data)
