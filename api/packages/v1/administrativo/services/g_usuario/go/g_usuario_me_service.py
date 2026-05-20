import ast
from packages.v1.administrativo.schemas.g_usuario_schema import GUsuarioIdSchema
from packages.v1.administrativo.actions.g_usuario.g_usuario_get_by_usuario_id_action import GetByUsuarioIdAction

class MeService:

    def execute(self, current_user):

        get_by_usuario_id_action = GetByUsuarioIdAction()

        # Converte a string para dict de forma segura
        usuario_data = ast.literal_eval(current_user["data"])

        # Define os dados do schema
        g_usuario_schema = GUsuarioIdSchema(usuario_id=int(usuario_data["usuario_id"]))

        # Executa a ação em questão
        return get_by_usuario_id_action.execute(g_usuario_schema)