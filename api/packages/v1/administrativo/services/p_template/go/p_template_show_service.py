from packages.v1.administrativo.actions.p_template.p_template_show_action import (
    ShowAction,
)
from packages.v1.administrativo.schemas.p_template_schema import PTemplateIdSchema


class ShowService:
    def execute(self, template_schema: PTemplateIdSchema):
        return ShowAction().execute(template_schema)
