from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from actions.data.generate_insert_sql import generate_insert_sql
from packages.v1.administrativo.schemas.g_emolumento_periodo_schema import (
    GEmolumentoPeriodoSaveSchema,
)


class GEmolumentoPeriodoSaveRepository(BaseRepository):
    """
    Repositório responsável pela operação de salvamento de um novo registro
    na tabela G_EMOLUMENTO_PERIODO.
    """

    def execute(self, g_emolumento_periodo_save_schema: GEmolumentoPeriodoSaveSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            g_emolumento_periodo_save_schema (GEmolumentoPeriodoSchema): O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:

            # ----------------------------------------------------
            # Preenchimento dos parâmetros
            # ----------------------------------------------------
            params = g_emolumento_periodo_save_schema.model_dump(exclude_unset=True)

            # ----------------------------------------------------
            # Montagem do SQL dinâmico
            # ----------------------------------------------------
            sql = generate_insert_sql("G_EMOLUMENTO_PERIODO", params)

            # ----------------------------------------------------
            # Execução do SQL e retorno do registro
            # ----------------------------------------------------
            return self.run_and_return(sql, params)

        except Exception as e:
            # ----------------------------------------------------
            # Tratamento de erros e lançamento de exceção HTTP
            # ----------------------------------------------------
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar registro em G_EMOLUMENTO_PERIODO: {e}",
            )
