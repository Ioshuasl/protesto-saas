from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_motivos_cancelamento.p_motivos_cancelamento_delete_action import (
    DeleteAction,
)
from packages.v1.administrativo.actions.p_motivos_cancelamento.p_motivos_cancelamento_show_action import (
    ShowAction,
)
from packages.v1.administrativo.repositories.p_titulo.p_titulo_count_by_motivo_cancelamento_repository import (
    CountByMotivoCancelamentoRepository,
)
from packages.v1.administrativo.schemas.p_motivos_cancelamento_schema import (
    PMotivosCancelamentoIdSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import (
    DeleteService as SequenciaDeleteService,
)


class DeleteService:
    def execute(self, motivos_cancelamento_schema: PMotivosCancelamentoIdSchema):
        current = ShowAction().execute(motivos_cancelamento_schema)
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o motivo de cancelamento.",
            )

        titulos = CountByMotivoCancelamentoRepository().execute(
            motivos_cancelamento_schema
        )
        if titulos > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=[
                    {
                        "input": "motivos_cancelamento_id",
                        "message": "Não é possível remover o motivo: existem títulos vinculados.",
                    }
                ],
            )

        data = DeleteAction().execute(motivos_cancelamento_schema)

        if data:
            seq_service = SequenciaDeleteService()
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=motivos_cancelamento_schema.motivos_cancelamento_id,
                tabela="P_MOTIVOS_CANCELAMENTO",
            )
            seq_service.execute(sequencia_schema)

        return data
