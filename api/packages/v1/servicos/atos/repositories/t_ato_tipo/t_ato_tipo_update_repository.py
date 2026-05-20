from abstracts.repository import BaseRepository
from actions.data.prepare_update_data import prepare_update_data
from fastapi import HTTPException, status

from packages.v1.servicos.atos.schemas.t_ato_tipo_schema import (
    TAtoTipoUpdateSchema,
)


class TAtoTipoUpdateRepository(BaseRepository):
    """
    Repositório responsável pela operação de atualização de registros
    na tabela T_ATO_TIPO.
    """

    def execute(self, t_ato_tipo_update_schema: TAtoTipoUpdateSchema):
        """
        Atualiza um registro existente na tabela T_ATO_TIPO.

        Args:
            t_ato_tipo_update_schema (TAtoTipoUpdateSchema):
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
                t_ato_tipo_update_schema,
                exclude_fields=["ato_tipo_id"],
                id_field="ato_tipo_id",
            )

            # ----------------------------------------------------
            # Montagem do SQL dinâmico
            # ----------------------------------------------------
            sql = f"""
                UPDATE T_ATO_TIPO
                SET {update_columns}
                WHERE ATO_TIPO_ID = :ato_tipo_id
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
                detail=f"Erro ao atualizar registro em T_ATO_TIPO: {str(e)}",
            )
