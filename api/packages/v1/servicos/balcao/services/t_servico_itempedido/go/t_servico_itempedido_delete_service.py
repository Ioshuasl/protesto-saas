from fastapi import HTTPException, status
from packages.v1.administrativo.services.g_usuario.go.g_usuario_delete_service import (
    SequenciaDeleteService,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.servicos.balcao.actions.t_servico_itempedido.t_servico_itempedido_delete_action import (
    TServicoItemPedidoDeleteAction,
)
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemPedidoIdSchema,
)
from packages.v1.servicos.balcao.schemas.t_servico_pedido_schema import (
    TServicoPedidoUpdateValorTotal,
)
from packages.v1.servicos.balcao.services.t_servico_itempedido.go.t_servico_itempedido_show_service import (
    TServicoItemPedidoShowService,
)
from packages.v1.servicos.balcao.services.t_servico_pedido.go.t_servico_pedido_update_valor_total_service import (
    TServicoPedidoUpdateValorTotalService,
)


class TServicoItemPedidoDeleteService:
    def execute(self, data: TServicoItemPedidoIdSchema):
        item = TServicoItemPedidoShowService().execute(
            TServicoItemPedidoIdSchema(servico_itempedido_id=data.servico_itempedido_id)
        )

        if not item:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Falha ao localizar item.",
            )

        result = TServicoItemPedidoDeleteAction().execute(data)

        TServicoPedidoUpdateValorTotalService().execute(
            TServicoPedidoUpdateValorTotal(
                servico_pedido_id=item.servico_pedido_id,
                valor_pedido=item.valor,
                valor_pago=item.valor,
                operacao=1,
            )
        )

        if result:
            SequenciaDeleteService().execute(
                GSequenciaDeleteSchema(
                    sequencia=result.servico_itempedido_id,
                    tabela="T_SERVICO_ITEMPEDIDO",
                )
            )
            return result

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nao foi possivel excluir o registro ou ele nao existe.",
        )
