from abstracts.repository import BaseRepository
from actions.data.prepare_update_data import prepare_update_data
from fastapi import HTTPException, status

from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoUpdateSchema


class TAtoUpdateRepository(BaseRepository):
    """
    Repositório responsável pela operação de atualização de registros
    na tabela T_ATO.
    """

    def execute(self, t_ato_update_schema: TAtoUpdateSchema, connection=None):
        """
        Atualiza um registro existente na tabela T_ATO.

        Args:
            t_ato_update_schema (TAtoUpdateSchema):
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
                t_ato_update_schema,
                exclude_fields=["ato_id"],
                id_field="ato_id",
            )

            # ----------------------------------------------------
            # Montagem do SQL dinâmico
            # ----------------------------------------------------
            sql = f"""
                UPDATE T_ATO
                SET {update_columns}
                WHERE ATO_ID = :ato_id
                RETURNING *;
            """

            # ----------------------------------------------------
            # Execução e retorno do registro atualizado
            # ----------------------------------------------------
            response = self.run_and_return(sql, params, connection=connection)
            return response

        except Exception as e:
            # ----------------------------------------------------
            # Tratamento de exceção e retorno HTTP padronizado
            # ----------------------------------------------------
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar registro em T_ATO: {str(e)}",
            )
