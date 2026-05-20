from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_marcacao_tipo_schema import (
    GMarcacaoTipoIdSchema,
)
from fastapi import HTTPException, status


class GMarcacaoTipoShowRepository(BaseRepository):

    def execute(self, marcacao_tipo_schema: GMarcacaoTipoIdSchema):

        # Montagem do SQL
        sql = "SELECT * FROM G_MARCACAO_TIPO WHERE MARCACAO_TIPO_ID = :marcacao_tipo_id"

        # Preenchimento de parâmetros
        params = {"marcacao_tipo_id": marcacao_tipo_schema.marcacao_tipo_id}

        # Execução do SQL
        result = self.fetch_one(sql, params)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro de G_MARCACAO_TIPO não encontrado",
            )

        return result
