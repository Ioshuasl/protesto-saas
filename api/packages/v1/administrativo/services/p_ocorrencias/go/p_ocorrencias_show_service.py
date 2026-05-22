from packages.v1.administrativo.actions.p_ocorrencias.p_ocorrencias_show_action import ShowAction
from packages.v1.administrativo.schemas.p_ocorrencias_schema import POcorrenciasIdSchema


class ShowService:
    def execute(self, ocorrencias_schema: POcorrenciasIdSchema):
        return ShowAction().execute(ocorrencias_schema)
