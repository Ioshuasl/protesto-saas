from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.servicos.balcao.schemas.t_servico_pedido_schema import (
    TServicoPedidoIdSchema,
)


class TServicoPedidoDeleteRepository(BaseRepository):
    """
    Repositório responsável pela exclusão de registros na tabela
    T_SERVICO_PEDIDO.
    """

    def execute(self, t_servico_pedido_id_schema: TServicoPedidoIdSchema):
        """
        Executa a exclusão de um registro específico da tabela T_SERVICO_PEDIDO
        com base no ID informado.

        Args:
            t_servico_pedido_id_schema (TServicoPedidoIdSchema): Esquema contendo o ID do registro a ser excluído.

        Returns:
            O resultado da operação de exclusão.
        """
        try:
            # Montagem do SQL
            sql = """
                DELETE FROM T_SERVICO_PEDIDO GG
                WHERE GG.SERVICO_PEDIDO_ID = :servico_pedido_id
            """

            # Preenchimento dos parâmetros
            params = {"servico_pedido_id": t_servico_pedido_id_schema.servico_pedido_id}

            # Execução da instrução SQL
            response = self.run(sql, params)

            # Retorna o resultado da exclusão
            return response

        except Exception as e:
            # Lança exceção HTTP em caso de erro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir registro de T_SERVICO_PEDIDO: {e}",
            )
