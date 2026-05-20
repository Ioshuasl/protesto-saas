from abstracts.repository import BaseRepository

from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoTextoFinalizacao

class TAtoGetTextoFinalizacaoRepository(BaseRepository):
    """
    Repositório responsável pela operação de exibição de um registro
    na tabela T_ATO.
    """

    def execute(self, data: TAtoTextoFinalizacao):

        sql = f""" SELECT TA.ATO_ID, TA.{data.coluna} as texto_finalizacao FROM T_ATO TA WHERE TA.ATO_ID = :ato_id """

        params = data.model_dump(exclude_unset=True)

        result = self.fetch_one(sql, params)

        return result
