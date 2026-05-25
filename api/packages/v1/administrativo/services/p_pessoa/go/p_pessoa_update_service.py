from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_pessoa.p_pessoa_show_action import ShowAction
from packages.v1.administrativo.actions.p_pessoa.p_pessoa_update_action import UpdateAction
from packages.v1.administrativo.schemas.p_pessoa_schema import (
    PPessoaIdSchema,
    PPessoaUpdateSchema,
)


class UpdateService:
    def execute(self, pessoa_id: int, pessoa_schema: PPessoaUpdateSchema):
        current = ShowAction().execute(PPessoaIdSchema(pessoa_id=pessoa_id))
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar a pessoa.",
            )

        return UpdateAction().execute(pessoa_id, pessoa_schema)
