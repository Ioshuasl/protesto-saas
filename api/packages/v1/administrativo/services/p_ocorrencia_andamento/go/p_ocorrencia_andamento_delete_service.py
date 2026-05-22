from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_ocorrencia_andamento.p_ocorrencia_andamento_delete_action import (
    DeleteAction,
)
from packages.v1.administrativo.actions.p_ocorrencia_andamento.p_ocorrencia_andamento_show_action import (
    ShowAction,
)
from packages.v1.administrativo.repositories.p_andamento.p_andamento_count_by_ocorrencia_andamento_repository import (
    CountByOcorrenciaAndamentoRepository as CountAndamentosRepository,
)
from packages.v1.administrativo.repositories.p_titulo.p_titulo_count_by_ocorrencia_andamento_repository import (
    CountByOcorrenciaAndamentoRepository as CountTitulosRepository,
)
from packages.v1.administrativo.schemas.p_ocorrencia_andamento_schema import (
    POcorrenciaAndamentoIdSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import (
    DeleteService as SequenciaDeleteService,
)


class DeleteService:
    def execute(self, ocorrencia_andamento_schema: POcorrenciaAndamentoIdSchema):
        current = ShowAction().execute(ocorrencia_andamento_schema)
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar a ocorrência de andamento.",
            )

        titulos = CountTitulosRepository().execute(ocorrencia_andamento_schema)
        if titulos > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=[
                    {
                        "input": "ocorrencia_andamento_id",
                        "message": "Não é possível remover: existem títulos vinculados.",
                    }
                ],
            )

        andamentos = CountAndamentosRepository().execute(ocorrencia_andamento_schema)
        if andamentos > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=[
                    {
                        "input": "ocorrencia_andamento_id",
                        "message": "Não é possível remover: existem andamentos vinculados.",
                    }
                ],
            )

        data = DeleteAction().execute(ocorrencia_andamento_schema)

        if data:
            seq_service = SequenciaDeleteService()
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=ocorrencia_andamento_schema.ocorrencia_andamento_id,
                tabela="P_OCORRENCIA_ANDAMENTO",
            )
            seq_service.execute(sequencia_schema)

        return data
