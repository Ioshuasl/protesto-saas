from abstracts.repository import BaseRepository
from actions.data.prepare_update_data import prepare_update_data
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.t_livro_natureza_schema import TLivroNaturezaUpdateSchema


class TLivroNaturezaUpdateRepository(BaseRepository):
    """Repositório para atualizar registros em T_LIVRO_NATUREZA."""

    def execute(self, schema: TLivroNaturezaUpdateSchema):
        try:
            params, update_columns = prepare_update_data(
                schema,
                exclude_fields=["livro_natureza_id"],
                id_field="livro_natureza_id",
            )

            if not update_columns:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Nenhum campo informado para atualizar T_LIVRO_NATUREZA.",
                )

            sql = f"""
                UPDATE T_LIVRO_NATUREZA
                SET {update_columns}
                WHERE LIVRO_NATUREZA_ID = :livro_natureza_id
                RETURNING *;
            """

            response = self.run_and_return(sql, params)
            return response
        except HTTPException:
            raise
        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar registro de T_LIVRO_NATUREZA: {error}",
            )

