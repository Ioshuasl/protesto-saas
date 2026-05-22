from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_motivos.p_motivos_delete_action import DeleteAction
from packages.v1.administrativo.actions.p_motivos.p_motivos_show_action import ShowAction
from packages.v1.administrativo.repositories.p_titulo.p_titulo_count_by_motivo_apontamento_repository import (
    CountByMotivoApontamentoRepository,
)
from packages.v1.administrativo.schemas.p_motivos_schema import PMotivosIdSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import (
    DeleteService as SequenciaDeleteService,
)


class DeleteService:
    def execute(self, motivos_schema: PMotivosIdSchema):
        current = ShowAction().execute(motivos_schema)
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o motivo.",
            )

        titulos = CountByMotivoApontamentoRepository().execute(motivos_schema)
        if titulos > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=[
                    {
                        "input": "motivos_id",
                        "message": "Não é possível remover o motivo: existem títulos vinculados.",
                    }
                ],
            )

        data = DeleteAction().execute(motivos_schema)

        if data:
            seq_service = SequenciaDeleteService()
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=motivos_schema.motivos_id,
                tabela="P_MOTIVOS",
            )
            seq_service.execute(sequencia_schema)

        return data
