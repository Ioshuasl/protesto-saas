from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from packages.v1.parametros.schemas.g_config_schema import GConfigIdSchema


class GConfigShowRepository(BaseRepository):
    def execute(self, data: GConfigIdSchema):
        sql = """
            SELECT
                GC.CONFIG_ID,
                GC.CONFIG_GRUPO_ID,
                GC.CONFIG_PADRAO_ID,
                GC.SECAO,
                GC.NOME,
                GC.VALOR,
                GC.DESCRICAO,
                GC.TERMINAL,
                GC.TIPO_VALOR,
                GC.ATUALIZADO,
                GC.TEXTO
            FROM G_CONFIG GC
            WHERE GC.CONFIG_ID = :config_id
        """

        params = {"config_id": data.config_id}

        result = self.fetch_one(sql, params)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro de G_CONFIG nao encontrado",
            )

        return result
