from abstracts.repository import BaseRepository
from actions.data.prepare_update_data import prepare_update_data
from packages.v1.administrativo.schemas.g_marcacao_tipo_schema import (
    GMarcacaoTipoUpdateSchema,
)
from fastapi import HTTPException, status


class GMarcacaoTipoUpdateRepository(BaseRepository):
    """
    Repositório para a operação de atualização na tabela G_MARCACAO_TIPO.
    """

    def execute(self, data: GMarcacaoTipoUpdateSchema):

        try:

            params, update_columns = prepare_update_data(
                data,
                exclude_fields=["marcacao_tipo_id"],
                id_field="marcacao_tipo_id",
            )

            sql = f"""
                    UPDATE G_MARCACAO_TIPO
                    SET {update_columns}
                    WHERE marcacao_tipo_id = :marcacao_tipo_id
                    RETURNING marcacao_tipo_id
                """

            # Executa o update
            response = self.run_and_return(sql, params)

            return response

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar registro: {e}",
            )
