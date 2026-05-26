from packages.v1.administrativo.actions.p_template.p_template_show_action import (
    ShowAction,
)
from packages.v1.administrativo.actions.p_template.p_template_update_action import (
    UpdateAction,
)
from packages.v1.administrativo.schemas.p_template_schema import (
    PTemplateIdSchema,
    PTemplateUpdateSchema,
)


class UpdateService:
    def execute(self, template_id: int, template_schema: PTemplateUpdateSchema):
        ShowAction().execute(PTemplateIdSchema(template_id=template_id))
        return UpdateAction().execute(template_id, template_schema)
