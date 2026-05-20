from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_usuario_schema import GUsuarioSchema
from packages.v1.administrativo.actions.g_usuario.g_usuario_show_action import ShowAction

class ShowService:

    def execute(self, usuario_schema: GUsuarioSchema):

        # Instânciamento de ação
        show_action = ShowAction()

        # Executa a ação em questão
        data = show_action.execute(usuario_schema)

        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Não foi possível localizar o registro'
            )

        # Retorno da informação
        return data