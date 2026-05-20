from abstracts.repository import BaseRepository

from packages.v1.administrativo.schemas.g_usuario_schema import GUsuarioEmailSchema, GUsuarioSchema

class GetByUsuarioEmailRepository(BaseRepository):

    def execute(self, g_usuario_schema = GUsuarioEmailSchema)-> GUsuarioSchema:

        # Define a consulta sql
        sql = """ SELECT * FROM g_usuario gu WHERE gu.email = :email """

        # Preenchimento dos parâmetros SQL
        params = {
            'email': g_usuario_schema.email
        }

        # Execução da instrução sql
        return self.fetch_one(sql, params)