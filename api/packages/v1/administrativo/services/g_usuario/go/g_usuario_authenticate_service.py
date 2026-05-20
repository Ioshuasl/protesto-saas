from fastapi import HTTPException, status, Request
from actions.jwt.create_token import CreateToken
from packages.v1.administrativo.schemas.g_usuario_schema import (
    GUsuarioAuthenticateSchema,
)
from packages.v1.administrativo.actions.g_usuario.g_usuario_get_by_authenticate_action import (
    GetByAuthenticateAction,
)
from importlib import import_module
import json

# Funções utilitárias para segurança (hash e verificação de senha)
from actions.security.security import Security

N8NTwoFactorClientService = import_module(
    "packages.v1.integrations.2fa.n8n_2fa_client_service"
).N8NTwoFactorClientService


class AuthenticateService:
    def execute(
        self,
        g_usuario_authenticate_schema: GUsuarioAuthenticateSchema,
        request: Request,
    ):

        # Instânciamento da action de authenticate
        get_by_authenticate_action = GetByAuthenticateAction()

        # Execução e retorno da action
        get_by_authenticate_result = get_by_authenticate_action.execute(
            g_usuario_authenticate_schema
        )

        # Se não encontrou o usuário, lança exceção ou retorna erro
        if get_by_authenticate_result is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Usuário ou senha inválidos",
            )

        # Verifica se a senha do usuário está criptografada
        if not Security.is_hash(get_by_authenticate_result.senha_api):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="A senha informada é inválida",
            )

        # Verifica se a senha do usuário esta correta
        if not Security.verify_senha_api(
            g_usuario_authenticate_schema.senha_api,
            get_by_authenticate_result.senha_api,
        ):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="A senha informada é inválida",
            )

        # Verifica se o usuário esta ativo
        if get_by_authenticate_result.situacao != "A":
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="O usuário encontra-se desativado",
            )

        # Verifica se o usuário tem codigo de segurança
        if not g_usuario_authenticate_schema.codigo_seguranca:
            N8NTwoFactorClientService.request_code(
                usuario_id=int(get_by_authenticate_result.usuario_id),
                email=str(get_by_authenticate_result.email),
                nome_completo=str(get_by_authenticate_result.nome_completo),
            )

            ttl_seconds = Security.get_otp_ttl_seconds()

            return {
                "usuario_id": int(get_by_authenticate_result.usuario_id),
                "nome": str(get_by_authenticate_result.nome_completo),
                "email": str(get_by_authenticate_result.email),
                "two_factor_required": True,
                "challenge_expires_in": ttl_seconds,
            }

        else:
            is_valid_code = N8NTwoFactorClientService.verify_code(
                usuario_id=int(get_by_authenticate_result.usuario_id),
                codigo=str(g_usuario_authenticate_schema.codigo_seguranca),
            )
            if not is_valid_code:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Código de segurança inválido",
                )

            # Gera o token de acesso
            create_token = CreateToken()

            nome_exibicao = (
                get_by_authenticate_result.nome_completo
                or get_by_authenticate_result.login
            )

            # Adiciona os dados do usuário ao token
            jwtUser = {
                "usuario_id": int(get_by_authenticate_result.usuario_id),
                "login": str(get_by_authenticate_result.login),
                "nome": str(nome_exibicao),
                "email": str(get_by_authenticate_result.email),
            }

            # Cria os dados da sessão
            request.session["user"] = jwtUser

            # Retorna o token dos dados do usuário
            return create_token.execute("access-token", json.dumps(jwtUser))
