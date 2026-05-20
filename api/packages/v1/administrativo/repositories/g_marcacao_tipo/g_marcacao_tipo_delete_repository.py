from abstracts.repository import BaseRepository

# O schema TServicoTipoIdSchema deve ser substituído por GMarcacaoTipoIdSchema.
from packages.v1.administrativo.schemas.g_marcacao_tipo_schema import (
    GMarcacaoTipoIdSchema,
)
from fastapi import HTTPException, status


class GMarcacaoTipoDeleteRepository(BaseRepository):

    def execute(self, marcacao_tipo_schema: GMarcacaoTipoIdSchema):

        try:
            # Montagem do sql
            sql = """ DELETE FROM G_MARCACAO_TIPO 
                      WHERE MARCACAO_TIPO_ID = :marcacao_tipo_id 
                      RETURNING MARCACAO_TIPO_ID
                """

            # Preenchimento de parâmetros
            params = {"marcacao_tipo_id": marcacao_tipo_schema.marcacao_tipo_id}

            # Execução do sql
            response = self.run(sql, params)

            # Retorna o resultado
            return response

        except Exception as e:
            # Informa que houve uma falha na exclusão
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir G_MARCACAO_TIPO: {e}",
            )
