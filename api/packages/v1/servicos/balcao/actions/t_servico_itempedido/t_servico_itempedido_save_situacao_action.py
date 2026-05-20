from packages.v1.servicos.balcao.repositories.t_servico_itempedido.t_servico_itempedido_save_situacao_repository import (
    TServicoItemPedidoSaveSituacaoRepository,
)
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemPedidoSaveSituacaoSchema,
)


class TServicoItemPedidoSaveSituacaoAction:
    def execute(self, data: TServicoItemPedidoSaveSituacaoSchema):
        return TServicoItemPedidoSaveSituacaoRepository().execute(data)
