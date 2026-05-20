from abstracts.action import BaseAction
from packages.v1.servicos.balcao.repositories.t_servico_pedido.t_servico_pedido_update_repository import (
    TServicoPedidoUpdateRepository,
)
from packages.v1.servicos.balcao.schemas.t_servico_pedido_schema import (
    TServicoPedidoUpdateSchema,
)


class TServicoPedidoUpdateAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a atualização
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, t_servico_pedido_update_schema: TServicoPedidoUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            t_servico_pedido_update_schema (TServicoPedidoUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório de atualização
        # ----------------------------------------------------
        t_servico_pedido_update_repository = TServicoPedidoUpdateRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_servico_pedido_update_repository.execute(
            t_servico_pedido_update_schema
        )

        # ----------------------------------------------------
        # Retorno do resultado
        # ----------------------------------------------------
        return response
