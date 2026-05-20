from packages.v1.servicos.balcao.actions.t_servico_pedido.t_servico_pedido_update_action import (
    TServicoPedidoUpdateAction,
)
from packages.v1.servicos.balcao.schemas.t_servico_pedido_schema import (
    TServicoPedidoUpdateSchema,
)


class TServicoPedidoUpdateService:
    """
    Serviço responsável pela operação de atualização de um registro
    na tabela T_SERVICO_PEDIDO.
    """

    def execute(self, t_servico_pedido_update_schema: TServicoPedidoUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            t_servico_pedido_update_schema (TServicoPedidoUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_servico_pedido_update_action = TServicoPedidoUpdateAction()

        # Obtenho a resposta da operação
        response = t_servico_pedido_update_action.execute(
            t_servico_pedido_update_schema
        )

        return response
