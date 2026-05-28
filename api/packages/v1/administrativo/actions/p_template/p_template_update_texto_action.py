from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_template.p_template_update_texto_repository import (
    UpdateTextoRepository,
)
from packages.v1.administrativo.schemas.p_template_schema import PTemplateUpdateTextoSchema


class UpdateTextoAction(BaseAction):
    def execute(self, data: PTemplateUpdateTextoSchema):
        return UpdateTextoRepository().execute(data)

