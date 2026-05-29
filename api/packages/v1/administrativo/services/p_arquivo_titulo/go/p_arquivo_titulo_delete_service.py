from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_arquivo_titulo.p_arquivo_titulo_delete_action import (
    DeleteAction,
)
from packages.v1.administrativo.actions.p_arquivo_titulo.p_arquivo_titulo_show_action import (
    ShowAction,
)
from packages.v1.administrativo.repositories.p_arquivo_titulo.p_arquivo_titulo_count_titulo_repository import (
    CountTituloRepository,
)
from packages.v1.administrativo.schemas.p_arquivo_titulo_schema import (
    PArquivoTituloIdSchema,
    PArquivoTituloShowSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import (
    DeleteService as SequenciaDeleteService,
)


class DeleteService:
    def execute(self, arquivo_schema: PArquivoTituloIdSchema):
        current = ShowAction().execute(
            PArquivoTituloShowSchema.from_id(arquivo_schema.arquivo_titulo_id)
        )
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Arquivo de título não encontrado.",
            )

        titulos = CountTituloRepository().execute(arquivo_schema)
        if titulos > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=[
                    {
                        "input": "arquivo_titulo_id",
                        "message": (
                            "Não é possível remover o arquivo: existem títulos vinculados."
                        ),
                    }
                ],
            )

        deleted = DeleteAction().execute(arquivo_schema)
        if deleted:
            SequenciaDeleteService().execute(
                GSequenciaDeleteSchema(
                    sequencia=arquivo_schema.arquivo_titulo_id,
                    tabela="P_ARQUIVO_TITULO",
                )
            )

        return deleted
