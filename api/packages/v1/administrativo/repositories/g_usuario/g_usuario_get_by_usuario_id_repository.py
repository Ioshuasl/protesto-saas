from abstracts.repository import BaseRepository

from packages.v1.administrativo.schemas.g_usuario_schema import GUsuarioSchema

class GetByUsuarioIdRepository(BaseRepository):

    def execute(self, g_usuario_schema = GUsuarioSchema):

        # Define a consulta sql
        sql = """ SELECT * FROM g_usuario gu WHERE gu.usuario_id = :usuarioId """

        # Preenchimento dos parâmetros SQL
        params = {
            'usuarioId': g_usuario_schema.usuario_id
        }

        # Execução da instrução sql
        return self.fetch_one(sql, params)