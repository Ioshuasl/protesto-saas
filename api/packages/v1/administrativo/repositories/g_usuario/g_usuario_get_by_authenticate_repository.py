from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_usuario_schema import (
    GUsuarioAuthenticateSchema,
)


class GetByAuthenticateRepository(BaseRepository):

    def execute(self, g_usuario_authenticate_schema: GUsuarioAuthenticateSchema):

        # Montagem do sql
        sql = """ SELECT FIRST 1 * FROM g_usuario gu WHERE gu.EMAIL LIKE :email"""

        # Preenchimento dos parâmetros
        params = {"email": g_usuario_authenticate_schema.email}

        # Execução do sql
        response = self.fetch_one(sql, params)

        # Retorna os dados localizados
        return response
