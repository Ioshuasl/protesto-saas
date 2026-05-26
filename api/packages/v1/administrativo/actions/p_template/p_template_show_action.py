from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_template.p_template_show_repository import (
    ShowRepository,
)
from packages.v1.administrativo.schemas.p_template_schema import PTemplateIdSchema


class ShowAction(BaseAction):
    def execute(self, template_schema: PTemplateIdSchema):
        return ShowRepository().execute(template_schema)
