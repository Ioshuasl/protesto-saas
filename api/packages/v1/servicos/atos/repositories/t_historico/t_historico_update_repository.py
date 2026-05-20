from abstracts.repository import BaseRepository
from actions.data.prepare_update_data import prepare_update_data
from fastapi import HTTPException, status
from packages.v1.servicos.atos.schemas.t_historico_schema import (
    THistoricoUpdateSchema,
)


class THistoricoUpdateRepository(BaseRepository):
    """
    Repositório responsável pela atualização de um registro
    na tabela T_HISTORICO.
    """

    def execute(self, data: THistoricoUpdateSchema):
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
                data,
                exclude_fields=["historico_id"],
                id_field="historico_id",
            )

            # ----------------------------------------------------
            # Montagem do SQL dinâmico
            # ----------------------------------------------------
            sql = f"""
                        UPDATE T_HISTORICO
                        SET {update_columns}
                        WHERE historico_id = :historico_id
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
                detail=f"Erro ao atualizar registro em T_ATO_VINCULOPARTE: {str(e)}",
            )
