from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_pessoa_vinculo.p_pessoa_vinculo_show_action import (
    ShowAction,
)
from packages.v1.administrativo.schemas.p_pessoa_vinculo_schema import PPessoaVinculoIdSchema


class ShowService:
    def execute(self, vinculo_schema: PPessoaVinculoIdSchema):
        row = ShowAction().execute(vinculo_schema)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o vínculo de pessoa.",
            )
        return row
