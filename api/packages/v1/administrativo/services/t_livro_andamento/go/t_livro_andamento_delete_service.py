from fastapi import HTTPException, status

from packages.v1.administrativo.actions.t_livro_andamento.t_livro_andamento_delete_action import (
    TLivroAndamentoDeleteAction,
)
from packages.v1.administrativo.actions.t_livro_andamento.t_livro_andamento_show_action import (
    TLivroAndamentoShowAction,
)
from packages.v1.administrativo.schemas.t_livro_andamento_schema import TLivroAndamentoIdSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import (
    DeleteService as SequenciaDeleteService,
)


class TLivroAndamentoDeleteService:
    """Service to delete one T_LIVRO_ANDAMENTO row."""

    def execute(self, schema: TLivroAndamentoIdSchema):
        current_data = TLivroAndamentoShowAction().execute(schema)

        if not current_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel localizar o registro de T_LIVRO_ANDAMENTO.",
            )

        result = TLivroAndamentoDeleteAction().execute(schema)

        sequencia_schema = GSequenciaDeleteSchema(
            tabela="T_LIVRO_ANDAMENTO",
            sequencia=int(schema.livro_andamento_id),
        )
        SequenciaDeleteService().execute(sequencia_schema)

        return result
