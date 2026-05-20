from abstracts.repository import BaseRepository
from actions.data.prepare_update_data import prepare_update_data
from fastapi import HTTPException, status

from packages.v1.servicos.atos.schemas.t_ato_parteimovel_schema import (
    TAtoParteImovelUpdateSchema,
)


class TAtoParteImovelUpdateRepository(BaseRepository):
    """
    Repositório responsável pela operação de atualização de registros
    na tabela T_ATO_PARTEIMOVEL.
    """

    def execute(self, t_ato_parteimovel_update_schema: TAtoParteImovelUpdateSchema):
        """
        Atualiza um registro existente na tabela T_ATO_PARTEIMOVEL.

        Args:
            t_ato_parteimovel_update_schema (TAtoParteImovelUpdateSchema):
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
                t_ato_parteimovel_update_schema,
                exclude_fields=["ato_parteimovel_id", "usuario_id"],
                id_field="ato_parteimovel_id",
            )

            # ----------------------------------------------------
            # Montagem do SQL dinâmico
            # ----------------------------------------------------
            sql = f"""
                UPDATE T_ATO_PARTEIMOVEL
                SET {update_columns}
                WHERE ATO_PARTEIMOVEL_ID = :ato_parteimovel_id
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
                detail=f"Erro ao atualizar registro em T_ATO_PARTEIMOVEL: {str(e)}",
            )
