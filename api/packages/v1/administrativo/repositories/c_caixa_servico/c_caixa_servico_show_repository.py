from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.c_caixa_servico_schema import CCaixaServicoIdSchema

class ShowRepository(BaseRepository):

    def execute(self, caixa_servico_schema : CCaixaServicoIdSchema):
        
        # Montagem do sql
        sql = """ SELECT * FROM C_CAIXA_SERVICO ccs WHERE ccs.caixa_servico_id = :caixa_servico_id """

        # Preenchimento de parâmetros
        params = {
            'caixa_servico_id' : caixa_servico_schema.caixa_servico_id
        }

        # Execução do sql
        return self.fetch_one(sql, params)