from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_template.p_template_update_repository import (
    UpdateRepository,
)
from packages.v1.administrativo.schemas.p_template_schema import PTemplateUpdateSchema


class UpdateAction(BaseAction):
    def execute(self, template_id: int, template_schema: PTemplateUpdateSchema):
        return UpdateRepository().execute(template_id, template_schema)
