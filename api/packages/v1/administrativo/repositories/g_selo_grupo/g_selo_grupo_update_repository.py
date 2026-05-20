from abstracts.repository import BaseRepository
from actions.data.prepare_update_data import prepare_update_data
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_selo_grupo_schema import (
    GSeloGrupoUpdateSchema,
)


class GSeloGrupoUpdateRepository(BaseRepository):
    """
    Repositório responsável pela operação de atualização de registros
    na tabela G_SELO_GRUPO.
    """

    def execute(self, g_selo_grupo_update_schema: GSeloGrupoUpdateSchema):
        """
        Atualiza um registro existente na tabela G_SELO_GRUPO.

        Args:
            g_selo_grupo_update_schema (GSeloGrupoUpdateSchema):
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
                g_selo_grupo_update_schema,
                exclude_fields=["selo_grupo_id"],
                id_field="selo_grupo_id",
            )

            # ----------------------------------------------------
            # Montagem do SQL dinâmico
            # ----------------------------------------------------
            sql = f"""
                UPDATE G_SELO_GRUPO
                SET {update_columns}
                WHERE SELO_GRUPO_ID = :selo_grupo_id
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
                detail=f"Erro ao atualizar registro em G_SELO_GRUPO: {str(e)}",
            )
