from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_banco.p_banco_index_repository import (
    IndexRepository,
)
from packages.v1.administrativo.schemas.p_banco_schema import PBancoIndexSchema


class IndexAction(BaseAction):
    def execute(self, banco_index_schema: PBancoIndexSchema):
        return IndexRepository().execute(banco_index_schema)
