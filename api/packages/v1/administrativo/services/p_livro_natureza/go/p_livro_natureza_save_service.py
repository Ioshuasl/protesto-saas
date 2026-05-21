from packages.v1.administrativo.actions.p_livro_natureza.p_livro_natureza_save_action import (
    SaveAction,
)
from packages.v1.administrativo.schemas.p_livro_natureza_schema import PLivroNaturezaSaveSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class SaveService:
    def execute(self, livro_natureza_schema: PLivroNaturezaSaveSchema):
        if not livro_natureza_schema.livro_natureza_id:
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "P_LIVRO_NATUREZA"
            livro_natureza_schema.livro_natureza_id = GenerateService().execute(
                sequencia_schema
            ).sequencia

        return SaveAction().execute(livro_natureza_schema)
