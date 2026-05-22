from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_andamento.p_andamento_delete_action import (
    DeleteAction,
)
from packages.v1.administrativo.actions.p_andamento.p_andamento_show_action import (
    ShowAction,
)
from packages.v1.administrativo.schemas.p_andamento_schema import PAndamentoIdSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import (
    DeleteService as SequenciaDeleteService,
)


class DeleteService:
    def execute(self, andamento_schema: PAndamentoIdSchema):
        current = ShowAction().execute(andamento_schema)
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o andamento.",
            )

        data = DeleteAction().execute(andamento_schema)

        if data:
            seq_service = SequenciaDeleteService()
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=andamento_schema.andamento_id,
                tabela="P_ANDAMENTO",
            )
            seq_service.execute(sequencia_schema)

        return data
