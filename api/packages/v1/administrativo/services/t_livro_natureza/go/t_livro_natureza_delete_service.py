from packages.v1.administrativo.actions.t_livro_natureza.t_livro_natureza_delete_action import (
    TLivroNaturezaDeleteAction,
)
from packages.v1.administrativo.actions.t_livro_natureza.t_livro_natureza_show_action import (
    TLivroNaturezaShowAction,
)
from packages.v1.administrativo.schemas.t_livro_natureza_schema import TLivroNaturezaIdSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import (
    DeleteService as SequenciaDeleteService,
)


class TLivroNaturezaDeleteService:
    """Serviço para excluir registros de T_LIVRO_NATUREZA."""

    def execute(self, schema: TLivroNaturezaIdSchema):
        TLivroNaturezaShowAction().execute(schema)
        action = TLivroNaturezaDeleteAction()
        result = action.execute(schema)

        sequencia_schema = GSequenciaDeleteSchema(
            tabela="T_LIVRO_NATUREZA",
            sequencia=int(schema.livro_natureza_id),
        )
        SequenciaDeleteService().execute(sequencia_schema)

        return result
