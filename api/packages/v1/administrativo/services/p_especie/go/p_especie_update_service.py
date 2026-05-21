from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_especie.p_especie_show_action import ShowAction
from packages.v1.administrativo.actions.p_especie.p_especie_update_action import UpdateAction
from packages.v1.administrativo.repositories.p_especie.p_especie_get_by_especie_repository import (
    GetByEspecieRepository,
)
from packages.v1.administrativo.schemas.p_especie_schema import (
    PEspecieEspecieSchema,
    PEspecieIdSchema,
    PEspecieUpdateSchema,
)


class UpdateService:
    @staticmethod
    def _row_value(row, key: str):
        if row is None:
            return None
        lower = key.lower()
        return row.get(lower) or row.get(key) or row.get(key.upper())

    def _ensure_especie_unique(self, especie: str, especie_id: int):
        duplicate = GetByEspecieRepository().execute(
            PEspecieEspecieSchema(especie=especie, especie_id=especie_id)
        )
        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=[
                    {
                        "input": "especie",
                        "message": "Já existe espécie cadastrada com esta sigla.",
                    }
                ],
            )

    def execute(self, especie_id: int, especie_schema: PEspecieUpdateSchema):
        current = ShowAction().execute(PEspecieIdSchema(especie_id=especie_id))
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar a espécie.",
            )

        especie = (
            especie_schema.especie
            if especie_schema.especie is not None
            else self._row_value(current, "especie")
        )
        if especie:
            self._ensure_especie_unique(str(especie), especie_id)

        return UpdateAction().execute(especie_id, especie_schema)
