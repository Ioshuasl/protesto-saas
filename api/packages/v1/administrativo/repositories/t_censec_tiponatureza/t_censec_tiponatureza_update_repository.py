from abstracts.repository import BaseRepository
from actions.data.prepare_update_data import prepare_update_data
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.t_censec_tiponatureza_schema import (
    TCensecTipoNaturezaUpdateSchema,
)


class TCensecTipoNaturezaUpdateRepository(BaseRepository):
    """
    Repositório responsável pela operação de atualização de registros
    na tabela T_CENSEC_TIPONATUREZA.
    """

    def execute(
        self, t_censec_tiponatureza_update_schema: TCensecTipoNaturezaUpdateSchema
    ):
        """
        Atualiza um registro existente na tabela T_CENSEC_TIPONATUREZA.

        Args:
            t_censec_tiponatureza_update_schema (TCensecTipoNaturezaUpdateSchema):
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
                t_censec_tiponatureza_update_schema,
                exclude_fields=["censec_tiponatureza_id"],
                id_field="censec_tiponatureza_id",
            )

            # ----------------------------------------------------
            # Montagem do SQL dinâmico
            # ----------------------------------------------------
            sql = f"""
                UPDATE T_CENSEC_TIPONATUREZA
                SET {update_columns}
                WHERE CENSEC_TIPONATUREZA_ID = :censec_tiponatureza_id
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
                detail=f"Erro ao atualizar registro em T_CENSEC_TIPONATUREZA: {str(e)}",
            )
