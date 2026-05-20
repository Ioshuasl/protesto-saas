from packages.v1.administrativo.actions.g_feriado.g_feriado_index_action import IndexAction
from packages.v1.administrativo.schemas.g_feriado_schema import GFeriadoIndexSchema


class IndexService:
    def execute(self, feriado_index_schema: GFeriadoIndexSchema):
        index_action = IndexAction()
        data = index_action.execute(feriado_index_schema)
        return data or []
