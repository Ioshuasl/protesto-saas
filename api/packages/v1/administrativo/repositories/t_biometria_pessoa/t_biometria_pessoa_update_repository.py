from abstracts.repository import BaseRepository
from actions.data.prepare_update_data import prepare_update_data
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.t_biometria_pessoa_schema import (
    TBiometriaPessoaUpdateSchema,
)


class TBiometriaPessoaUpdateRepository(BaseRepository):
    """
    Repositório responsável pela operação de atualização de registros
    na tabela T_BIOMETRIA_PESSOA.
    """

    def execute(self, t_biometria_pessoa_update_schema: TBiometriaPessoaUpdateSchema):
        """
        Atualiza um registro existente na tabela T_BIOMETRIA_PESSOA.

        Args:
            t_biometria_pessoa_update_schema (TBiometriaPessoaUpdateSchema):
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
                t_biometria_pessoa_update_schema,
                exclude_fields=["biometria_pessoa_id"],
                id_field="biometria_pessoa_id",
            )

            # ----------------------------------------------------
            # Montagem do SQL dinâmico
            # ----------------------------------------------------
            sql = f"""
                UPDATE T_BIOMETRIA_PESSOA
                SET {update_columns}
                WHERE BIOMETRIA_PESSOA_ID = :biometria_pessoa_id
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
                detail=f"Erro ao atualizar registro em T_BIOMETRIA_PESSOA: {str(e)}",
            )
