from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_feriado.g_feriado_index_repository import (
    IndexRepository,
)
from packages.v1.administrativo.schemas.g_feriado_schema import GFeriadoIndexSchema


class IndexAction(BaseAction):
    def execute(self, feriado_index_schema: GFeriadoIndexSchema):
        return IndexRepository().execute(feriado_index_schema)
