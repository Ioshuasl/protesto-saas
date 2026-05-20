from packages.v1.administrativo.actions.p_banco.p_banco_index_action import IndexAction
from packages.v1.administrativo.schemas.p_banco_schema import PBancoIndexSchema


class IndexService:
    def execute(self, banco_index_schema: PBancoIndexSchema):
        return IndexAction().execute(banco_index_schema)
