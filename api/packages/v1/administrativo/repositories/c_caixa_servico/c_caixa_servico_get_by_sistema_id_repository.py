from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.c_caixa_servico_schema import CCaixaServicoSistemaIdSchema

class ShowSistemaIdRepository(BaseRepository):

    def execute(self, caixa_servico_schema : CCaixaServicoSistemaIdSchema):
        
        # Montagem do sql
        sql = """ SELECT * FROM C_CAIXA_SERVICO ccs WHERE ccs.sistema_id = :sistema_id ORDER BY ccs.descricao ASC"""

        # Preenchimento de parâmetros
        params = {
            'sistema_id' : caixa_servico_schema.sistema_id
        }

        # Execução do sql
        return self.fetch_all(sql, params)