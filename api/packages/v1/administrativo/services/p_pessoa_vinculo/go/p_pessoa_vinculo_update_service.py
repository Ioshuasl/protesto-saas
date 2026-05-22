from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_pessoa.p_pessoa_show_action import (
    ShowAction as PessoaShowAction,
)
from packages.v1.administrativo.actions.p_pessoa_vinculo.p_pessoa_vinculo_show_action import (
    ShowAction,
)
from packages.v1.administrativo.actions.p_pessoa_vinculo.p_pessoa_vinculo_update_action import (
    UpdateAction,
)
from packages.v1.administrativo.model.p_titulo import get_p_titulo_model
from packages.v1.administrativo.schemas.p_pessoa_schema import PPessoaIdSchema
from packages.v1.administrativo.schemas.p_pessoa_vinculo_schema import (
    PPessoaVinculoIdSchema,
    PPessoaVinculoUpdateSchema,
)


class UpdateService:
    @staticmethod
    def _row_value(row, key: str):
        if row is None:
            return None
        lower = key.lower()
        return row.get(lower) or row.get(key) or row.get(key.upper())

    def _ensure_titulo_exists(self, titulo_id: int) -> None:
        row = get_p_titulo_model().findByPk(titulo_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=[
                    {
                        "input": "titulo_id",
                        "message": "Título não encontrado.",
                    }
                ],
            )

    def _ensure_pessoa_exists(self, pessoa_id: int) -> None:
        row = PessoaShowAction().execute(PPessoaIdSchema(pessoa_id=pessoa_id))
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=[
                    {
                        "input": "pessoa_id",
                        "message": "Pessoa não encontrada.",
                    }
                ],
            )

    def execute(self, pessoa_vinculo_id: int, vinculo_schema: PPessoaVinculoUpdateSchema):
        current = ShowAction().execute(
            PPessoaVinculoIdSchema(pessoa_vinculo_id=pessoa_vinculo_id)
        )
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o vínculo de pessoa.",
            )

        titulo_id = (
            vinculo_schema.titulo_id
            if vinculo_schema.titulo_id is not None
            else self._row_value(current, "titulo_id")
        )
        if titulo_id is not None:
            self._ensure_titulo_exists(int(titulo_id))

        pessoa_id = (
            vinculo_schema.pessoa_id
            if vinculo_schema.pessoa_id is not None
            else self._row_value(current, "pessoa_id")
        )
        if pessoa_id is not None:
            self._ensure_pessoa_exists(int(pessoa_id))

        return UpdateAction().execute(pessoa_vinculo_id, vinculo_schema)
