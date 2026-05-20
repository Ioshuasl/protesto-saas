from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from actions.data.generate_insert_sql import generate_insert_sql
from packages.v1.servicos.atos.schemas.t_historico_schema import (
    THistoricoSaveSchema,
)


class THistoricoSaveRepository(BaseRepository):
    """
    Repositório responsável pela inserção de um novo registro
    na tabela T_HISTORICO.
    """

    def execute(self, data: THistoricoSaveSchema, connection=None):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            t_ato_vinculoparte_save_schema (TAtoVinculoParteSchema): O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:

            # ----------------------------------------------------
            # Preenchimento dos parâmetros
            # ----------------------------------------------------
            params = data.model_dump(exclude_unset=True)

            # ----------------------------------------------------
            # Montagem do SQL dinâmico
            # ----------------------------------------------------
            sql = generate_insert_sql("T_HISTORICO", params)

            # ----------------------------------------------------
            # Execução do SQL e retorno do registro
            # ----------------------------------------------------
            return self.run_and_return(sql, params, connection=connection)

        except Exception as e:
            # ----------------------------------------------------
            # Tratamento de erros e lançamento de exceção HTTP
            # ----------------------------------------------------
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar registro em T_HISTORICO: {e}",
            )
