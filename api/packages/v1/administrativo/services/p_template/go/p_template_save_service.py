from packages.v1.administrativo.actions.p_template.p_template_save_action import (
    SaveAction,
)
from packages.v1.administrativo.schemas.p_template_schema import PTemplateSaveSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class SaveService:
    def execute(self, template_schema: PTemplateSaveSchema):
        if not template_schema.template_id:
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "P_TEMPLATE"
            template_schema.template_id = GenerateService().execute(
                sequencia_schema
            ).sequencia

        return SaveAction().execute(template_schema)
