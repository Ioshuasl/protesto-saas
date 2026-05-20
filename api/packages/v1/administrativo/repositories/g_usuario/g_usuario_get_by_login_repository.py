from abstracts.repository import BaseRepository

from packages.v1.administrativo.schemas.g_usuario_schema import (
    GUsuarioLoginSchema,
    GUsuarioSchema,
)


class GetByUsuarioLoginRepository(BaseRepository):

    def execute(self, g_usuario_schema=GUsuarioLoginSchema) -> GUsuarioSchema:

        # Define a consulta sql
        sql = """ SELECT * FROM g_usuario gu WHERE gu.login = :login """

        # Preenchimento dos parâmetros SQL
        params = {"login": g_usuario_schema.login}

        # Execução da instrução sql
        return self.fetch_one(sql, params)
