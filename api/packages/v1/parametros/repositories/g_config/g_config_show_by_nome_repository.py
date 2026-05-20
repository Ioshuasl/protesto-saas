from abstracts.repository import BaseRepository
from packages.v1.parametros.schemas.g_config_schema import (
    GConfigNomeSchema,
    GConfigResponseSchema,
)


class GConfigShowByNomeRepository(BaseRepository):

    def execute(self, g_config_nome_schema: GConfigNomeSchema) -> GConfigResponseSchema:

        # Montagem da consulta sql
        sql = """ SELECT
                    FIRST 1 GC.*
                  FROM G_CONFIG GC
                  JOIN G_CONFIG_GRUPO GCG ON GC.CONFIG_GRUPO_ID = GCG.CONFIG_GRUPO_ID
                  WHERE GC.NOME LIKE :nome
                  AND GCG.SISTEMA_ID = :sistema_id
              """

        # Preenchimento dos parâmetros
        params = {
            "nome": g_config_nome_schema.nome,
            "sistema_id": g_config_nome_schema.sistema_id,
        }

        # Execução do sql
        response = self.fetch_one(sql, params)

        # Transforma em dict associativo
        return response
