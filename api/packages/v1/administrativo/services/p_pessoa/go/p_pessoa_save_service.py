from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_pessoa.p_pessoa_save_action import SaveAction
from packages.v1.administrativo.repositories.p_pessoa.p_pessoa_get_by_cpfcnpj_repository import (
    GetByCpfcnpjRepository,
)
from packages.v1.administrativo.schemas.p_pessoa_schema import (
    PPessoaCpfcnpjSchema,
    PPessoaSaveSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class SaveService:
    def _ensure_cpfcnpj_unique(self, cpfcnpj: str | None, pessoa_id: int | None = None):
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

    def execute(self, pessoa_schema: PPessoaSaveSchema):
        self._ensure_cpfcnpj_unique(pessoa_schema.cpfcnpj, pessoa_schema.pessoa_id)

        if not pessoa_schema.pessoa_id:
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "P_PESSOA"
            pessoa_schema.pessoa_id = GenerateService().execute(sequencia_schema).sequencia

        return SaveAction().execute(pessoa_schema)
