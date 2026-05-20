from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from abstracts.repository import BaseRepository


class Save(BaseRepository):

    def execute(self, sequencia_schema : GSequenciaSchema):
        
        # Construção do sql
        sql = """  UPDATE G_SEQUENCIA 
                    SET SEQUENCIA = :sequencia 
                    WHERE TABELA LIKE :tabela 
                    RETURNING TABELA, SEQUENCIA """

        # Preenchimento de parâmetros
        params = {
            "sequencia": sequencia_schema.sequencia,
            "tabela": sequencia_schema.tabela
        }

        # Execução do sql
        response = self.run_and_return(sql, params)

        # Retorna como verdadeiro se for salvo com sucesso
        return response