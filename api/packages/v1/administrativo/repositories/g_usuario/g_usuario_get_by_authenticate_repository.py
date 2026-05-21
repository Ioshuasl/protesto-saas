from __future__ import annotations

from abstracts.repository import BaseRepository
from packages.v1.administrativo.repositories.g_usuario.g_usuario_get_by_cpf_repository import (
    GetByUsuarioCpfRepository,
)
from packages.v1.administrativo.schemas.g_usuario_schema import (
    GUsuarioAuthenticateSchema,
)


class GetByAuthenticateRepository(BaseRepository):
    def execute(self, g_usuario_authenticate_schema: GUsuarioAuthenticateSchema):
        identificador = g_usuario_authenticate_schema.identificador
        mode = g_usuario_authenticate_schema.credential_mode

        if mode == "email":
            sql = """
            SELECT FIRST 1 *
            FROM G_USUARIO gu
            WHERE gu.EMAIL LIKE :identificador
            """
            params = {"identificador": identificador}

        elif mode == "login":
            sql = """
            SELECT FIRST 1 *
            FROM G_USUARIO gu
            WHERE UPPER(TRIM(gu.LOGIN)) = UPPER(TRIM(:identificador))
            """
            params = {"identificador": identificador}

        else:
            cpf_limpo = GetByUsuarioCpfRepository.limpar_cpf(identificador)
            cpf_mascarado = GetByUsuarioCpfRepository.aplicar_mascara_cpf(cpf_limpo)
            sql = """
            SELECT FIRST 1 *
            FROM G_USUARIO gu
            WHERE gu.CPF = :cpf_limpo
               OR gu.CPF = :cpf_mascarado
            """
            params = {
                "cpf_limpo": cpf_limpo,
                "cpf_mascarado": cpf_mascarado,
            }

        return self.fetch_one(sql, params)
