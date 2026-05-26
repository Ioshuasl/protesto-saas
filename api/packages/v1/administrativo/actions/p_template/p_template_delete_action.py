from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_template.p_template_delete_repository import (
    DeleteRepository,
)
from packages.v1.administrativo.schemas.p_template_schema import PTemplateIdSchema


class DeleteAction(BaseAction):
    def execute(self, template_schema: PTemplateIdSchema):
        return DeleteRepository().execute(template_schema)
