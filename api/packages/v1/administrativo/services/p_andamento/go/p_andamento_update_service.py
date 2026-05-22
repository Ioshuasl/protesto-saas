from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_andamento.p_andamento_show_action import (
    ShowAction,
)
from packages.v1.administrativo.actions.p_andamento.p_andamento_update_action import (
    UpdateAction,
)
from packages.v1.administrativo.actions.p_ocorrencia_andamento.p_ocorrencia_andamento_show_action import (
    ShowAction as OcorrenciaAndamentoShowAction,
)
from packages.v1.administrativo.model.p_titulo import get_p_titulo_model
from packages.v1.administrativo.schemas.p_andamento_schema import (
    PAndamentoIdSchema,
    PAndamentoUpdateSchema,
)
from packages.v1.administrativo.schemas.p_ocorrencia_andamento_schema import (
    POcorrenciaAndamentoIdSchema,
)


class UpdateService:
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

    def execute(self, andamento_id: int, andamento_schema: PAndamentoUpdateSchema):
        current = ShowAction().execute(PAndamentoIdSchema(andamento_id=andamento_id))
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o andamento.",
            )

        titulo_id = andamento_schema.titulo_id
        if titulo_id is not None:
            self._ensure_titulo_exists(titulo_id)

        ocorrencia_id = andamento_schema.ocorrencia_andamento_id
        if ocorrencia_id is not None:
            self._ensure_ocorrencia_andamento_exists(ocorrencia_id)

        return UpdateAction().execute(andamento_id, andamento_schema)
