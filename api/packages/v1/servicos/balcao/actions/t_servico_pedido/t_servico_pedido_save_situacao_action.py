from abstracts.action import BaseAction
from packages.v1.servicos.balcao.repositories.t_servico_pedido.t_servico_pedido_save_situacao_repository import (
    TServicoPedidoSaveSituacaoRepository,
)
from packages.v1.servicos.balcao.schemas.t_servico_pedido_schema import (
    TServicoPedidoSaveSituacaoSchema,
)


class TServicoPedidoSaveSituacaoAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvamento de um novo registro na tabela T_SERVICO_PEDIDO.
    """

    def execute(self, data: TServicoPedidoSaveSituacaoSchema):
        """
        Executa a operação de salvamento.

        Args:
            t_servico_pedido_schema (TServicoPedidoSchema):
                O esquema com os dados a serem persistidos.

        Returns:
            O resultado da operação de salvamento.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_servico_pedido_save_situacao_repository = (
            TServicoPedidoSaveSituacaoRepository()
        )

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_servico_pedido_save_situacao_repository.execute(data)

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
