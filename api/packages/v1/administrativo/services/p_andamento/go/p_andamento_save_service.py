from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_andamento.p_andamento_save_action import (
    SaveAction,
)
from packages.v1.administrativo.actions.p_ocorrencia_andamento.p_ocorrencia_andamento_show_action import (
    ShowAction as OcorrenciaAndamentoShowAction,
)
from packages.v1.administrativo.model.p_titulo import get_p_titulo_model
from packages.v1.administrativo.schemas.p_andamento_schema import PAndamentoSaveSchema
from packages.v1.administrativo.schemas.p_ocorrencia_andamento_schema import (
    POcorrenciaAndamentoIdSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class SaveService:
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

    def _ensure_ocorrencia_andamento_exists(self, ocorrencia_andamento_id: int) -> None:
        try:
            OcorrenciaAndamentoShowAction().execute(
                POcorrenciaAndamentoIdSchema(
                    ocorrencia_andamento_id=ocorrencia_andamento_id
                )
            )
        except HTTPException as exc:
            if exc.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=[
                        {
                            "input": "ocorrencia_andamento_id",
                            "message": "Ocorrência de andamento não encontrada.",
                        }
                    ],
                ) from exc
            raise

    def execute(self, andamento_schema: PAndamentoSaveSchema):
        self._ensure_titulo_exists(andamento_schema.titulo_id)
        self._ensure_ocorrencia_andamento_exists(
            andamento_schema.ocorrencia_andamento_id
        )

        if not andamento_schema.andamento_id:
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "P_ANDAMENTO"
            andamento_schema.andamento_id = GenerateService().execute(
                sequencia_schema
            ).sequencia

        return SaveAction().execute(andamento_schema)
