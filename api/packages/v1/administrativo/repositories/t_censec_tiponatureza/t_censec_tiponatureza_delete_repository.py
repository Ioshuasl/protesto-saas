from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.t_censec_tiponatureza_schema import (
    TCensecTipoNaturezaIdSchema,
)


class TCensecTipoNaturezaDeleteRepository(BaseRepository):
    
    def execute(self, t_censec_tiponatureza_id_schema: TCensecTipoNaturezaIdSchema):
       
        try:
            # Montagem do SQL
            sql = """
                    DELETE FROM T_CENSEC_TIPONATUREZA TCT
                    WHERE TCT.CENSEC_TIPONATUREZA_ID = :censec_tiponatureza_id
                    RETURNING TCT.CENSEC_TIPONATUREZA_ID
                  """

            # Preenchimento dos parâmetros
            params = t_censec_tiponatureza_id_schema.model_dump(exclude_unset=True)

            # Execução da instrução SQL
            response = self.run_and_return(sql, params)

            # Retorna o resultado da exclusão
            return response

        except Exception as e:
            # Lança exceção HTTP em caso de erro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir registro de T_CENSEC_TIPONATUREZA: {e}",
            )
