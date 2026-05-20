from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_banco.p_banco_update_repository import (
    UpdateRepository,
)
from packages.v1.administrativo.schemas.p_banco_schema import PBancoUpdateSchema


class UpdateAction(BaseAction):
    def execute(self, banco_id: int, banco_schema: PBancoUpdateSchema):
        return UpdateRepository().execute(banco_id, banco_schema)
