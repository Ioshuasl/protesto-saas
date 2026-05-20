from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoIdSchema


class TAtoCancelarAtoRepository(BaseRepository):
    """
    Cancela o ato: SITUACAO_ATO = 4 (Cancelado), DATA_CANCELAMENTO = agora.
    Não altera se já estiver cancelado.
    """

    def execute(self, t_ato_id_schema: TAtoIdSchema):
        try:
            sql = """
                UPDATE T_ATO
                SET SITUACAO_ATO = '4',
                    DATA_CANCELAMENTO = CURRENT_TIMESTAMP
                WHERE ATO_ID = :ato_id
                  AND (SITUACAO_ATO IS NULL OR SITUACAO_ATO <> '4')
                RETURNING ATO_ID AS ato_id
            """
            params = {"ato_id": t_ato_id_schema.ato_id}
            return self.run_and_return(sql, params)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao cancelar o ato: {e}",
            )
