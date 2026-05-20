from abstracts.repository import BaseRepository


class TopServicosTipoRepository(BaseRepository):

    def execute(self):
        sql = """
            SELECT
                FIRST 4
                COUNT(tsip.SERVICO_TIPO_ID) AS quantity,
                tst.SERVICO_TIPO_ID         AS servico_tipo_id,
                tst.DESCRICAO               AS descricao,
                tst.TIPO_ITEM               AS tipo_item,
                tst.TIPO_PESSOA             AS tipo_pessoa,
                tst.REQUER_ABONADOR         AS requer_abonador,
                tst.REQUER_BIOMETRIA        AS requer_biometria,
                tst.REQUER_CPF              AS requer_cpf,
                tst.SERVICO_CAIXA_ID        AS servico_caixa_id,
                tst.SELAR                   AS selar,
                tst.EMOLUMENTO_ID           AS emolumento_id
            FROM T_SERVICO_TIPO tst
            LEFT JOIN T_SERVICO_ITEMPEDIDO tsip
              ON tsip.SERVICO_TIPO_ID = tst.SERVICO_TIPO_ID
            GROUP BY
                tst.SERVICO_TIPO_ID,
                tst.DESCRICAO,
                tst.TIPO_ITEM,
                tst.TIPO_PESSOA,
                tst.REQUER_ABONADOR,
                tst.REQUER_BIOMETRIA,
                tst.REQUER_CPF,
                tst.SERVICO_CAIXA_ID,
                tst.SELAR,
                tst.EMOLUMENTO_ID
            ORDER BY quantity DESC
        """

        return self.fetch_all(sql, {})
