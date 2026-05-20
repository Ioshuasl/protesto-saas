from packages.v1.administrativo.schemas.g_usuario_schema import GUsuarioUpdateSchema
from packages.v1.administrativo.actions.g_usuario.g_usuario_update_action import UpdateAction

class GUsuarioUpdateService: 

    def execute(self, usuario_id: int, usuario_schema: GUsuarioUpdateSchema):     

        # Instânciamento de ações
        updateAction = UpdateAction()

        # Retorna todos produtos desejados
        return updateAction.execute(usuario_id, usuario_schema)