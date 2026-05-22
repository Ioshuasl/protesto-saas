from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_ocorrencias.p_ocorrencias_delete_action import (
    DeleteAction,
)
from packages.v1.administrativo.actions.p_ocorrencias.p_ocorrencias_show_action import ShowAction
from packages.v1.administrativo.repositories.p_titulo.p_titulo_count_by_ocorrencia_repository import (
    CountByOcorrenciaRepository,
)
from packages.v1.administrativo.schemas.p_ocorrencias_schema import POcorrenciasIdSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import (
    DeleteService as SequenciaDeleteService,
)


class DeleteService:
    def execute(self, ocorrencias_schema: POcorrenciasIdSchema):
        current = ShowAction().execute(ocorrencias_schema)
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar a ocorrência.",
            )

        titulos = CountByOcorrenciaRepository().execute(ocorrencias_schema)
        if titulos > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=[
                    {
                        "input": "ocorrencias_id",
                        "message": "Não é possível remover a ocorrência: existem títulos vinculados.",
                    }
                ],
            )

        data = DeleteAction().execute(ocorrencias_schema)

        if data:
            seq_service = SequenciaDeleteService()
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=ocorrencias_schema.ocorrencias_id,
                tabela="P_OCORRENCIAS",
            )
            seq_service.execute(sequencia_schema)

        return data
