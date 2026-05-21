from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_livro_andamento.p_livro_andamento_delete_action import (
    DeleteAction,
)
from packages.v1.administrativo.actions.p_livro_andamento.p_livro_andamento_show_action import (
    ShowAction,
)
from packages.v1.administrativo.repositories.p_livro_andamento.p_livro_andamento_count_by_titulo_repository import (
    CountByTituloRepository,
)
from packages.v1.administrativo.schemas.p_livro_andamento_schema import PLivroAndamentoIdSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import (
    DeleteService as SequenciaDeleteService,
)


class DeleteService:
    def execute(self, livro_andamento_schema: PLivroAndamentoIdSchema):
        current = ShowAction().execute(livro_andamento_schema)
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o livro de andamento.",
            )

        titulos = CountByTituloRepository().execute(livro_andamento_schema)
        if titulos > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=[
                    {
                        "input": "livro_andamento_id",
                        "message": (
                            "Não é possível remover o livro de andamento: existem "
                            "títulos vinculados (apontamento ou protesto)."
                        ),
                    }
                ],
            )

        data = DeleteAction().execute(livro_andamento_schema)

        if data:
            seq_service = SequenciaDeleteService()
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=livro_andamento_schema.livro_andamento_id,
                tabela="P_LIVRO_ANDAMENTO",
            )
            seq_service.execute(sequencia_schema)

        return data
