from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_livro_natureza.p_livro_natureza_delete_action import (
    DeleteAction,
)
from packages.v1.administrativo.actions.p_livro_natureza.p_livro_natureza_show_action import (
    ShowAction,
)
from packages.v1.administrativo.repositories.p_livro_andamento.p_livro_andamento_count_by_livro_natureza_repository import (
    CountByLivroNaturezaRepository,
)
from packages.v1.administrativo.schemas.p_livro_natureza_schema import PLivroNaturezaIdSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import (
    DeleteService as SequenciaDeleteService,
)


class DeleteService:
    def execute(self, livro_natureza_schema: PLivroNaturezaIdSchema):
        current = ShowAction().execute(livro_natureza_schema)
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar a natureza de livro.",
            )

        vinculos = CountByLivroNaturezaRepository().execute(livro_natureza_schema)
        if vinculos > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=[
                    {
                        "input": "livro_natureza_id",
                        "message": (
                            "Não é possível remover a natureza de livro: "
                            "existem livros de andamento vinculados."
                        ),
                    }
                ],
            )

        data = DeleteAction().execute(livro_natureza_schema)

        if data:
            seq_service = SequenciaDeleteService()
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=livro_natureza_schema.livro_natureza_id,
                tabela="P_LIVRO_NATUREZA",
            )
            seq_service.execute(sequencia_schema)

        return data
