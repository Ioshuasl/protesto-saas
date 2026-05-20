from abstracts.action import BaseAction
from packages.v1.servicos.balcao.repositories.t_servico_itempedido.t_servico_itempedido_index_repository import (
    TServicoItemPedidoIndexRepository,
)
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemIndexSchema,
)


class TServicoItemPedidoIndexAction(BaseAction):
    def execute(self, data: TServicoItemIndexSchema):
        return TServicoItemPedidoIndexRepository().execute(data)
