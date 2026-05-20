from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemPedidoIdSchema,
)


class TServicoItemPedidoShowRepository(BaseRepository):

    def execute(self, data: TServicoItemPedidoIdSchema):
        try:
            sql = """
                SELECT
                        TSP.SERVICO_ITEMPEDIDO_ID,
                        TSP.SERVICO_PEDIDO_ID,
                        TSP.EMOLUMENTO_ID,
                        TSP.EMOLUMENTO_ITEM_ID,
                        TSP.SERVICO_TIPO_ID,
                        TSP.TIPO_ITEM,
                        TSP.QTD,
                        TSP.EMOLUMENTO,
                        TSP.TAXA_JUDICIARIA,
                        TSP.VALOR_ISS,
                        TSP.FUNDESP,
                        TSP.VALOR,
                        TSP.CERTIDAO_TEXTO,
                        TSP.CERTIDAO_ATO_ID,
                        TST.DESCRICAO AS SERVICO_TIPO_DESCRICAO,
                        TSP.SITUACAO,
                        TSE.ETIQUETA_MODELO_ID,
                        GMT.TEXTO AS ETIQUETA_TEXTO,
                        GMT.GRUPO,
                        TE.NOME,
                        TE.CPF_CNPJ,
                        TE.PESSOA_ID,
                        GE.DESCRICAO AS EMOLUMENTO_DESCRICAO
                    FROM T_SERVICO_ITEMPEDIDO TSP
                    JOIN T_SERVICO_TIPO TST
                        ON TSP.SERVICO_TIPO_ID = TST.SERVICO_TIPO_ID
                    LEFT JOIN T_SERVICO_ETIQUETA TSE
                        ON TST.SERVICO_TIPO_ID = TSE.SERVICO_TIPO_ID
                    LEFT JOIN G_MARCACAO_TIPO GMT
                        ON TSE.ETIQUETA_MODELO_ID = GMT.MARCACAO_TIPO_ID
                    JOIN G_EMOLUMENTO GE
                        ON TSP.EMOLUMENTO_ID = GE.EMOLUMENTO_ID
                    LEFT JOIN T_PESSOA TE
                        ON TSP.PESSOA_ID = TE.PESSOA_ID
                    WHERE TSP.SERVICO_ITEMPEDIDO_ID = :servico_itempedido_id
            """
            params = data.model_dump(exclude_unset=True)
            # Execução do SQL
            result = self.fetch_one(sql, params)
            # Validação de retorno
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Registro de T_SERVICO_ITEMPEDIDO não encontrado.",
                )

            return result

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao buscar registro em T_SERVICO_ITEMPEDIDO: {e}",
            )
