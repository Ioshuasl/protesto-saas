from packages.v1.administrativo.actions.p_template.p_template_delete_action import (
    DeleteAction,
)
from packages.v1.administrativo.actions.p_template.p_template_show_action import (
    ShowAction,
)
from packages.v1.administrativo.schemas.p_template_schema import PTemplateIdSchema


class DeleteService:
    def execute(self, template_schema: PTemplateIdSchema):
        ShowAction().execute(template_schema)
        return DeleteAction().execute(template_schema)
