from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_motivos.p_motivos_show_action import ShowAction
from packages.v1.administrativo.actions.p_motivos.p_motivos_update_action import UpdateAction
from packages.v1.administrativo.repositories.p_motivos.p_motivos_get_by_codigo_repository import (
    GetByCodigoRepository,
)
from packages.v1.administrativo.schemas.p_motivos_schema import (
    PMotivosCodigoSchema,
    PMotivosIdSchema,
    PMotivosUpdateSchema,
)


class UpdateService:
    def _ensure_codigo_unique(
        self, codigo: str, motivos_id: int, motivos_schema: PMotivosUpdateSchema
    ):
        if motivos_schema.codigo is None:
            return
        duplicate = GetByCodigoRepository().execute(
            PMotivosCodigoSchema(codigo=codigo, motivos_id=motivos_id)
        )
        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=[
                    {
                        "input": "codigo",
                        "message": "Já existe motivo cadastrado com este código.",
                    }
                ],
            )

    def execute(self, motivos_id: int, motivos_schema: PMotivosUpdateSchema):
        current = ShowAction().execute(PMotivosIdSchema(motivos_id=motivos_id))
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o motivo.",
            )

        codigo = motivos_schema.codigo or current.get("codigo")
        if codigo:
            self._ensure_codigo_unique(codigo, motivos_id, motivos_schema)

        return UpdateAction().execute(motivos_id, motivos_schema)
