from abstracts.action import BaseAction
from packages.v1.servicos.balcao.repositories.t_servico_pedido.t_servico_pedido_show_repository import (
    TServicoPedidoShowRepository,
)
from packages.v1.servicos.balcao.schemas.t_servico_pedido_schema import (
    TServicoPedidoIdSchema,
)


class TServicoPedidoShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, t_servico_pedido_id_schema: TServicoPedidoIdSchema):
        """
        Executa a operação de exibição.

        Args:
            t_servico_pedido_id_schema (TServicoPedidoIdSchema):
                O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_servico_pedido_show_repository = TServicoPedidoShowRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_servico_pedido_show_repository.execute(t_servico_pedido_id_schema)

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
