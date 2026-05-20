from abstracts.repository import BaseRepository

from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoSaveMinuta


class TAtoUpdateMinutaRepository(BaseRepository):
    """
    Repositório responsável pela operação de atualização de registros
    na tabela T_ATO.
    """

    def execute(self, data: TAtoSaveMinuta):

        # ----------------------------------------------------
        # Montagem do SQL dinâmico
        # ----------------------------------------------------
        sql = f""" UPDATE T_ATO SET TEXTO = :texto WHERE ATO_ID = :ato_id RETURNING ATO_ID, TEXTO;"""

        params = {
            "ato_id": data.ato_id,
            "texto": data.texto
        }

        # ----------------------------------------------------
        # Execução e retorno do registro atualizado
        # ----------------------------------------------------
        response = self.run_and_return(sql, params)

        return response
