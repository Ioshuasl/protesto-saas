from abstracts.repository import BaseRepository
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemIndexSchema,
)


class TServicoItemPedidoIndexIdsRepository(BaseRepository):
    """
    Repositório para listagem de itens do pedido de serviço.

    IMPORTANTE:
    - Materializa BLOBs (Firebird) ainda na camada de banco
    - Nunca retorna objetos BlobReader
    - Retorna apenas tipos seguros (dict, bytes, str, int, etc.)
    """

    def execute(self, data: TServicoItemIndexSchema):
        sql = """
                SELECT
                    TSP.SERVICO_ITEMPEDIDO_ID,
                WHERE TSP.SERVICO_PEDIDO_ID = :servico_pedido_id
            """

        params = {
            "servico_pedido_id": data.servico_pedido_id
        }

        return self.fetch_all(sql, params)
