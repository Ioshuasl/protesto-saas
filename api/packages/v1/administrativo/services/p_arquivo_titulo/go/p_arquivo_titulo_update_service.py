from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_arquivo_titulo.p_arquivo_titulo_show_action import (
    ShowAction,
)
from packages.v1.administrativo.actions.p_arquivo_titulo.p_arquivo_titulo_update_action import (
    UpdateAction,
)
from packages.v1.administrativo.schemas.p_arquivo_titulo_schema import (
    PArquivoTituloIdSchema,
    PArquivoTituloShowSchema,
    PArquivoTituloUpdateSchema,
)


class UpdateService:
    def execute(self, arquivo_titulo_id: int, arquivo_schema: PArquivoTituloUpdateSchema):
        current = ShowAction().execute(
            PArquivoTituloShowSchema.from_id(arquivo_titulo_id)
        )
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Arquivo de título não encontrado.",
            )
        return UpdateAction().execute(arquivo_titulo_id, arquivo_schema)
