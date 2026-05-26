from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_certidao.p_certidao_cancelar_action import (
    CancelarAction,
)
from packages.v1.administrativo.actions.p_certidao.p_certidao_show_action import (
    ShowAction,
)
from packages.v1.administrativo.schemas.p_certidao_schema import PCertidaoIdSchema


class CancelarService:
    def execute(self, certidao_schema: PCertidaoIdSchema):
        certidao = ShowAction().execute(certidao_schema)
        if (certidao.get("status") or "").strip().upper() != "A":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Apenas certidões ativas podem ser canceladas.",
            )

        return CancelarAction().execute(certidao_schema)
