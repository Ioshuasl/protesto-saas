from packages.v1.administrativo.schemas.g_usuario_schema import GUsuarioIdSchema
from packages.v1.administrativo.actions.g_usuario.g_usuario_delete_action import (
    DeleteAction,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import (
    DeleteService as SequenciaDeleteService,
)
from fastapi import HTTPException, status


class DeleteService:

    def execute(self, usuario_schema: GUsuarioIdSchema):
        # 1. Instanciamento da ação de exclusão
        delete_action = DeleteAction()

        # 2. Executa a exclusão e armazena o resultado
        # Supõe-se que o repositório retorne o registro deletado ou True se houver sucesso
        data = delete_action.execute(usuario_schema)

        # 3. Validação de Sucesso: Só prossegue se 'data' for verdadeiro
        if data:
            # Instancia o serviço de sequência
            seq_service = SequenciaDeleteService()

            # Cria o schema de deleção para a G_SEQUENCIA
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=usuario_schema.usuario_id, tabela="G_USUARIO"
            )

            # Executa a atualização da sequência
            seq_service.execute(sequencia_schema)

            return data

        # 4. Caso a exclusão não tenha afetado nenhuma linha (id não existia, por exemplo)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Não foi possível excluir o registro ou ele não existe.",
        )
