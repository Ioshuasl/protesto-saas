from __future__ import annotations

import json
from importlib import import_module
from typing import Any

from fastapi import HTTPException, Request, status

from actions.env.api_env import is_api_development
from actions.jwt.create_token import CreateToken
from actions.security.security import Security
from packages.v1.administrativo.actions.g_usuario.g_usuario_get_by_authenticate_action import (
    GetByAuthenticateAction,
)
from packages.v1.administrativo.schemas.g_usuario_schema import (
    GUsuarioAuthenticateSchema,
)

N8NTwoFactorClientService = import_module(
    "packages.v1.integrations.2fa.n8n_2fa_client_service"
).N8NTwoFactorClientService


class AuthenticateService:
    def execute(
        self,
        g_usuario_authenticate_schema: GUsuarioAuthenticateSchema,
        request: Request,
    ):
        get_by_authenticate_action = GetByAuthenticateAction()
        get_by_authenticate_result = get_by_authenticate_action.execute(
            g_usuario_authenticate_schema
        )

        if get_by_authenticate_result is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Usuário ou senha inválidos",
            )

        if not Security.is_hash(get_by_authenticate_result.senha_api):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="A senha informada é inválida",
            )

        if not Security.verify_senha_api(
            g_usuario_authenticate_schema.senha_api,
            get_by_authenticate_result.senha_api,
        ):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="A senha informada é inválida",
            )

        if get_by_authenticate_result.situacao != "A":
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="O usuário encontra-se desativado",
            )

        # API_ENV=development → token direto; API_ENV=production → 2FA n8n
        if is_api_development():
            return self._issue_access_token(get_by_authenticate_result, request)

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

        is_valid_code = N8NTwoFactorClientService.verify_code(
            usuario_id=int(get_by_authenticate_result.usuario_id),
            codigo=str(g_usuario_authenticate_schema.codigo_seguranca),
        )
        if not is_valid_code:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Código de segurança inválido",
            )

        return self._issue_access_token(get_by_authenticate_result, request)

    @staticmethod
    def _issue_access_token(user: Any, request: Request) -> str:
        create_token = CreateToken()

        nome_exibicao = user.nome_completo or user.login

        jwt_user = {
            "usuario_id": int(user.usuario_id),
            "login": str(user.login),
            "nome": str(nome_exibicao),
            "email": str(user.email),
        }

        request.session["user"] = jwt_user
        return create_token.execute("access-token", json.dumps(jwt_user))
