from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_gramatica.g_gramatica_get_by_palavra_repository import (
    GGramaticaGetByPalavraRepository,
)
from packages.v1.administrativo.schemas.g_gramatica_schema import GGramaticaPalavraSchema


class GGramaticaGetByPalavraAction(BaseAction):
    def execute(self, g_gramatica_palavra_schema: GGramaticaPalavraSchema):
        g_gramatica_get_by_palavra_repository = GGramaticaGetByPalavraRepository()
        return g_gramatica_get_by_palavra_repository.execute(g_gramatica_palavra_schema)
