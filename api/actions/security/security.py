# core/security.py

# Importa CryptContext da biblioteca passlib para operações de hash de senha
import base64
import os

from passlib.context import CryptContext

# Cria uma instância do contexto de criptografia
# O esquema usado é 'bcrypt', que é seguro e amplamente aceito
# O parâmetro 'deprecated="auto"' marca versões antigas como inseguras, se aplicável
CRYPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')


class Security:
    # Lê o TTL do OTP a partir do ambiente e aplica fallback seguro.
    @staticmethod
    def get_otp_ttl_seconds() -> int:
        try:
            return max(60, int(os.getenv("ORIUS_2FA_OTP_TTL_SECONDS", "300")))
        except ValueError:
            return 300

    # Lê o limite de tentativas do OTP e garante valor mínimo de 1.
    @staticmethod
    def get_otp_max_attempts() -> int:
        try:
            return max(1, int(os.getenv("ORIUS_2FA_OTP_MAX_ATTEMPTS", "5")))
        except ValueError:
            return 5

    # Monta o header Authorization Basic com suporte a variáveis legadas.
    @staticmethod
    def get_basic_auth_header() -> str | None:
        # Mantem compatibilidade com variaveis antigas e novas.
        basic_user = (
            os.getenv("ORIUS_2FA_BASIC_USER") or os.getenv("ORIUS_2FA_USER") or ""
        ).strip()
        if not basic_user:
            return None
        basic_password = (
            os.getenv("ORIUS_2FA_BASIC_PASSWORD") or os.getenv("ORIUS_2FA_PASSWORD") or ""
        )
        token = base64.b64encode(
            f"{basic_user}:{basic_password}".encode("utf-8")
        ).decode("ascii")
        return f"Basic {token}"

    # Verifica se a senha tem um hash válido
    @staticmethod
    def is_hash(senha: str) -> bool:
        """
        Verifica se a string fornecida é um hash reconhecido pelo CryptContext.
        """
        return CRYPTO.identify(senha)


    # Verifica se uma senha fornecida corresponde ao hash armazenado
    @staticmethod
    def verify_senha_api(plain_senha_api: str, hashed_senha_api: str) -> bool:
        """
        Compara a senha fornecida em texto puro com o hash armazenado.
        
        :param plain_senha_api: Senha digitada pelo usuário
        :param hashed_senha_api: Hash da senha armazenado no banco de dados
        :return: True se corresponder, False se não
        """
        return CRYPTO.verify(plain_senha_api, hashed_senha_api)


    # Gera o hash de uma senha fornecida
    @staticmethod
    def hash_senha_api(plain_senha_api: str) -> str:
        """
        Gera e retorna o hash da senha fornecida.

        :param plain_senha_api: Senha em texto puro fornecida pelo usuário
        :return: Hash da senha
        """
        return CRYPTO.hash(plain_senha_api)
