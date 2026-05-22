from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_ocorrencia_andamento.p_ocorrencia_andamento_show_action import (
    ShowAction,
)
from packages.v1.administrativo.actions.p_ocorrencia_andamento.p_ocorrencia_andamento_update_action import (
    UpdateAction,
)
from packages.v1.administrativo.repositories.p_ocorrencia_andamento.p_ocorrencia_andamento_get_by_codigo_repository import (
    GetByCodigoRepository,
)
from packages.v1.administrativo.schemas.p_ocorrencia_andamento_schema import (
    POcorrenciaAndamentoCodigoSchema,
    POcorrenciaAndamentoIdSchema,
    POcorrenciaAndamentoUpdateSchema,
)


class UpdateService:
    def _ensure_codigo_unique(
        self,
        codigo: str,
        ocorrencia_andamento_id: int,
        ocorrencia_andamento_schema: POcorrenciaAndamentoUpdateSchema,
    ):
        if ocorrencia_andamento_schema.codigo is None:
            return
        duplicate = GetByCodigoRepository().execute(
            POcorrenciaAndamentoCodigoSchema(
                codigo=codigo, ocorrencia_andamento_id=ocorrencia_andamento_id
            )
        )
        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=[
                    {
                        "input": "codigo",
                        "message": "Já existe ocorrência de andamento cadastrada com este código.",
                    }
                ],
            )

    def execute(
        self,
        ocorrencia_andamento_id: int,
        ocorrencia_andamento_schema: POcorrenciaAndamentoUpdateSchema,
    ):
        current = ShowAction().execute(
            POcorrenciaAndamentoIdSchema(ocorrencia_andamento_id=ocorrencia_andamento_id)
        )
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar a ocorrência de andamento.",
            )

        codigo = ocorrencia_andamento_schema.codigo or current.get("codigo")
        if codigo:
            self._ensure_codigo_unique(
                codigo, ocorrencia_andamento_id, ocorrencia_andamento_schema
            )

        return UpdateAction().execute(ocorrencia_andamento_id, ocorrencia_andamento_schema)
