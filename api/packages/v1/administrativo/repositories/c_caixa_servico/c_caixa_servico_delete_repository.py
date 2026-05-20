from packages.v1.administrativo.schemas.c_caixa_servico_schema import (
    CCaixaServicoIdSchema,
)
from abstracts.repository import BaseRepository
from fastapi import HTTPException, status


class DeleteRepository(BaseRepository):

    def execute(self, caixa_servico_schema: CCaixaServicoIdSchema):

        try:

            # Montagem do sql
            sql = """ DELETE FROM c_caixa_servico ccs 
                      WHERE ccs.caixa_servico_id = :caixa_servico_id 
                      RETURNING ccs.caixa_servico_id"""

            # Preenchimento de parâmetros
            params = {"caixa_servico_id": caixa_servico_schema.caixa_servico_id}

            # Execução do sql
            response = self.run_and_return(sql, params)

            # Retorna o resultado
            return response

        except Exception as e:

            # Informa que houve  uma falha na atualização do usuário
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir C_CAIXA_SERVICO: {e}",
            )
