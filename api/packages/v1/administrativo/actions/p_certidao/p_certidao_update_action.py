from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_certidao.p_certidao_update_repository import (
    UpdateRepository,
)
from packages.v1.administrativo.schemas.p_certidao_schema import PCertidaoUpdateSchema


class UpdateAction(BaseAction):
    def execute(self, certidao_id: int, certidao_schema: PCertidaoUpdateSchema):
        return UpdateRepository().execute(certidao_id, certidao_schema)
