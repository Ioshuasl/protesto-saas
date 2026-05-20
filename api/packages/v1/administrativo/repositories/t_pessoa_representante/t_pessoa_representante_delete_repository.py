from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.t_pessoa_representante_schema import (
    TPessoaRepresentanteIdSchema,
)


class TPessoaRepresentanteDeleteRepository(BaseRepository):

    def execute(self, t_pessoa_representante_id_schema: TPessoaRepresentanteIdSchema):

        try:
            # Montagem do sql
            sql = """ 
                    DELETE FROM T_PESSOA_REPRESENTANTE TPR 
                    WHERE TPR.PESSOA_REPRESENTANTE_ID = :pessoaRepresentanteId    
                    RETURNING TPR.PESSOA_REPRESENTANTE_ID                 
                  """

            # Preenchimento de parâmetros
            params = {
                "pessoaRepresentanteId": t_pessoa_representante_id_schema.pessoa_representante_id
            }

            # Execução do sql
            response = self.run_and_return(sql, params)

            # Retorna o resultado
            return response

        except Exception as e:
            # Informa que houve uma falha na exclusão
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir T_PESSOA_REPRESENTANTE: {e}",
            )
