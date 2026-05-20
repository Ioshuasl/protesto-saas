from packages.v1.administrativo.actions.t_livro_natureza.t_livro_natureza_save_action import (
    TLivroNaturezaSaveAction,
)
from packages.v1.administrativo.schemas.t_livro_natureza_schema import (
    TLivroNaturezaSaveSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import (
    GenerateService,
)


class TLivroNaturezaSaveService:
    """Serviço para criar registros em T_LIVRO_NATUREZA."""

    def execute(self, schema: TLivroNaturezaSaveSchema):
        if not schema.livro_natureza_id:
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "T_LIVRO_NATUREZA"

            sequencia = GenerateService().execute(sequencia_schema)
            schema.livro_natureza_id = sequencia.sequencia

        action = TLivroNaturezaSaveAction()
        return action.execute(schema)

