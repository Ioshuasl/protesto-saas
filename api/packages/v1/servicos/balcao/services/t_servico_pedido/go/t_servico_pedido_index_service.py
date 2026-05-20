from packages.v1.servicos.balcao.actions.t_servico_pedido.t_servico_pedido_index_action import (
    TServicoPedidoIndexAction,
)
from fastapi import HTTPException, status


class TServicoPedidoIndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela T_SERVICO_PEDIDO.
    """

    def execute(self):
        """
        Executa a operação de busca de todos os registros no banco de dados.

        Args:
            t_servico_pedido_index_schema (TServicoPedidoIndexSchema):
                Esquema que pode conter filtros ou parâmetros de busca.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_servico_pedido_index_action = TServicoPedidoIndexAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = t_servico_pedido_index_action.execute()

        # ----------------------------------------------------
        # Verificação de retorno
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar registros de T_SERVICO_PEDIDO.",
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
