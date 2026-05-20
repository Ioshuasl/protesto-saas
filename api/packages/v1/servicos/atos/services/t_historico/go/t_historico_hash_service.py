from fastapi import HTTPException, status

from actions.data.sha_256_crypt import Sha256Crypt
from packages.v1.servicos.atos.actions.t_historico.t_historico_hash_action import (
    THistoricoHashAction,
)
from packages.v1.servicos.atos.schemas.t_historico_schema import THistoricoHashSchema


class THistoricoHashService:
    def execute(self, data: THistoricoHashSchema):
        data.hash = Sha256Crypt.execute(data.hash_input)
        result = THistoricoHashAction().execute(data)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nenhum historico localizado para o hash informado",
            )

        return result
