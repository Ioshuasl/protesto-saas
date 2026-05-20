from abstracts.repository import BaseRepository

from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoTextoAssinaturaUpdateSchema


class TAtoUpdateTextoAssinaturaRepository(BaseRepository):
    """
    Repositorio responsavel pela atualizacao do texto de assinatura em T_ATO.
    """

    def execute(self, data: TAtoTextoAssinaturaUpdateSchema):

        sql = f""" UPDATE T_ATO TA SET TA.{data.coluna} = :texto WHERE ATO_ID = :ato_id RETURNING *;"""

        params = {
            "ato_id": data.ato_id,
            "texto": data.texto,
        }

        response = self.run_and_return(sql, params)

        return response

