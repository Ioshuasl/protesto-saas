from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_tb_txmodelogrupo_schema import GTbTxmodelogrupoDescricaoSchema

class GetByDescricaoRepository(BaseRepository):

    def execute(self, txmodelogrupo_schema: GTbTxmodelogrupoDescricaoSchema):

        # Montagem do sql
        sql = """ SELECT * FROM G_TB_TXMODELOGRUPO WHERE DESCRICAO = :descricao """

        # Preenchimento de parâmetros
        params = {
            'descricao': txmodelogrupo_schema.descricao
        }

        # Execução do sql
        return self.fetch_one(sql, params)