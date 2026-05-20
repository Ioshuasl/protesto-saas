from abstracts.repository import BaseRepository

from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoClearTextoSchema


class TAtoClearTextoRepository(BaseRepository):
    def execute(self, data: TAtoClearTextoSchema):
        sql = """
            UPDATE T_ATO TA
            SET TA.TEXTO = NULL
            WHERE TA.ATO_ID = :ato_id
            RETURNING TA.ATO_ID, TA.TEXTO
        """

        params = {"ato_id": data.ato_id}
        return self.run_and_return(sql, params)
