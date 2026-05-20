from abstracts.repository import BaseRepository
from actions.data.prepare_update_data import prepare_update_data
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_selo_livro_schema import GSeloLivroUpdateSchema


class GSeloLivroUpdateRepository(BaseRepository):
    def execute(self, data: GSeloLivroUpdateSchema, connection=None):
        try:
            params, update_columns = prepare_update_data(
                data,
                exclude_fields=["selo_livro_id"],
                id_field="selo_livro_id",
            )

            sql = f"""
                UPDATE G_SELO_LIVRO
                SET {update_columns}
                WHERE SELO_LIVRO_ID = :selo_livro_id
                RETURNING *;
            """

            return self.run_and_return(sql, params, connection=connection)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar registro em G_SELO_LIVRO: {e}",
            )
