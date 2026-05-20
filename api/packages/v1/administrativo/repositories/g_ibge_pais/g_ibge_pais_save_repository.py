from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from actions.data.generate_insert_sql import generate_insert_sql
from packages.v1.administrativo.schemas.g_ibge_pais_schema import (
    GIbgePaisSaveSchema,
)


class GIbgePaisSaveRepository(BaseRepository):
    """
    Repositório responsável pela operação de salvamento de um novo registro
    na tabela G_IBGE_PAIS.
    """

    def execute(self, g_ibge_pais_save_schema: GIbgePaisSaveSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            g_ibge_pais_save_schema (GIbgePaisSaveSchema):
                O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:
            # ----------------------------------------------------
            # Preenchimento dos parâmetros
            # ----------------------------------------------------
            params = g_ibge_pais_save_schema.model_dump(exclude_unset=True)

            # ----------------------------------------------------
            # Montagem do SQL dinâmico
            # ----------------------------------------------------
            sql = generate_insert_sql("G_IBGE_PAIS", params)

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
                detail=f"Erro ao salvar registro em G_IBGE_PAIS: {e}",
            )
