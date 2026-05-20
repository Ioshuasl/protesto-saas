from fastapi import HTTPException, status
from packages.v1.servicos.balcao.actions.t_servico_itempedido.t_servico_itempedido_index_action import (
    TServicoItemPedidoIndexAction,
)
from packages.v1.servicos.balcao.actions.t_servico_pedido.t_servico_pedido_show_action import (
    TServicoPedidoShowAction,
)
from packages.v1.servicos.balcao.actions.t_servico_pedido.t_servico_pedido_update_action import (
    TServicoPedidoUpdateAction,
)
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemIndexSchema,
)
from packages.v1.servicos.balcao.schemas.t_servico_pedido_schema import (
    TServicoPedidoIdSchema,
    TServicoPedidoUpdateValorTotal,
)


class TServicoPedidoUpdateValorTotalService:
    """
    Recalcula o valor total do pedido a partir dos itens já vinculados.
    """

    def execute(self, data: TServicoPedidoUpdateValorTotal):

        # Busca pedido (aggregate root)
        pedido = TServicoPedidoShowAction().execute(
            TServicoPedidoIdSchema(servico_pedido_id=data.servico_pedido_id)
        )

        # Verifica se existe resposta
        if not pedido:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pedido não localizado",
            )

        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        itens_index_action = TServicoItemPedidoIndexAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        itens = itens_index_action.execute(
            TServicoItemIndexSchema(servico_pedido_id=pedido.servico_pedido_id)
        )

        # Atualiza o total do pedido
        total = sum((item.valor or 0) * (item.qtd or 1) for item in itens)

        # Atualiza SOMENTE o valor do pedido
        update_action = TServicoPedidoUpdateAction()

        return update_action.execute(
            TServicoPedidoUpdateValorTotal(
                servico_pedido_id=pedido.servico_pedido_id,
                valor_pedido=total,
                valor_pago=total,  # não altera pagamento
            )
        )
