from abstracts.repository import BaseRepository
from actions.data.prepare_update_data import prepare_update_data
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_ibge_pais_schema import (
    GIbgePaisUpdateSchema,
)


class GIbgePaisUpdateRepository(BaseRepository):
    """
    Repositório responsável pela operação de atualização de registros
    na tabela G_IBGE_PAIS.
    """

    def execute(self, g_ibge_pais_update_schema: GIbgePaisUpdateSchema):
        """
        Atualiza um registro existente na tabela G_IBGE_PAIS.

        Args:
            g_ibge_pais_update_schema (GIbgePaisUpdateSchema):
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
                g_ibge_pais_update_schema,
                exclude_fields=["g_ibge_pais_id"],
                id_field="g_ibge_pais_id",
            )

            # ----------------------------------------------------
            # Montagem do SQL dinâmico
            # ----------------------------------------------------
            sql = f"""
                UPDATE G_IBGE_PAIS
                SET {update_columns}
                WHERE G_IBGE_PAIS_ID = :g_ibge_pais_id
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
                detail=f"Erro ao atualizar registro em G_IBGE_PAIS: {str(e)}",
            )
