from fastapi import HTTPException, status

from packages.v1.administrativo.actions.g_feriado.g_feriado_show_action import ShowAction
from packages.v1.administrativo.actions.g_feriado.g_feriado_update_action import UpdateAction
from packages.v1.administrativo.repositories.g_feriado.g_feriado_get_by_data_tipo_repository import (
    GetByDataTipoRepository,
)
from packages.v1.administrativo.schemas.g_feriado_schema import (
    GFeriadoDataTipoSchema,
    GFeriadoIdSchema,
    GFeriadoUpdateSchema,
)


class UpdateService:
    @staticmethod
    def _row_value(row, key: str):
        if row is None:
            return None
        lower = key.lower()
        return row.get(lower) or row.get(key) or row.get(key.upper())

    def execute(self, feriado_id: int, feriado_schema: GFeriadoUpdateSchema):
        current = ShowAction().execute(GFeriadoIdSchema(feriado_id=feriado_id))

        data = (
            feriado_schema.data
            if feriado_schema.data is not None
            else self._row_value(current, "data")
        )
        tipo = (
            feriado_schema.tipo
            if feriado_schema.tipo is not None
            else self._row_value(current, "tipo")
        )

        if data is not None and tipo is not None:
            duplicate = GetByDataTipoRepository().execute(
                GFeriadoDataTipoSchema(
                    data=data,
                    tipo=str(tipo),
                    feriado_id=feriado_id,
                )
            )
            if duplicate:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=[
                        {
                            "input": "data",
                            "message": "Já existe feriado cadastrado para esta data e tipo.",
                        }
                    ],
                )

        update_action = UpdateAction()
        return update_action.execute(feriado_id, feriado_schema)
