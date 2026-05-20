from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemPedidoIdSchema,
)


class TServicoItemPedidoDeleteRepository(BaseRepository):
    """
    Repositório responsável pela exclusão de registros na tabela
    T_SERVICO_ITEMPEDIDO.
    """

    def execute(self, data: TServicoItemPedidoIdSchema):
        try:
            sql = """
                DELETE FROM T_SERVICO_ITEMPEDIDO TSI
                WHERE TSI.SERVICO_ITEMPEDIDO_ID = :servico_itempedido_id
                RETURNING *
            """
            params = {
                "servico_itempedido_id": data.servico_itempedido_id
            }

            # Execução da instrução SQL
            response = self.run_and_return(sql, params)

            # Retorna o resultado da exclusão
            return response

        except Exception as e:
            # Lança exceção HTTP em caso de erro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir registro de T_SERVICO_ITEMPEDIDO: {e}",
            )
