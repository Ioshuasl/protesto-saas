from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_pessoa_schema import TPessoaIdSchema
from fastapi import HTTPException, status


class TPessoaDeleteRepository(BaseRepository):

    def execute(self, t_pessoa_id_schema: TPessoaIdSchema):

        try:
            # Montagem do sql
            sql = """ 
                    DELETE FROM T_PESSOA 
                    WHERE PESSOA_ID = :pessoa_id 
                    RETURNING PESSOA_ID
                  """

            # Preenchimento de parâmetros
            params = {"pessoa_id": t_pessoa_id_schema.pessoa_id}

            # Execução do sql
            response = self.run_and_return(sql, params)

            # Retorna o resultado
            return response

        except Exception as e:
            # Informa que houve uma falha na exclusão
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir T_PESSOA: {e}",
            )
