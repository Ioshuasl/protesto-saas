from fastapi import HTTPException, status

from packages.v1.servicos.balcao.actions.t_servico_itempedido.t_servico_itempedido_show_action import (
    TServicoItemPedidoShowAction,
)
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemPedidoIdSchema,
)


class TServicoItemPedidoCertidaoShowService:
    def execute(self, data: TServicoItemPedidoIdSchema):
        result = TServicoItemPedidoShowAction().execute(data)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel localizar o registro de T_SERVICO_ITEMPEDIDO.",
            )

        return result
