from abstracts.repository import BaseRepository

from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoClearTextoAssinaturaSchema


class TAtoClearTextoAssinaturaRepository(BaseRepository):
    def execute(self, data: TAtoClearTextoAssinaturaSchema):
        sql = f"""
            UPDATE T_ATO TA
            SET TA.{data.coluna} = NULL
            WHERE TA.ATO_ID = :ato_id
            RETURNING TA.ATO_ID, TA.{data.coluna} as texto_assinatura
        """

        params = {"ato_id": data.ato_id}
        return self.run_and_return(sql, params)
