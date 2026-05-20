from abstracts.repository import BaseRepository
from actions.data.prepare_update_data import prepare_update_data
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.t_livro_andamento_schema import (
    TLivroAndamentoUpdateSchema,
)


class TLivroAndamentoUpdateRepository(BaseRepository):
    """Repository to update T_LIVRO_ANDAMENTO rows."""

    def execute(self, schema: TLivroAndamentoUpdateSchema, connection=None):
        try:
            params, update_columns = prepare_update_data(
                schema,
                exclude_fields=["livro_andamento_id"],
                id_field="livro_andamento_id",
            )

            if not update_columns:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Nenhum campo informado para atualizar T_LIVRO_ANDAMENTO.",
                )

            sql = f"""
                UPDATE T_LIVRO_ANDAMENTO
                SET {update_columns}
                WHERE LIVRO_ANDAMENTO_ID = :livro_andamento_id
                RETURNING *;
            """

            return self.run_and_return(sql, params, connection=connection)
        except HTTPException:
            raise
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar registro de T_LIVRO_ANDAMENTO: {error}",
            )
