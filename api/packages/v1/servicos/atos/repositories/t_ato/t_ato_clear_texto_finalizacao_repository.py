from abstracts.repository import BaseRepository

from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoClearTextoFinalizacaoSchema


class TAtoClearTextoFinalizacaoRepository(BaseRepository):
    def execute(self, data: TAtoClearTextoFinalizacaoSchema):
        sql = f"""
            UPDATE T_ATO TA
            SET TA.{data.coluna} = NULL
            WHERE TA.ATO_ID = :ato_id
            RETURNING TA.ATO_ID, TA.{data.coluna} as texto_finalizacao
        """
        params = {"ato_id": data.ato_id}
        return self.run_and_return(sql, params)
