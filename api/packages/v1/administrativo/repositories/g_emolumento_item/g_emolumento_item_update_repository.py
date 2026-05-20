from abstracts.repository import BaseRepository
from actions.data.prepare_update_data import prepare_update_data
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_emolumento_item_schema import (
    GEmolumentoItemUpdateSchema,
)


class GEmolumentoItemUpdateRepository(BaseRepository):
    """
    Repositório responsável pela operação de atualização de registros
    na tabela G_EMOLUMENTO_ITEM.
    """

    def execute(self, g_emolumento_item_update_schema: GEmolumentoItemUpdateSchema):
        """
        Atualiza um registro existente na tabela G_EMOLUMENTO_ITEM.

        Args:
            g_emolumento_item_update_schema (GEmolumentoItemUpdateSchema):
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
                g_emolumento_item_update_schema,
                exclude_fields=["emolumento_item_id"],
                id_field="emolumento_item_id",
            )

            # ----------------------------------------------------
            # Montagem do SQL dinâmico
            # ----------------------------------------------------
            sql = f"""
                UPDATE G_EMOLUMENTO_ITEM
                SET {update_columns}
                WHERE EMOLUMENTO_ITEM_ID = :emolumento_item_id
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
                detail=f"Erro ao atualizar registro em G_EMOLUMENTO_ITEM: {str(e)}",
            )
