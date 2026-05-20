from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_usuario_schema import GUsuarioEmailSchema
from packages.v1.administrativo.actions.g_usuario.g_usuario_get_by_email_action import GetByUsuarioEmailAction

class GetEmailService:

    def execute(self, usuario_schema: GUsuarioEmailSchema, messageValidate: bool):

        # Instânciamento de ação
        email_action = GetByUsuarioEmailAction()

        # Executa a ação em questão
        data = email_action.execute(usuario_schema)

        if messageValidate:

            if not data:
                # Retorna uma exceção
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Não foi possível localizar o e-mail do usuário'
                )

        # Retorno da informação
        return data