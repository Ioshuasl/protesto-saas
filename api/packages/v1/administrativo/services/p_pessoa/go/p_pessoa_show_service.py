from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_pessoa.p_pessoa_show_action import ShowAction
from packages.v1.administrativo.schemas.p_pessoa_schema import PPessoaIdSchema


class ShowService:
    def execute(self, pessoa_schema: PPessoaIdSchema):
        data = ShowAction().execute(pessoa_schema)
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar a pessoa.",
            )
        return data
