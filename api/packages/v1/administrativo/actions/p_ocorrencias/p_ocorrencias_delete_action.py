from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_ocorrencias.p_ocorrencias_delete_repository import (
    DeleteRepository,
)
from packages.v1.administrativo.schemas.p_ocorrencias_schema import POcorrenciasIdSchema


class DeleteAction(BaseAction):
    def execute(self, ocorrencias_schema: POcorrenciasIdSchema):
        return DeleteRepository().execute(ocorrencias_schema)
