from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_especie.p_especie_save_action import SaveAction
from packages.v1.administrativo.repositories.p_especie.p_especie_get_by_especie_repository import (
    GetByEspecieRepository,
)
from packages.v1.administrativo.schemas.p_especie_schema import (
    PEspecieEspecieSchema,
    PEspecieSaveSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class SaveService:
    def _ensure_especie_unique(self, especie: str, especie_id: int | None = None):
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

    def execute(self, especie_schema: PEspecieSaveSchema):
        self._ensure_especie_unique(especie_schema.especie)

        if not especie_schema.especie_id:
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "P_ESPECIE"
            especie_schema.especie_id = GenerateService().execute(sequencia_schema).sequencia

        return SaveAction().execute(especie_schema)
