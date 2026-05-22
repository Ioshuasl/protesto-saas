from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_ocorrencias.p_ocorrencias_show_repository import (
    ShowRepository,
)
from packages.v1.administrativo.schemas.p_ocorrencias_schema import POcorrenciasIdSchema


class ShowAction(BaseAction):
    def execute(self, ocorrencias_schema: POcorrenciasIdSchema):
        return ShowRepository().execute(ocorrencias_schema)
