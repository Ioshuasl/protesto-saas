from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_usuario_schema import GUsuarioCpfSchema
from packages.v1.administrativo.actions.g_usuario.g_usuario_get_by_cpf_action import GetByUsuarioCpfAction

class GetCpfService:

    def execute(self, usuario_schema: GUsuarioCpfSchema, messageValidate: bool):

        # Instânciamento de ação
        cpf_action = GetByUsuarioCpfAction()

        # Executa a ação em questão
        data = cpf_action.execute(usuario_schema)

        if messageValidate:

            if not data:
                # Retorna uma exceção
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Não foi possível localizar o CPF do usuário'
                )

        # Retorno da informação
        return data