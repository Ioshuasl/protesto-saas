from packages.v1.servicos.balcao.actions.t_servico_pedido.t_servico_pedido_delete_action import (
    TServicoPedidoDeleteAction,
)
from packages.v1.servicos.balcao.schemas.t_servico_pedido_schema import (
    TServicoPedidoIdSchema,
)


class TServicoPedidoDeleteService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de exclusão de um registro na tabela T_SERVICO_PEDIDO.
    """

    def execute(self, t_servico_pedido_id_schema: TServicoPedidoIdSchema):
        """
        Executa a operação de exclusão do registro no banco de dados.

        Args:
            t_servico_pedido_id_schema (TServicoPedidoIdSchema):
                O esquema com o ID do registro a ser excluído.

        Returns:
            O resultado da operação de exclusão.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_servico_pedido_delete_action = TServicoPedidoDeleteAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = t_servico_pedido_delete_action.execute(t_servico_pedido_id_schema)

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
