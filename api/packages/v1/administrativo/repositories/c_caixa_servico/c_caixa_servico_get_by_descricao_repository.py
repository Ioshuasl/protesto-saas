from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.c_caixa_servico_schema import CCaixaServicoDescricaoSchema

class ShowRepository(BaseRepository):

    def execute(self, caixa_servico_schema : CCaixaServicoDescricaoSchema):
        
        # Montagem do sql
        sql = """ SELECT * FROM C_CAIXA_SERVICO ccs WHERE ccs.descricao = :descricao """

        # Preenchimento de parâmetros
        params = {
            'descricao' : caixa_servico_schema.descricao
        }

        # Execução do sql
        return self.fetch_one(sql, params)