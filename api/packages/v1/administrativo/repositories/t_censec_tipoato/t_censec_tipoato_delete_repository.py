from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.t_censec_tipoato_schema import (
    TCensecTipoAtoIdSchema,
)


class TCensecTipoAtoDeleteRepository(BaseRepository):
    
    def execute(self, t_censec_tipoato_id_schema: TCensecTipoAtoIdSchema):
       
        try:
            # Montagem do SQL
            sql = """
                    DELETE FROM T_CENSEC_TIPOATO CTA
                    WHERE CTA.CENSEC_TIPOATO_ID = :censec_tipoato_id
                    RETURNING CTA.CENSEC_TIPOATO_ID
                  """

            # Preenchimento dos parâmetros
            params = {"censec_tipoato_id": t_censec_tipoato_id_schema.censec_tipoato_id}

            # Execução da instrução SQL
            response = self.run_and_return(sql, params)

            # Retorna o resultado da exclusão
            return response

        except Exception as e:
            # Lança exceção HTTP em caso de erro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir registro de T_CENSEC_TIPOATO: {e}",
            )
