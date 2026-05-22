from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_pessoa.p_pessoa_show_action import ShowAction
from packages.v1.administrativo.actions.p_pessoa.p_pessoa_update_action import UpdateAction
from packages.v1.administrativo.repositories.p_pessoa.p_pessoa_get_by_cpfcnpj_repository import (
    GetByCpfcnpjRepository,
)
from packages.v1.administrativo.schemas.p_pessoa_schema import (
    PPessoaCpfcnpjSchema,
    PPessoaIdSchema,
    PPessoaUpdateSchema,
)


class UpdateService:
    def _ensure_cpfcnpj_unique(
        self, cpfcnpj: str | None, pessoa_id: int
    ):
        if not cpfcnpj:
            return
        duplicate = GetByCpfcnpjRepository().execute(
            PPessoaCpfcnpjSchema(cpfcnpj=cpfcnpj, pessoa_id=pessoa_id)
        )
        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=[
                    {
                        "input": "cpfcnpj",
                        "message": "Já existe pessoa cadastrada com este CPF/CNPJ.",
                    }
                ],
            )

    def execute(self, pessoa_id: int, pessoa_schema: PPessoaUpdateSchema):
        current = ShowAction().execute(PPessoaIdSchema(pessoa_id=pessoa_id))
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar a pessoa.",
            )

        if pessoa_schema.cpfcnpj is not None:
            self._ensure_cpfcnpj_unique(pessoa_schema.cpfcnpj, pessoa_id)

        return UpdateAction().execute(pessoa_id, pessoa_schema)
