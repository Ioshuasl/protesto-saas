from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from actions.data.generate_insert_sql import generate_insert_sql
from packages.v1.servicos.atos.schemas.t_ato_vinculovalor_schema import (
    TAtoVinculoValorSaveSchema,
)


class TAtoVinculoValorSaveRepository(BaseRepository):
    """
    Repositório responsável pela operação de salvamento de um novo registro
    na tabela T_ATO_VINCULOVALOR.
    """

    def execute(self, t_ato_vinculovalor_save_schema: TAtoVinculoValorSaveSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            t_ato_vinculovalor_save_schema (TAtoVinculoValorSchema): O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:

            # ----------------------------------------------------
            # Preenchimento dos parâmetros
            # ----------------------------------------------------
            params = t_ato_vinculovalor_save_schema.model_dump(exclude_unset=True)

            # Campo sistema_id é usado apenas em regras de cálculo
            # e não existe na tabela T_ATO_VINCULOVALOR.
            params.pop("sistema_id", None)
            # usuario_id apenas para auditoria / histórico (sem coluna na tabela)
            params.pop("usuario_id", None)

            # ----------------------------------------------------
            # Montagem do SQL dinâmico
            # ----------------------------------------------------
            sql = generate_insert_sql("T_ATO_VINCULOVALOR", params, True)

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
                detail=f"Erro ao salvar registro em T_ATO_VINCULOVALOR: {e}",
            )
