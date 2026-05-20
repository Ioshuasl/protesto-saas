from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_imovel_schema import TImovelIdSchema
from fastapi import HTTPException, status


class TImovelDeleteRepository(BaseRepository):
    
    def execute(self, t_imovel_id_schema: TImovelIdSchema):
       
        try:

            # Montagem do sql
            sql = """ 
                      DELETE FROM T_IMOVEL TI 
                      WHERE TI.IMOVEL_ID = :imovelId 
                      RETURNING TI.IMOVEL_ID
                """

            # Preenchimento de parâmetros
            params = {
                "imovelId": t_imovel_id_schema.imovel_id
            }

            # Execução do sql
            response = self.run_and_return(sql, params)

            # Retorna o resultado
            return response
    
        except Exception as e:
            
            # Informa que houve uma falha na exclusão
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir T_IMOVEL: {e}"
            )