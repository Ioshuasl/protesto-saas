from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from abstracts.repository import BaseRepository


class Get(BaseRepository):

    def execute(self, sequencia_schema : GSequenciaSchema):

        # Montagem da consulta sql
        sql = """ SELECT FIRST 1 * FROM G_SEQUENCIA gs WHERE gs.TABELA LIKE :tabela """

        # Preenchimento dos parâmetros
        params = {
            "tabela" : sequencia_schema.tabela
        }

        # Execução do sql
        response = self.fetch_one(sql, params)

        # Transforma em dict associativo
        return response