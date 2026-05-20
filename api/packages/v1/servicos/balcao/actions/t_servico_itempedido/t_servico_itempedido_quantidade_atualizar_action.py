from abstracts.action import BaseAction
from packages.v1.servicos.balcao.repositories.t_servico_itempedido.t_servico_itempedido_save_repository import (
    TServicoItemPedidoSaveRepository,
)
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemPedidoSaveSchema,
)


class TServicoItemPedidoQuantidadeAtualizarAction(BaseAction):
    def execute(self, data: TServicoItemPedidoSaveSchema):
        return TServicoItemPedidoSaveRepository().execute(data)
