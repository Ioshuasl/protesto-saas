from typing import Any, Optional

from abstracts.repository import BaseRepository
from actions.data.prepare_update_data import prepare_update_data
from fastapi import HTTPException, status

from packages.v1.servicos.atos.schemas.t_ato_vinculoparte_schema import (
    TAtoVinculoParteUpdateSchema,
)

class TAtoVinculoParteUpdateRepository(BaseRepository):
    """
    Repositório responsável pela operação de atualização de registros
    na tabela T_ATO_VINCULOPARTE.
    """

    def execute(self, t_ato_vinculoparte_update_schema: TAtoVinculoParteUpdateSchema):
        """
        Atualiza um registro existente na tabela T_ATO_VINCULOPARTE.

        Args:
            t_ato_vinculoparte_update_schema (TAtoVinculoParteUpdateSchema):
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
                t_ato_vinculoparte_update_schema,
                exclude_fields=["ato_vinculoparte_id"],
                id_field="ato_vinculoparte_id",
            )

            # ----------------------------------------------------
            # Montagem do SQL dinâmico
            # ----------------------------------------------------
            sql = f""" UPDATE T_ATO_VINCULOPARTE SET {update_columns} WHERE ATO_VINCULOPARTE_ID = :ato_vinculoparte_id RETURNING ATO_ID, ATO_VINCULOPARTE_ID;"""

            return self.run_and_return(sql, params)

        except Exception as e:
            # ----------------------------------------------------
            # Tratamento de exceção e retorno HTTP padronizado
            # ----------------------------------------------------
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar registro em T_ATO_VINCULOPARTE: {str(e)}",
            )
