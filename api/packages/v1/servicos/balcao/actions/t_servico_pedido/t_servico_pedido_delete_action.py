from abstracts.action import BaseAction
from packages.v1.servicos.balcao.repositories.t_servico_pedido.t_servico_pedido_delete_repository import (
    TServicoPedidoDeleteRepository,
)
from packages.v1.servicos.balcao.schemas.t_servico_pedido_schema import (
    TServicoPedidoIdSchema,
)


class TServicoPedidoDeleteAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de exclusão de um registro na tabela T_SERVICO_PEDIDO.
    """

    def execute(self, t_servico_pedido_id_schema: TServicoPedidoIdSchema):
        """
        Executa a operação de exclusão no banco de dados.

        Args:
            t_servico_pedido_id_schema (TServicoPedidoIdSchema):
                O esquema contendo o ID do registro a ser excluído.

        Returns:
            O resultado da operação de exclusão.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_servico_pedido_delete_repository = TServicoPedidoDeleteRepository()

        # ----------------------------------------------------
        # Execução da exclusão
        # ----------------------------------------------------
        response = t_servico_pedido_delete_repository.execute(
            t_servico_pedido_id_schema
        )

        return response
