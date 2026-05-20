from abstracts.repository import BaseRepository
from actions.data.prepare_update_data import prepare_update_data
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_natureza_titulo_schema import (
    GNaturezaTituloUpdateSchema,
)


class GNaturezaTituloUpdateRepository(BaseRepository):
    """
    Repositório responsável pela operação de atualização de registros
    na tabela G_NATUREZA_TITULO.
    """

    def execute(self, g_natureza_titulo_update_schema: GNaturezaTituloUpdateSchema):
        """
        Atualiza um registro existente na tabela G_NATUREZA_TITULO.

        Args:
            g_natureza_titulo_update_schema (GNaturezaTituloUpdateSchema):
                Esquema contendo os dados a serem atualizados.

        Returns:
            O registro atualizado (via RETURNING *).

        Raises:
            HTTPException: Caso ocorra um erro na execução do SQL.
        """
        try:
            # ----------------------------------------------------
            # Prepara parâmetros e colunas de atualização dinâmicas
            # ----------------------------------------------------
            params, update_columns = prepare_update_data(
                g_natureza_titulo_update_schema,
                exclude_fields=["natureza_titulo_id"],
                id_field="natureza_titulo_id",
            )

            # ----------------------------------------------------
            # Montagem do SQL dinâmico
            # ----------------------------------------------------
            sql = f"""
                UPDATE G_NATUREZA_TITULO
                SET {update_columns}
                WHERE NATUREZA_TITULO_ID = :natureza_titulo_id
                RETURNING *;
            """

            # ----------------------------------------------------
            # Execução e retorno do registro atualizado
            # ----------------------------------------------------
            response = self.run_and_return(sql, params)
            return response

        except Exception as e:
            # ----------------------------------------------------
            # Tratamento de exceção e retorno HTTP padronizado
            # ----------------------------------------------------
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar registro em G_NATUREZA_TITULO: {str(e)}",
            )
