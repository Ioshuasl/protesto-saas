from packages.v1.administrativo.schemas.g_usuario_schema import GUsuarioIdSchema
from abstracts.repository import BaseRepository
from fastapi import HTTPException, status


class DeleteRepository(BaseRepository):

    def execute(self, usuario_schema: GUsuarioIdSchema):

        try:

            # Montagem do sql (exclusão lógica)
            sql = """
                UPDATE g_usuario
                   SET situacao = 'D'
                 WHERE usuario_id = :usuarioId
                 RETURNING usuario_id
            """

            # Preenchimento de parâmetros
            params = {"usuarioId": usuario_schema.usuario_id}

            # Execução do sql
            response = self.run_and_return(sql, params)

            # Retorna o resultado
            return response

        except Exception as e:

            # Informa que houve uma falha na exclusão do usuário
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir usuário: {e}",
            )