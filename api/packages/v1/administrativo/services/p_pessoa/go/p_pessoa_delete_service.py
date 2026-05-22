from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_pessoa.p_pessoa_delete_action import DeleteAction
from packages.v1.administrativo.actions.p_pessoa.p_pessoa_show_action import ShowAction
from packages.v1.administrativo.repositories.p_pessoa.p_pessoa_count_banco_by_pessoa_id_repository import (
    CountBancoByPessoaIdRepository,
)
from packages.v1.administrativo.repositories.p_pessoa.p_pessoa_count_vinculos_by_pessoa_id_repository import (
    CountVinculosByPessoaIdRepository,
)
from packages.v1.administrativo.schemas.p_pessoa_schema import PPessoaIdSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import (
    DeleteService as SequenciaDeleteService,
)


class DeleteService:
    def execute(self, pessoa_schema: PPessoaIdSchema):
        current = ShowAction().execute(pessoa_schema)
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar a pessoa.",
            )

        vinculos = CountVinculosByPessoaIdRepository().execute(pessoa_schema)
        if vinculos > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=[
                    {
                        "input": "pessoa_id",
                        "message": (
                            "Não é possível remover a pessoa: existem vínculos "
                            "com títulos."
                        ),
                    }
                ],
            )

        bancos = CountBancoByPessoaIdRepository().execute(pessoa_schema)
        if bancos > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=[
                    {
                        "input": "pessoa_id",
                        "message": (
                            "Não é possível remover a pessoa: existem bancos "
                            "vinculados."
                        ),
                    }
                ],
            )

        data = DeleteAction().execute(pessoa_schema)

        if data:
            seq_service = SequenciaDeleteService()
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=pessoa_schema.pessoa_id,
                tabela="P_PESSOA",
            )
            seq_service.execute(sequencia_schema)

        return data
