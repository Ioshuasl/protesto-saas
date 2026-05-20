from fastapi import HTTPException, status
from packages.v1.administrativo.controllers.g_usuario_controller import (
    GUsuarioIndexSchema,
)
from packages.v1.administrativo.actions.g_usuario.g_usuario_index_action import (
    IndexAction,
)


class IndexService:

    def execute(self, g_usuario_index_schema: GUsuarioIndexSchema):

        # Instânciamento de acções
        index_action = IndexAction()

        # Executa a busca de todas as ações
        data = index_action.execute(g_usuario_index_schema)

        # Verifica se foi loalizado registros
        if not data:
            # Retorna uma exeção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar os usuários",
            )

        # Retorna as informações localizadas
        return data
