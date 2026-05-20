from abstracts.action import BaseAction
from packages.v1.servicos.balcao.repositories.t_servico_itempedido.t_servico_itempedido_certidao_save_repository import (
    TServicoItemPedidoCertidaoSaveRepository,
)
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemPedidoCertidaoSaveSchema,
)


class TServicoItemPedidoCertidaSaveAction(BaseAction):
    def execute(self, data: TServicoItemPedidoCertidaoSaveSchema):
        return TServicoItemPedidoCertidaoSaveRepository().execute(data)
