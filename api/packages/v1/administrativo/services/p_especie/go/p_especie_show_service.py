from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_especie.p_especie_show_action import ShowAction
from packages.v1.administrativo.schemas.p_especie_schema import PEspecieIdSchema


class ShowService:
    def execute(self, especie_schema: PEspecieIdSchema):
        data = ShowAction().execute(especie_schema)

        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar a espécie.",
            )

        return data
