from abstracts.action import BaseAction
from packages.v1.servicos.balcao.repositories.t_servico_itempedido.t_servico_itempedido_index_ids_repository import (
    TServicoItemPedidoIndexIdsRepository,
)
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemIndexSchema,
)


class TServicoItemPedidoIndexIdsAction(BaseAction):
    def execute(self, data: TServicoItemIndexSchema):
        return TServicoItemPedidoIndexIdsRepository().execute(data)
