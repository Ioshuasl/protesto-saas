from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_usuario_schema import GUsuarioLoginSchema
from packages.v1.administrativo.actions.g_usuario.g_usuario_get_by_login_action import (
    GetByUsuarioLoginAction,
)


class GetLoginService:

    def execute(self, usuario_schema: GUsuarioLoginSchema, messageValidate: bool):

        # Instânciamento de ação
        login_action = GetByUsuarioLoginAction()

        # Executa a ação em questão
        data = login_action.execute(usuario_schema)

        if messageValidate:

            if not data:
                # Retorna uma exceção
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Não foi possível localizar o login do usuário",
                )

        # Retorno da informação
        return data
