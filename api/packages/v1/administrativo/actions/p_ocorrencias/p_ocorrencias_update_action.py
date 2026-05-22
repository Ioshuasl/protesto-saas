from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_ocorrencias.p_ocorrencias_update_repository import (
    UpdateRepository,
)
from packages.v1.administrativo.schemas.p_ocorrencias_schema import POcorrenciasUpdateSchema


class UpdateAction(BaseAction):
    def execute(self, ocorrencias_id: int, ocorrencias_schema: POcorrenciasUpdateSchema):
        return UpdateRepository().execute(ocorrencias_id, ocorrencias_schema)
