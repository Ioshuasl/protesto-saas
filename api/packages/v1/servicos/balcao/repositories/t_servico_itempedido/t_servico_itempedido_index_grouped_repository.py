from abstracts.repository import BaseRepository
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemIndexSchema,
)


class TServicoItemPedidoIndexGroupedRepository(BaseRepository):
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
                    TSP.SERVICO_PEDIDO_ID,
                    TSP.EMOLUMENTO_ID,
                    TSP.EMOLUMENTO_ITEM_ID,
                    GEI.SELO_GRUPO_ID,
                    TSP.SERVICO_TIPO_ID,
                    TSP.TIPO_ITEM,
                    tsp.SITUACAO,
                    ge.DESCRICAO AS EMOLUMENTO_DESCRICAO,
                    tst.DESCRICAO AS SERVICO_TIPO_DESCRICAO,
                    SUM(tsp.VALOR) AS VALOR,
                    SUM(tsp.EMOLUMENTO) AS EMOLUMENTO,
                    SUM(tsp.TAXA_JUDICIARIA) AS TAXA_JUDICIARIA,
                    SUM(tsp.FUNDESP) AS FUNDESP,
                    SUM(tsp.VALOR_ISS) AS VALOR_ISS,
                    SUM(tsp.qtd) AS QTD
                FROM T_SERVICO_ITEMPEDIDO TSP
                JOIN T_SERVICO_TIPO TST
                    ON TSP.SERVICO_TIPO_ID = TST.SERVICO_TIPO_ID
                JOIN G_EMOLUMENTO_ITEM GEI
                    ON TSP.EMOLUMENTO_ITEM_ID = GEI.EMOLUMENTO_ITEM_ID
                JOIN G_EMOLUMENTO GE
                    ON TSP.EMOLUMENTO_ID = GE.EMOLUMENTO_ID
                LEFT JOIN T_PESSOA TE
                    ON TSP.PESSOA_ID = TE.PESSOA_ID
                WHERE TSP.SERVICO_PEDIDO_ID = :servico_pedido_id
                GROUP BY tsp.SERVICO_TIPO_ID,
                    TSP.SERVICO_PEDIDO_ID,
                    TSP.EMOLUMENTO_ID,
                    TSP.EMOLUMENTO_ITEM_ID,
                    GEI.SELO_GRUPO_ID,
                    TSP.SERVICO_TIPO_ID,
                    TSP.TIPO_ITEM,
                    tsp.SITUACAO,
                    ge.DESCRICAO,
                    tst.DESCRICAO,
                    tst.DESCRICAO,
                    tsp.VALOR,
                    tsp.EMOLUMENTO,
                    tsp.TAXA_JUDICIARIA,
                    tsp.FUNDESP
            """

        params = {
            "servico_pedido_id": data.servico_pedido_id
        }
        # 1) Executa a query
        response = self.fetch_all(sql, params)
        # 3) Retorno seguro
        return response
