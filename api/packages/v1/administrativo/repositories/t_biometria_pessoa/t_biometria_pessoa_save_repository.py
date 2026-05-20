from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from actions.data.generate_insert_sql import generate_insert_sql
from packages.v1.administrativo.schemas.t_biometria_pessoa_schema import (
    TBiometriaPessoaSaveSchema,
)


class TBiometriaPessoaSaveRepository(BaseRepository):
    """
    Repositório responsável pela operação de salvamento de um novo registro
    na tabela G_GRAMATICA.
    """

    def execute(self, data: TBiometriaPessoaSaveSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            t_biometria_pessoa_save_schema (TBiometriaPessoaSchema): O esquema com os dados a serem salvos.

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
            sql = generate_insert_sql("T_BIOMETRIA_PESSOA", params)

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
                detail=f"Erro ao salvar registro em T_BIOMETRIA_PESSOA: {e}",
            )
