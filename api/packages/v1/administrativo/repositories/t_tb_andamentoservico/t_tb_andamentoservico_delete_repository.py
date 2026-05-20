from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_tb_andamentoservico_schema import TTbAndamentoservicoIdSchema
from fastapi import HTTPException, status


class DeleteRepository(BaseRepository):

    def execute(self, andamentoservico_schema: TTbAndamentoservicoIdSchema):

        try:
            # Montagem do sql
            sql = """ 
                    DELETE FROM T_TB_ANDAMENTOSERVICO 
                    WHERE TB_ANDAMENTOSERVICO_ID = :tb_andamentoservico_id 
                    RETURNING TB_ANDAMENTOSERVICO_ID
                """

            # Preenchimento de parâmetros
            params = {
                "tb_andamentoservico_id": andamentoservico_schema.tb_andamentoservico_id
            }

            # Execução do sql
            response = self.run_and_return(sql, params)

            # Retorna o resultado
            return response
    
        except Exception as e:
            # Informa que houve uma falha na exclusão
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir T_TB_ANDAMENTOSERVICO: {e}"
            )