from packages.v1.administrativo.actions.g_selo_livro.g_selo_livro_delete_action import (
    GSeloLivroDeleteAction,
)
from packages.v1.administrativo.schemas.g_selo_livro_schema import GSeloLivroIdSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import (
    DeleteService as SequenciaDeleteService,
)


class GSeloLivroDeleteService:
    def execute(self, data: GSeloLivroIdSchema):
        result = GSeloLivroDeleteAction().execute(data)

        if result:
            SequenciaDeleteService().execute(
                GSequenciaDeleteSchema(
                    sequencia=data.selo_livro_id,
                    tabela="G_SELO_LIVRO",
                )
            )

        return result
