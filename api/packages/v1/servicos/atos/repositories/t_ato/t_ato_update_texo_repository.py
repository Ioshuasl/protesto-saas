from abstracts.repository import BaseRepository
from packages.v1.docx.services.docx_save_service import TAtoTextoFinalizacaoUpdateSchema


class TAtoUpdateTextoRepository(BaseRepository):
    """
    Repositório responsável pela operação de atualização de registros
    na tabela T_ATO.
    """
    def execute(self, data: TAtoTextoFinalizacaoUpdateSchema):

        sql = f""" UPDATE T_ATO TA SET TA.TEXTO = :texto WHERE ATO_ID = :ato_id RETURNING *;"""

        params = {
            "ato_id": data.ato_id,
            "texto": data.texto
        }

        response = self.run_and_return(sql, params)

        return response
