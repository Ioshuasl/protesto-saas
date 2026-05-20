from abstracts.repository import BaseRepository
from fastapi import HTTPException, status
from packages.v1.administrativo.schemas.t_censec_qualidadeato_schema import (
    TCensecQualidadeAtoIdSchema,
)


class TCensecQualidadeAtoDeleteRepository(BaseRepository):
    
    def execute(self, t_censec_qualidadeato_id_schema: TCensecQualidadeAtoIdSchema):
        
        try:
            
            # Montagem do SQL            
            sql = """
                DELETE FROM T_CENSEC_QUALIDADEATO CQA
                WHERE CQA.CENSEC_QUALIDADEATO_ID = :censec_qualidadeato_id
                RETURNING CQA.CENSEC_QUALIDADEATO_ID           
            """
            
            # Preenchimento dos parâmetros            
            params = {
                "censec_qualidadeato_id": t_censec_qualidadeato_id_schema.censec_qualidadeato_id
            }
            
            # Execução da instrução SQL            
            response = self.run_and_return(sql, params)
            
            # Retorno do resultado            
            return response

        except Exception as e:
            
            # Tratamento de erro e exceção HTTP padronizada
            
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir registro de T_CENSEC_QUALIDADEATO: {e}",
            )
