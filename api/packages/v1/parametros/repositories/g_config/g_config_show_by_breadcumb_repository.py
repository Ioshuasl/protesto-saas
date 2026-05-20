from abstracts.repository import BaseRepository
from packages.v1.parametros.schemas.g_config_schema import (
    GConfigResponseSchema,
    GConfigShowByBreadcumbSchema,
)


class GConfigShowByBreadcumbRepository(BaseRepository):

    def execute(self, data: GConfigShowByBreadcumbSchema) -> GConfigResponseSchema:

        # Montagem da consulta sql
        sql = """ SELECT
                        GC.*
                    FROM
                        G_CONFIG GC
                    JOIN G_CONFIG_GRUPO GCG ON
                        GC.CONFIG_GRUPO_ID = GCG.CONFIG_GRUPO_ID
                    JOIN G_SISTEMA GS ON
                        GCG.SISTEMA_ID = GS.SISTEMA_ID
                    WHERE
                        GS.SISTEMA_ID = :sistema_id
                        AND
                            GC.NOME LIKE :nome
                        AND
                            GC.SECAO LIKE :secao
                        AND
                            GCG.DESCRICAO LIKE :descricao
              """

        # Preenchimento dos parâmetros
        params = {
            "nome": data.nome,
            "secao": data.secao,
            "descricao": data.grupo_descricao,
            "sistema_id": data.sistema_id,
        }

        # Execução do sql
        response = self.fetch_one(sql, params)

        # Transforma em dict associativo
        return response
