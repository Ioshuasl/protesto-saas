from packages.v1.administrativo.actions.t_livro_andamento.t_livro_andamento_save_action import (
    TLivroAndamentoSaveAction,
)
from packages.v1.administrativo.schemas.t_livro_andamento_schema import TLivroAndamentoSaveSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class TLivroAndamentoSaveService:
    """Service to insert one T_LIVRO_ANDAMENTO row."""
    def execute(self, schema: TLivroAndamentoSaveSchema):

        print(schema)

        if not schema.livro_andamento_id:
            sequencia = GenerateService().execute(
                GSequenciaSchema(
                    tabela="T_LIVRO_ANDAMENTO"
                )
            )
            schema.livro_andamento_id = sequencia.sequencia

        return TLivroAndamentoSaveAction().execute(schema)
