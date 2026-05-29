from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_banco.p_banco_show_by_codigo_action import (
    ShowByCodigoAction,
)
from packages.v1.administrativo.schemas.p_banco_schema import PBancoCodigoSchema


class ShowByCodigoService:
    def execute(self, codigo_schema: PBancoCodigoSchema):
        data = ShowByCodigoAction().execute(codigo_schema)

        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o banco para o código informado.",
            )

        return data
