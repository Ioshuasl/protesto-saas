from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_imovel_unidade_schema import TImovelUnidadeIdSchema
from fastapi import HTTPException, status

class TImovelUnidadeDeleteRepository(BaseRepository):
    
    def execute(self, t_imovel_unidade_id_schema: TImovelUnidadeIdSchema):
        
        try:
            # Montagem do sql
            sql = """ 
                    DELETE FROM T_IMOVEL_UNIDADE 
                    WHERE IMOVEL_UNIDADE_ID = :imovel_unidade_id 
                    RETURNING IMOVEL_UNIDADE_ID                    
                  """

            # Preenchimento de parâmetros
            params = {
                "imovel_unidade_id": t_imovel_unidade_id_schema.imovel_unidade_id
            }

            # Execução do sql
            response = self.run_and_return(sql, params)

            # Retorna o resultado
            return response
    
        except Exception as e:
            # Informa que houve uma falha na exclusão
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir T_IMOVEL_UNIDADE: {e}"
            )