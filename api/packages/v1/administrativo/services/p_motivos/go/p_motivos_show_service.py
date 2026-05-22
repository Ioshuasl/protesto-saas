from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_motivos.p_motivos_show_action import ShowAction
from packages.v1.administrativo.schemas.p_motivos_schema import PMotivosIdSchema


class ShowService:
    def execute(self, motivos_schema: PMotivosIdSchema):
        data = ShowAction().execute(motivos_schema)

        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o motivo.",
            )

        return data
