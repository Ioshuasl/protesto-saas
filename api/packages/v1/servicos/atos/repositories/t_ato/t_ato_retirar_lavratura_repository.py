from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoIdSchema


class TAtoRetirarLavraturaRepository(BaseRepository):
    """
    Remove marcação de lavratura em T_ATO e retorna para Pré-lavrado (2).
    """

    def execute(self, t_ato_id_schema: TAtoIdSchema):
        try:
            sql = """
                UPDATE T_ATO
                SET DATA_LAVRATURA = NULL,
                    USUARIO_ID_LAVRATURA = NULL,
                    FOLHA_INICIAL = NULL,
                    FOLHA_FINAL = NULL,
                    FOLHA_TOTAL = NULL,
                    LIVRO_ANDAMENTO_ID = NULL,
                    SELO_LIVRO_ID = NULL,
                    SITUACAO_ATO = '2'
                WHERE ATO_ID = :ato_id
                  AND (
                    SITUACAO_ATO = '3'
                    OR DATA_LAVRATURA IS NOT NULL
                    OR USUARIO_ID_LAVRATURA IS NOT NULL
                  )
                RETURNING ATO_ID AS ato_id
            """
            params = {"ato_id": t_ato_id_schema.ato_id}
            return self.run_and_return(sql, params)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao retirar lavratura do ato: {e}",
            )
