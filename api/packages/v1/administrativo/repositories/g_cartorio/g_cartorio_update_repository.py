from abstracts.repository import BaseRepository
from actions.data.prepare_update_data import prepare_update_data
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_cartorio_schema import GCartorioUpdateSchema


class GCartorioUpdateRepository(BaseRepository):
    """
    Repositório responsável pela operação de atualização de registros
    na tabela G_CARTORIO.
    """

    def execute(self, g_cartorio_update_schema: GCartorioUpdateSchema):
        """
        Atualiza um registro existente na tabela G_CARTORIO.

        Args:
            g_cartorio_update_schema (GCartorioUpdateSchema):
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
                g_cartorio_update_schema,
                exclude_fields=["cartorio_id"],
                id_field="cartorio_id",
            )

            # ----------------------------------------------------
            # Montagem do SQL dinâmico
            # ----------------------------------------------------
            sql = f"""
                UPDATE G_CARTORIO
                SET {update_columns}
                WHERE CARTORIO_ID = :cartorio_id
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
                detail=f"Erro ao atualizar registro em G_CARTORIO: {str(e)}",
            )
