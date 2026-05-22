from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_pessoa_vinculo.p_pessoa_vinculo_delete_action import (
    DeleteAction,
)
from packages.v1.administrativo.actions.p_pessoa_vinculo.p_pessoa_vinculo_show_action import (
    ShowAction,
)
from packages.v1.administrativo.schemas.p_pessoa_vinculo_schema import PPessoaVinculoIdSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import (
    DeleteService as SequenciaDeleteService,
)


class DeleteService:
    def execute(self, vinculo_schema: PPessoaVinculoIdSchema):
        current = ShowAction().execute(vinculo_schema)
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o vínculo de pessoa.",
            )

        deleted = DeleteAction().execute(vinculo_schema)

        if deleted:
            seq_service = SequenciaDeleteService()
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=vinculo_schema.pessoa_vinculo_id,
                tabela="P_PESSOA_VINCULO",
            )
            seq_service.execute(sequencia_schema)

        return deleted
