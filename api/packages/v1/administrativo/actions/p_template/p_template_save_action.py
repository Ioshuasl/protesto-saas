from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_template.p_template_save_repository import (
    SaveRepository,
)
from packages.v1.administrativo.schemas.p_template_schema import PTemplateSaveSchema


class SaveAction(BaseAction):
    def execute(self, template_schema: PTemplateSaveSchema):
        return SaveRepository().execute(template_schema)
