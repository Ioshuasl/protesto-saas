from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_ocorrencias.p_ocorrencias_save_repository import (
    SaveRepository,
)
from packages.v1.administrativo.schemas.p_ocorrencias_schema import POcorrenciasSaveSchema


class SaveAction(BaseAction):
    def execute(self, ocorrencias_schema: POcorrenciasSaveSchema):
        return SaveRepository().execute(ocorrencias_schema)
