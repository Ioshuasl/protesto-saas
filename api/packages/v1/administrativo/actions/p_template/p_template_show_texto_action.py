from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_template.p_template_show_texto_repository import (
    ShowTextoRepository,
)
from packages.v1.administrativo.schemas.p_template_schema import PTemplateIdSchema


class ShowTextoAction(BaseAction):
    def execute(self, template_schema: PTemplateIdSchema):
        return ShowTextoRepository().execute(template_schema)

