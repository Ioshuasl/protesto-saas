from abstracts.repository import BaseRepository
from actions.data.prepare_update_data import prepare_update_data
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.t_censec_tipoato_schema import (
    TCensecTipoAtoUpdateSchema,
)


class TCensecTipoAtoUpdateRepository(BaseRepository):
    """
    Repositório responsável pela operação de atualização de registros
    na tabela T_CENSEC_TIPOATO.
    """

    def execute(self, t_censec_tipoato_update_schema: TCensecTipoAtoUpdateSchema):
        """
        Atualiza um registro existente na tabela T_CENSEC_TIPOATO.

        Args:
            t_censec_tipoato_update_schema (TCensecTipoAtoUpdateSchema):
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
                t_censec_tipoato_update_schema,
                exclude_fields=["censec_tipoato_id"],
                id_field="censec_tipoato_id",
            )

            # ----------------------------------------------------
            # Montagem do SQL dinâmico
            # ----------------------------------------------------
            sql = f"""
                UPDATE T_CENSEC_TIPOATO
                SET {update_columns}
                WHERE CENSEC_TIPOATO_ID = :censec_tipoato_id
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
                detail=f"Erro ao atualizar registro em T_CENSEC_TIPOATO: {str(e)}",
            )
