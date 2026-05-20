from abstracts.repository import BaseRepository
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoIdSchema


class TAtoAtoAnteriorRepository(BaseRepository):
    def execute(self, t_ato_id_schema: TAtoIdSchema):
        sql = """
            SELECT FIRST 1
                TA.ATO_ID,
                TA.ATO_ANTERIOR_ORIGEM,
                TA.ATO_ANTERIOR_LIVRO,
                TA.ATO_ANTERIOR_FINICIAL,
                TA.ATO_ANTERIOR_TB_CARTORIO_ID,
                TA.ATO_ANTERIOR_OUTORGANTE,
                TA.ATO_ANTERIOR_OBSERVACAO,
                TA.ATO_ANTERIOR_ATO_ID,
                TA.ATO_ANTERIOR_DATA,
                TA.ATO_ANTERIOR_ANOTACAO_ADICIONAL,
                TA.ATO_ANTERIOR_ATO_TIPO_ID,
                TAT.DESCRICAO AS T_ATO_TIPO_DESCRICAO,
                TA.ATO_ANTERIOR_VALOR_DOCUMENTO
            FROM T_ATO TA
            JOIN T_ATO_TIPO TAT ON TA.ATO_ANTERIOR_ATO_TIPO_ID = TAT.ATO_TIPO_ID
            WHERE TA.ATO_ID = :ato_id
            ORDER BY TA.ATO_ID DESC
        """

        params = {"ato_id": t_ato_id_schema.ato_id}
        return self.fetch_one(sql, params)
