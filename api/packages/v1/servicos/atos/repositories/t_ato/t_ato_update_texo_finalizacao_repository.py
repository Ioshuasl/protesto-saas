from abstracts.repository import BaseRepository

from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoTextoFinalizacaoUpdateSchema


class TAtoUpdateTextoFinalizacaoRepository(BaseRepository):
    """
    Repositório responsável pela operação de atualização de registros
    na tabela T_ATO.
    """

    def execute(self, data: TAtoTextoFinalizacaoUpdateSchema):

        # ----------------------------------------------------
        # Montagem do SQL dinâmico
        # ----------------------------------------------------
        sql = f""" UPDATE T_ATO TA SET TA.{data.coluna} = :texto WHERE TA.ATO_ID = :ato_id RETURNING *;"""

        params = {
            "ato_id": data.ato_id,
            "texto": data.texto
        }

        # ----------------------------------------------------
        # Execução e retorno do registro atualizado
        # ----------------------------------------------------
        response = self.run_and_return(sql, params)

        return response
