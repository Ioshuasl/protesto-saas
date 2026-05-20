from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.t_biometria_pessoa_schema import (
    TBiometriaPessoaIdSchema,
)


class TBiometriaPessoaDeleteRepository(BaseRepository):


    def execute(self, t_biometria_pessoa_id_schema: TBiometriaPessoaIdSchema):

        try:
            # Montagem do SQL
            sql = """
                DELETE FROM T_BIOMETRIA_PESSOA TBP
                WHERE TBP.BIOMETRIA_PESSOA_ID = :biometria_pessoa_id
                RETURNING TBP.BIOMETRIA_PESSOA_ID
            """

            # Preenchimento dos parâmetros
            params = {
                "biometria_pessoa_id": t_biometria_pessoa_id_schema.biometria_pessoa_id
            }

            # Execução da instrução SQL
            response = self.run_and_return(sql, params)

            # Retorna o resultado da exclusão
            return response

        except Exception as e:
            # Lança exceção HTTP em caso de erro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir registro de T_BIOMETRIA_PESSOA: {e}",
            )
