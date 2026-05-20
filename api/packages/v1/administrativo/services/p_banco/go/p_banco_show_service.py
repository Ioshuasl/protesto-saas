from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_banco.p_banco_show_action import ShowAction
from packages.v1.administrativo.schemas.p_banco_schema import PBancoIdSchema


class ShowService:
    def execute(self, banco_schema: PBancoIdSchema):
        data = ShowAction().execute(banco_schema)

        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o banco.",
            )

        return data
