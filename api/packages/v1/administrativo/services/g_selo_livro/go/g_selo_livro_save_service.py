from packages.v1.administrativo.actions.g_selo_livro.g_selo_livro_save_action import (
    GSeloLivroSaveAction,
)
from packages.v1.administrativo.schemas.g_selo_livro_schema import GSeloLivroSaveSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class GSeloLivroSaveService:
    def execute(self, data: GSeloLivroSaveSchema):
        if not data.selo_livro_id:
            sequencia = GenerateService().execute(GSequenciaSchema(tabela="G_SELO_LIVRO"))
            data.selo_livro_id = sequencia.sequencia

        return GSeloLivroSaveAction().execute(data)
