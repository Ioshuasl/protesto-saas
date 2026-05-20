from abstracts.repository import BaseRepository


class TAtoIsLastLavradoByProtocoloFolhaRepository(BaseRepository):
    """
    Verifica se o ato e o ultimo lavrado no livro considerando protocolo e folha_final.
    """

    def execute(
        self,
        *,
        ato_id,
        livro_andamento_id,
        protocolo,
        folha_final,
    ) -> bool:
        sql = """
            SELECT FIRST 1
                TA.ATO_ID
            FROM T_ATO TA
            WHERE TA.LIVRO_ANDAMENTO_ID = :livro_andamento_id
              AND TA.SITUACAO_ATO = '3'
              AND TA.ATO_ID <> :ato_id
              AND (
                    COALESCE(TA.PROTOCOLO, 0) > :protocolo
                    OR COALESCE(TA.FOLHA_FINAL, 0) > :folha_final
                  )
            ORDER BY
                TA.PROTOCOLO DESC,
                TA.FOLHA_FINAL DESC,
                TA.ATO_ID DESC
        """

        params = {
            "ato_id": ato_id,
            "livro_andamento_id": livro_andamento_id,
            "protocolo": protocolo,
            "folha_final": folha_final,
        }

        response_exists_newer = self.fetch_one(sql, params)
        return response_exists_newer is None
