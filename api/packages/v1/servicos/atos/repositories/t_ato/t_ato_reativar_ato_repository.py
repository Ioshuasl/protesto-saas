from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoIdSchema


class TAtoReativarAtoRepository(BaseRepository):
    """
    Reativa o ato cancelado: SITUACAO_ATO = 1 (Montagem), limpa DATA_CANCELAMENTO.
    Só aplica quando a situação atual é Cancelado (4).
    """

    def execute(self, t_ato_id_schema: TAtoIdSchema):
        try:
            sql = """
                UPDATE T_ATO
                SET SITUACAO_ATO = '1',
                    DATA_CANCELAMENTO = NULL
                WHERE ATO_ID = :ato_id
                  AND SITUACAO_ATO = '4'
                RETURNING ATO_ID AS ato_id
            """
            params = {"ato_id": t_ato_id_schema.ato_id}
            return self.run_and_return(sql, params)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao reativar o ato: {e}",
            )
